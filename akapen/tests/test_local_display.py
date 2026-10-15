import argparse
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import urllib.request

ASSETS = Path(__file__).resolve().parents[1] / 'assets'
sys.path.insert(0, str(ASSETS))
spec = importlib.util.spec_from_file_location('relay_local', ASSETS / 'akapen-serve.py')
relay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(relay)


class LocalDisplayTest(unittest.TestCase):
    def test_relay_serves_sheet_and_reads_new_submission(self):
        script = ASSETS / 'akapen-serve.py'
        with tempfile.TemporaryDirectory(prefix='akapen-test-') as tmp:
            root = Path(tmp).resolve()
            sheet = root / '赤ペン review.html'
            sheet.write_text('<h1>ブラウザ確認</h1>', encoding='utf-8')

            def run_cli(*args):
                result = subprocess.run(
                    [sys.executable, str(script), *map(str, args)],
                    capture_output=True, text=True, timeout=15,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                return result.stdout.strip()

            try:
                url = run_cli('open', sheet)
                with urllib.request.urlopen(url, timeout=3) as response:
                    self.assertEqual(response.read().decode('utf-8'), sheet.read_text(encoding='utf-8'))
                first_state = relay.read_state(root)
                run_cli('open', root / sheet.name)
                self.assertEqual(relay.read_state(root)['pid'], first_state['pid'])

                endpoint = url.rsplit('/', 1)[0] + '/akapen-answer'
                body = json.dumps({'sheet': sheet.name, 'text': '【赤ペン回答】テスト'}).encode('utf-8')
                request = urllib.request.Request(endpoint, body, {'Content-Type': 'application/json'})
                with urllib.request.urlopen(request, timeout=3) as response:
                    self.assertTrue(json.load(response)['ok'])
                self.assertEqual(run_cli('read', sheet), '【赤ペン回答】テスト')
            finally:
                run_cli('stop', root)

    def test_link_only_without_browser_or_external_proxy(self):
        with tempfile.TemporaryDirectory() as tmp:
            sheet = Path(tmp) / '日本語.html'
            sheet.write_text('<html></html>', encoding='utf-8')
            for legacy_flag in (False, True):
                with self.subTest(no_browser=legacy_flag):
                    output = io.StringIO()
                    with patch.object(relay, 'relay_running', return_value={'pid': 123, 'port': 8766}), \
                         patch('subprocess.run') as system_command, \
                         patch('os.startfile', create=True) as startfile, \
                         contextlib.redirect_stdout(output):
                        relay.cmd_open(argparse.Namespace(sheet=str(sheet), no_browser=legacy_flag))
                    self.assertEqual(output.getvalue().strip(), 'http://127.0.0.1:8766/%E6%97%A5%E6%9C%AC%E8%AA%9E.html')
                    system_command.assert_not_called()
                    startfile.assert_not_called()

    def test_read_ignores_previous_answer_then_reads_new_submission(self):
        with tempfile.TemporaryDirectory() as tmp:
            sheet = Path(tmp) / 'review.html'
            sheet.write_text('<html></html>', encoding='utf-8')
            answer = Path(tmp) / 'review.html.answer.txt'
            meta = Path(tmp) / 'review.html.answer.json'
            answer.write_text('previous answer\n', encoding='utf-8')
            meta.write_text(json.dumps({'received_epoch': 100}), encoding='utf-8')
            with patch.object(relay, 'relay_running', return_value={'pid': 123, 'port': 8766}), \
                 patch.object(relay.time, 'time', return_value=200), \
                 contextlib.redirect_stdout(io.StringIO()), \
                 contextlib.redirect_stderr(io.StringIO()):
                relay.cmd_open(argparse.Namespace(sheet=str(sheet), no_browser=False))
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
                relay.cmd_read(argparse.Namespace(sheet=str(sheet)))
            self.assertEqual(error.exception.code, 3)
            answer.write_text('new answer\n', encoding='utf-8')
            meta.write_text(json.dumps({'received_epoch': 201}), encoding='utf-8')
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                relay.cmd_read(argparse.Namespace(sheet=str(sheet)))
            self.assertEqual(output.getvalue(), 'new answer\n')


if __name__ == '__main__':
    unittest.main()

# 赤ペン先生（akapen）

We部の学生向けに、AIへ作業を頼む前の「これで進めてよい？」をブラウザで確認する Skill です。AIが1案をHTMLにし、あなたの回答を受け取ってから実装・修正を進めます。

## できること

- **標準**：画面・設計・方針を見て、選択肢への回答、全体コメント、赤ピンを返す。
- **指摘**：記事やREADMEの段落・文字に、直してほしい点を付ける。
- **添削**：ブラウザで文章を直接書き換え、完成形を返す。

## 必要なもの

- ローカルPCで動く Codex または Claude Code と、その利用設定・契約。Skill自体にAIは含まれません。
- Python **3.8以上**（追加のPythonライブラリは不要）、ブラウザ、Git。
- ターミナルで `python3 --version` と `git --version` が実行できること。

Codexを優先した設計で、Claude Codeは互換経路です。OpenCodeの配置先も下に示しますが、**OpenCodeでの動作は未検証**です。クラウド環境は正式対応外です。エージェントとブラウザを同じPCで使ってください。

## インストール

次のどちらか1つの方法を選んでください。どちらもユーザー用の配置で、複数のプロジェクトから使えます。

| 利用するエージェント | 配置先 |
|---|---|
| Codex | `~/.agents/skills/akapen` |
| Claude Code | `~/.claude/skills/akapen` |

以下はmacOS / Linuxのターミナル用です。Windowsでは利用するエージェントと同じ環境に配置し、パスやPythonのコマンドを読み替えてください（Windowsでの動作は未検証）。既存の `akapen` がある場合は、内容を確認してバックアップするまで上書きしないでください。

### 方法1：GitHub CLIでインストール

`gh skill --help` が使えるGitHub CLIが必要です。`gh skill` はプレビュー機能のため仕様変更があります。コマンドが見つからなければ方法2を使ってください。

まず内容を確認します。このリポジトリではSkillが `akapen/` にあるため、パスを `akapen/SKILL.md` と指定します。

```sh
gh skill preview junhat6/akapen-skill akapen/SKILL.md
```

**Codexの場合：**

```sh
if [ -e ~/.agents/skills/akapen ] || [ -L ~/.agents/skills/akapen ]; then
  echo '既存の akapen があります。上書きせず内容を確認してください。'
else
  gh skill install junhat6/akapen-skill akapen/SKILL.md --agent codex --scope user
fi
```

**Claude Codeの場合：**

```sh
if [ -e ~/.claude/skills/akapen ] || [ -L ~/.claude/skills/akapen ]; then
  echo '既存の akapen があります。上書きせず内容を確認してください。'
else
  gh skill install junhat6/akapen-skill akapen/SKILL.md --agent claude-code --scope user
fi
```

`--scope user` を含めて実行してください。省略するとプロジェクト単位の配置になります。

### 方法2：git cloneして手動で配置

まだ同名のフォルダがない作業場所で取得します。既にクローン済みの場合は、そのフォルダで更新してから配置してください。

```sh
git clone https://github.com/junhat6/akapen-skill.git
cd akapen-skill
```

続けて、利用するエージェントのコマンドを実行します。

**Codexの場合：**

```sh
mkdir -p ~/.agents/skills
if [ -e ~/.agents/skills/akapen ] || [ -L ~/.agents/skills/akapen ]; then
  echo '既存の akapen があります。上書きせず内容を確認してください。'
else
  cp -R akapen ~/.agents/skills/akapen
fi
```

**Claude Codeの場合：**

```sh
mkdir -p ~/.claude/skills
if [ -e ~/.claude/skills/akapen ] || [ -L ~/.claude/skills/akapen ]; then
  echo '既存の akapen があります。上書きせず内容を確認してください。'
else
  cp -R akapen ~/.claude/skills/akapen
fi
```

`SKILL.md` だけでなく、`assets`・`references`・`agents` を含む `akapen` フォルダ全体をコピーします。

### インストール後

エージェントの新しい会話を始めて、下の「初めて使う」に進んでください。OpenCodeの配置候補は `~/.config/opencode/skills/akapen` ですが、OpenCodeでの動作は未検証です。

## 初めて使う

作業するプロジェクトをエージェントで開き、例えば次のように頼みます。

> 赤ペン先生で、学習記録アプリのトップ画面を作る前に1案を見せてください。まだ実装は始めないでください。

Codexでは `$akapen`、Claude Codeでは `/akapen` でも呼び出せます。文章なら「READMEを指摘モードで確認したい」「この記事を添削モードで直接直したい」と伝えます。

1. AIが `./akapen/<話題>-01.html` とローカルURLを作ります。
2. 提示されたリンクを自分で開き、HTML上で回答・指摘・編集します。
3. ブラウザの **［送信］** を押します。
4. エージェントとの会話へ戻り、**「回答しました」** と送ります。ブラウザの送信だけでは会話は再開しません。
5. AIが保存された回答を読み、反映します。未決定があれば次のシートで確認します。

`file://` で開いた場合は［貼り付ける文章を作る］を押し、できた全文を会話へ貼ってください。コピーできなければ画面のテキスト欄から手動でコピーします。

## 更新

更新前にエージェントの作業と中継サーバを終了し、配置済みの `akapen` フォルダをバックアップしてください。自分で変更したファイルがある場合は差分を確認します。

- **方法1で導入した場合**：`gh skill update --help` で利用中のCLIの更新オプションを確認し、対象のSkillを更新してください。
- **方法2で導入した場合**：最初にクローンした `akapen-skill` フォルダで `git pull --ff-only` を実行します。配置済みフォルダを別名へ移してから、方法2の該当するコピー手順で最新の `akapen` を配置してください。

## つまずいたら

| 症状 | 確認すること |
|---|---|
| Skillが見つからない | 配置先の `akapen/SKILL.md` を確認し、新しい会話で明示的に呼び出す |
| `python3` が見つからない | Python 3.8以上を導入する。必要ならAIに実行コマンドの読み替えを依頼する |
| リンクが開かない | AIとブラウザが同じPCか確認し、中継の再起動を依頼する。ポート番号はAIが実際に出したものを使う |
| 回答が届かない | ［送信］の完了表示を確認し、会話で「回答しました」と伝える。`file://` なら全文を貼る |
| 古い下書きが出る | AIに次の番号のシートを作ってもらう。下書きはブラウザ内にも保存される |

中継の確認・終了を手動で行う場合（Codexの配置例。作業プロジェクト内で実行）：

```sh
python3 ~/.agents/skills/akapen/assets/akapen-serve.py status ./akapen
python3 ~/.agents/skills/akapen/assets/akapen-serve.py stop ./akapen
```

## 安全に使うために

- 中継は `127.0.0.1` で動き、**HTMLの親フォルダ全体を静的配信**します。生成物専用の `./akapen/` を使い、秘密鍵・トークン・個人情報・非公開資料を置かないでください。機密ファイルへのシンボリックリンクも置かないでください。
- ポートをインターネットへ公開・転送しないでください。終了後は中継を止めます。
- HTMLには原稿や提案が埋め込まれ、回答は `.answer.txt` / `.answer.json` に保存されます。ブラウザ内の下書きも含め、共有PCやGitへの誤公開に注意してください。生成先をプロジェクトの `.gitignore` に追加することをおすすめします。
- 標準・添削テンプレートは **Google Fontsへ外部通信**します。オフラインでは代替フォントになります。完全に外部通信を止める必要がある場合は、使用前にHTMLのGoogle Fonts指定を除去してください。
- AIサービスに渡す内容は、そのサービスのデータ取扱い設定も確認してください。AIの提案・変更内容は自分で確認します。回答前の実装や自動commitを認めるSkillではありません。

## ライセンス

MIT License。既存コードの `Copyright (c) 2026 AI-Driven R&D Dept` と許諾文を [LICENSE](LICENSE) に保持しています。再配布時も著作権表示と許諾文を保持してください。

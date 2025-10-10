# cat-file-watcher

**ファイル変更監視ツール - ファイルの変更を検知してコマンドを実行**

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
</p>

## Quick Links
| 項目 | リンク |
|------|--------|
| 📊 開発状況 | [generated-docs/daily-summaries](generated-docs/daily-summaries) |

## 概要

ファイルのタイムスタンプの変更を監視し、ファイルが更新されたときにコマンドを実行するファイル監視ツールです。

## 特徴

- 複数のファイルを同時に監視
- ファイル変更時にカスタムコマンドを実行
- TOML設定ファイルで設定可能
- 軽量で使いやすい

## インストール

1. このリポジトリをクローン:
```bash
git clone https://github.com/cat2151/cat-file-watcher.git
cd cat-file-watcher
```

2. 依存パッケージをインストール:
```bash
pip install -r requirements.txt
```

## 使い方

設定ファイルを指定してファイルウォッチャーを実行:

```bash
python src/cat_file_watcher.py --config-filename config.toml
```

引数:
- `--config-filename`: TOML設定ファイルのパス（必須）

## 設定

監視するファイルと実行するコマンドを定義するTOML設定ファイルを作成します:

```toml
[files]
"myfile.txt" = { command = "echo 'File changed!'" }
"script.py" = { command = "python -m pytest tests/" }
```

### 設定フォーマット

設定ファイルには、各エントリがファイル名とコマンドをマッピングする `[files]` セクションが必要です:

- **キー**: 監視するファイルのパス（相対パスまたは絶対パス）
- **値**: 実行するシェルコマンドを含む `command` フィールドを持つオブジェクト

### 設定例

様々なユースケースの完全な例は `config.example.toml` を参照してください。

```toml
[files]
"document.txt" = { command = "cp document.txt document.txt.bak" }
"app.log" = { command = "notify-send 'Log Updated' 'New entries in app.log'" }
```

## 動作の仕組み

1. ツールがTOML設定ファイルを読み込みます
2. 指定されたすべてのファイルの更新タイムスタンプを監視します
3. ファイルのタイムスタンプが変更されると、関連するコマンドを実行します
4. このプロセスはCtrl+Cで停止するまで継続的に繰り返されます

## ライセンス

MIT License - 詳細はLICENSEファイルを参照してください

※このREADME.mdはREADME.ja.mdを元にGeminiの翻訳でGitHub Actionsにより自動生成しています

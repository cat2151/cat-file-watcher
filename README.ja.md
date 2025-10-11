# cat-file-watcher

**ファイル変更監視ツール - ファイルの変更を検知してコマンドを実行**

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
</p>

※このドキュメントは大部分がAI生成です。issueをagentに投げて生成させました。一部（コンセプト、使い分け）は人力で書いています

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
python -m src --config-filename config.toml
```

引数:
- `--config-filename`: TOML設定ファイルのパス（必須）

## 設定

監視するファイルと実行するコマンドを定義するTOML設定ファイルを作成します:

```toml
# デフォルトの監視間隔
# 時間フォーマット: "1s"（1秒）、"2m"（2分）、"3h"（3時間）、"0.5s"（0.5秒）
default_interval = "1s"

# 設定ファイル自体の変更チェック間隔
config_check_interval = "1s"

# コマンド実行ログのファイルパス（省略可）
log_file = "command_execution.log"

# エラーログのファイルパス（省略可）
# error_log_file = "error.log"

# コマンド実行抑制ログのファイルパス（省略可）
# suppression_log_file = "suppression.log"

# 時間帯の定義（省略可）
[time_periods]
business_hours = { start = "09:00", end = "17:00" }
night_shift = { start = "23:00", end = "01:00" }

[files]
"myfile.txt" = { command = "echo 'File changed!'" }
"script.py" = { command = "python -m pytest tests/", interval = "2s" }
"src/main.py" = { command = "make build", suppress_if_process = "vim|emacs|code" }
"batch.csv" = { command = "./process.sh", time_period = "night_shift" }
"important.txt" = { command = "backup.sh", enable_log = true }
"lib/module.c" = { command = "gcc -c module.c -o module.o", cwd = "./lib" }
```

### 設定フォーマット

設定ファイルには、各エントリがファイル名とコマンドをマッピングする `[files]` セクションが必要です:

- **キー**: 監視するファイルまたはディレクトリのパス（相対パスまたは絶対パス）
  - ファイルの場合: ファイルの変更時刻が変わったときにコマンドを実行
  - ディレクトリの場合: ディレクトリの変更時刻が変わったとき（ファイルの追加・削除など）にコマンドを実行
- **値**: 実行するシェルコマンドを含む `command` フィールドを持つオブジェクト
  - `command` (必須): ファイルまたはディレクトリ変更時に実行するシェルコマンド
  - `interval` (省略可): このファイルまたはディレクトリの監視間隔。時間フォーマット（"1s", "2m", "3h", "0.5s"）で指定します。小数点も使用可能です（例: "0.5s"は0.5秒）。省略した場合は `default_interval` が使用されます
  - `suppress_if_process` (省略可): 実行中のプロセス名にマッチする正規表現パターン。マッチするプロセスが見つかった場合、コマンド実行をスキップします。エディタなどの特定のプログラムが実行中の場合にアクションをトリガーしないようにする場合に便利です
  - `time_period` (省略可): ファイルまたはディレクトリを監視する時間帯の名前。`[time_periods]` セクションで定義された時間帯名を指定します。指定した時間帯内でのみ監視します
  - `enable_log` (省略可): `true` に設定すると、コマンド実行の詳細をログファイルに記録します（デフォルト: `false`）。グローバル設定で `log_file` の設定が必要です
  - `cwd` (省略可): コマンドを実行する前に指定されたパスに作業ディレクトリを変更します。これにより、コマンド内の相対パスが指定されたディレクトリから解決されます

### グローバル設定

- `default_interval` (省略可): すべてのファイルおよびディレクトリのデフォルト監視間隔。時間フォーマット（"1s", "2m", "3h", "0.5s"）で指定します。小数点も使用可能です（例: "0.5s"は0.5秒）。省略した場合は"1s"（1秒）が使用されます
- `config_check_interval` (省略可): 設定ファイル自体の変更チェック間隔。時間フォーマット（"1s", "2m", "3h", "0.5s"）で指定します。設定ファイルが変更されると自動的に再読み込みされます。省略した場合は"1s"（1秒）が使用されます
- `log_file` (省略可): コマンド実行の詳細を記録するログファイルのパス。設定すると、`enable_log = true` が指定されたファイルまたはディレクトリのコマンド実行情報（タイムスタンプ、パス、TOML設定内容）がこのファイルに記録されます
- `error_log_file` (省略可): コマンド実行エラーの詳細を記録するエラーログファイルのパス。設定すると、コマンド失敗時のエラーメッセージ、実行コマンド、標準エラー出力、スタックトレースなどの詳細情報がこのファイルに記録されます
- `suppression_log_file` (省略可): コマンド実行抑制の詳細を記録するログファイルのパス。設定すると、`suppress_if_process` によりコマンド実行がスキップされた際の情報（タイムスタンプ、ファイルパス、プロセスパターン、マッチしたプロセス）がこのファイルに記録されます


### 時間帯設定

`[time_periods]` セクション（省略可）で時間帯を定義できます:

- 各時間帯は名前を付けて定義します
- `start`: 開始時刻（HH:MM形式、例: "09:00"）
- `end`: 終了時刻（HH:MM形式、例: "17:00"）
- 日をまたぐ時間帯もサポート（例: `start = "23:00", end = "01:00"`）
- ファイルごとに `time_period` パラメータで時間帯名を指定すると、その時間帯内でのみそのファイルまたはディレクトリを監視します

例:
```toml
[time_periods]
business_hours = { start = "09:00", end = "17:00" }  # 通常の時間帯
night_shift = { start = "23:00", end = "01:00" }     # 日をまたぐ時間帯
```

### 設定例

様々なユースケースの完全な例は `examples/config.example.toml` を参照してください。

```toml
# デフォルトの監視間隔を1秒に設定
default_interval = "1s"

# 設定ファイル自体の変更チェック間隔を1秒に設定
config_check_interval = "1s"

# コマンド実行の詳細を記録するログファイル（省略可）
log_file = "command_execution.log"

# エラーログファイル（省略可）
# error_log_file = "error.log"

# コマンド実行抑制ログファイル（省略可）
# suppression_log_file = "suppression.log"

# 時間帯の定義
[time_periods]
business_hours = { start = "09:00", end = "17:00" }
after_hours = { start = "18:00", end = "08:00" }  # 日をまたぐ

[files]
# デフォルト間隔を使用（1秒ごとにチェック）
"document.txt" = { command = "cp document.txt document.txt.bak" }

# カスタム間隔を指定（0.5秒ごとにチェック）
"app.log" = { command = "notify-send 'Log Updated' 'New entries in app.log'", interval = "0.5s" }

# カスタム間隔を指定（5秒ごとにチェック）
"config.ini" = { command = "systemctl reload myapp", interval = "5s" }

# 営業時間のみ監視
"report.txt" = { command = "python generate_report.py", time_period = "business_hours" }

# 営業時間外のみ監視（バッチ処理など）
"batch.csv" = { command = "./process_batch.sh", time_period = "after_hours" }

# 重要なファイルのログを有効化（タイムスタンプ、ファイルパス、設定内容を記録）
"important.txt" = { command = "backup.sh", enable_log = true }
```

## 動作の仕組み

1. ツールがTOML設定ファイルを読み込みます
2. 指定されたすべてのファイルの更新タイムスタンプを監視します
3. ファイルのタイムスタンプが変更されると、関連するコマンドを実行します
4. 設定ファイル自体も監視し、変更があれば自動的に再読み込みします
5. このプロセスはCtrl+Cで停止するまで継続的に繰り返されます

### コマンド実行時の出力

実行されたコマンドの標準出力および標準エラー出力は、**リアルタイムで**コンソールに表示されます:

- **出力表示**: コマンドの標準出力と標準エラー出力は、実行中に逐次コンソールに表示されます。長時間実行されるコマンドでも、途中経過をリアルタイムで確認できます
- **失敗時**: コマンドが失敗した場合（終了コード 0以外）、`Error: Command failed for '<ファイルパス>' with exit code <コード>` というメッセージが表示されます
- **エラーログファイル**: `error_log_file` を設定している場合、コマンド失敗時のエラーメッセージと実行コマンドがログファイルに記録されます

コマンド実行のタイムアウトは30秒に設定されており、それを超えるとタイムアウトエラーが発生します。

## コンセプト

toml記述内容がシンプルでメンテしやすいことを優先します

## 使い分け

手軽にファイル更新監視したい場合、楽に運用したい場合は、cat-file-watcher

散在するファイルを手早く更新監視on/offしたい場合は、cat-file-watcher

これにしかない各種機能を利用したい場合は、cat-file-watcher

もっと高度な機能を使いたい場合は、ほかのアプリ

TypeScriptアプリ開発等には、スタンダードにタスクランナー

## ライセンス

MIT License - 詳細はLICENSEファイルを参照してください

※このREADME.mdはREADME.ja.mdを元にGeminiの翻訳でGitHub Actionsにより自動生成しています

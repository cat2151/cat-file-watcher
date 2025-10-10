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
# デフォルトの監視間隔（ミリ秒単位）
default_interval = 1000

# 設定ファイル自体の変更チェック間隔（ミリ秒単位）
config_check_interval = 1000

# 時間帯の定義（省略可）
[time_periods]
business_hours = { start = "09:00", end = "17:00" }
night_shift = { start = "23:00", end = "01:00" }

[files]
"myfile.txt" = { command = "echo 'File changed!'" }
"script.py" = { command = "python -m pytest tests/", interval = 2000 }
"src/main.py" = { command = "make build", suppress_if_process = "vim|emacs|code" }
"batch.csv" = { command = "./process.sh", time_period = "night_shift" }
```

### 設定フォーマット

設定ファイルには、各エントリがファイル名とコマンドをマッピングする `[files]` セクションが必要です:

- **キー**: 監視するファイルのパス（相対パスまたは絶対パス）
- **値**: 実行するシェルコマンドを含む `command` フィールドを持つオブジェクト
  - `command` (必須): ファイル変更時に実行するシェルコマンド
  - `interval` (省略可): このファイルの監視間隔（ミリ秒単位）。省略した場合は `default_interval` が使用されます
  - `suppress_if_process` (省略可): 実行中のプロセス名にマッチする正規表現パターン。マッチするプロセスが見つかった場合、コマンド実行をスキップします。エディタなどの特定のプログラムが実行中の場合にアクションをトリガーしないようにする場合に便利です
  - `time_period` (省略可): ファイルを監視する時間帯の名前。`[time_periods]` セクションで定義された時間帯名を指定します。指定した時間帯内でのみファイルを監視します

### グローバル設定

- `default_interval` (省略可): すべてのファイルのデフォルト監視間隔（ミリ秒単位）。省略した場合は1000ms（1秒）が使用されます
- `config_check_interval` (省略可): 設定ファイル自体の変更チェック間隔（ミリ秒単位）。設定ファイルが変更されると自動的に再読み込みされます。省略した場合は1000ms（1秒）が使用されます

### 時間帯設定

`[time_periods]` セクション（省略可）で時間帯を定義できます:

- 各時間帯は名前を付けて定義します
- `start`: 開始時刻（HH:MM形式、例: "09:00"）
- `end`: 終了時刻（HH:MM形式、例: "17:00"）
- 日をまたぐ時間帯もサポート（例: `start = "23:00", end = "01:00"`）
- ファイルごとに `time_period` パラメータで時間帯名を指定すると、その時間帯内でのみファイルを監視します

例:
```toml
[time_periods]
business_hours = { start = "09:00", end = "17:00" }  # 通常の時間帯
night_shift = { start = "23:00", end = "01:00" }     # 日をまたぐ時間帯
```

### 設定例

様々なユースケースの完全な例は `config.example.toml` を参照してください。

```toml
# デフォルトの監視間隔を1秒に設定
default_interval = 1000

# 設定ファイル自体の変更チェック間隔を1秒に設定
config_check_interval = 1000

# 時間帯の定義
[time_periods]
business_hours = { start = "09:00", end = "17:00" }
after_hours = { start = "18:00", end = "08:00" }  # 日をまたぐ

[files]
# デフォルト間隔を使用（1秒ごとにチェック）
"document.txt" = { command = "cp document.txt document.txt.bak" }

# カスタム間隔を指定（500msごとにチェック）
"app.log" = { command = "notify-send 'Log Updated' 'New entries in app.log'", interval = 500 }

# カスタム間隔を指定（5秒ごとにチェック）
"config.ini" = { command = "systemctl reload myapp", interval = 5000 }

# 営業時間のみ監視
"report.txt" = { command = "python generate_report.py", time_period = "business_hours" }

# 営業時間外のみ監視（バッチ処理など）
"batch.csv" = { command = "./process_batch.sh", time_period = "after_hours" }
```

## 動作の仕組み

1. ツールがTOML設定ファイルを読み込みます
2. 指定されたすべてのファイルの更新タイムスタンプを監視します
3. ファイルのタイムスタンプが変更されると、関連するコマンドを実行します
4. 設定ファイル自体も監視し、変更があれば自動的に再読み込みします
5. このプロセスはCtrl+Cで停止するまで継続的に繰り返されます

## ライセンス

MIT License - 詳細はLICENSEファイルを参照してください

※このREADME.mdはREADME.ja.mdを元にGeminiの翻訳でGitHub Actionsにより自動生成しています

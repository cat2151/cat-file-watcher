Last updated: 2025-12-11

# Project Overview

## プロジェクト概要
- ファイルの変更をリアルタイムで監視し、変更が検知された際に指定されたコマンドを自動実行するツールです。
- TOML形式の設定ファイルを通じて、監視対象ファイル、実行コマンド、監視間隔、特定の条件での実行抑制など、柔軟な監視ルールを定義できます。
- 軽量で使いやすく、開発や自動化のワークフローを効率化するために設計されており、Windows環境でのフォーカス奪取防止機能も備えています。

## 技術スタック
- フロントエンド: 該当なし（本プロジェクトはコマンドラインインターフェースツールです）
- 音楽・オーディオ: 該当なし
- 開発ツール:
    - **Python**: プロジェクトの主要な開発言語。ファイル監視ロジック、設定解析、コマンド実行など、全てのコア機能がPythonで実装されています。
    - **pip**: Pythonパッケージのインストールと管理に使用されるツール。依存ライブラリの管理に利用されます。
    - **git**: ソースコードのバージョン管理システム。プロジェクトの変更履歴の追跡と共同開発に不可欠です。
    - **VS Code**: 開発に使用される統合開発環境（IDE）。設定ファイル(`.vscode/`)が存在し、開発効率を高めるための設定が含まれています。
- テスト:
    - **pytest**: Python用の強力なテストフレームワーク。プロジェクトの機能が意図通りに動作することを検証するために使用されます。
- ビルドツール:
    - **TOML**: 設定ファイルの記述に採用されている、人間が読み書きしやすいデータシリアライズ形式。監視対象やコマンド、グローバル設定などを定義します。
    - **subprocess**: Python標準ライブラリの一部。外部コマンドをPythonスクリプト内から実行するために利用されます。
- 言語機能:
    - **Python**: 高レベルで汎用的なプログラミング言語。ファイルシステムの監視、プロセス管理、時間処理など、本ツールの主要な機能実装に使用されています。
- 自動化・CI/CD:
    - **pre-commit**: コミット前に自動的にコード品質チェックやフォーマットを行うためのフレームワーク。コードの一貫性を保ち、エラーを早期に発見するのに役立ちます。
    - **GitHub Actions**: リポジトリのイベントに基づいてワークフローを自動実行するCI/CDサービス。テストの実行やドキュメントの自動生成などに利用されています。
- 開発標準:
    - **Ruff**: Pythonコードのリンティングとフォーマットを高速に行うツール。コードの品質と一貫性を維持するために使用されます。
    - **.editorconfig**: 異なるエディタやIDE間でコードスタイル（インデント、改行コードなど）の一貫性を定義・維持するためのファイル。

## ファイル階層ツリー
```
📄 .editorconfig
📄 .gitignore
📄 .pre-commit-config.yaml
📁 .vscode/
  📖 README.md
  📊 extensions.json
  📊 settings.json
📄 LICENSE
📖 README.ja.md
📖 README.md
📄 _config.yml
📄 dev-requirements.txt
📁 examples/
  📄 config.example.toml
  📄 monitoring-group-example.toml
📁 generated-docs/
🌐 googled947dc864c270e07.html
📁 issue-notes/
  📖 117.md
  📖 119.md
  📖 121.md
  📖 123.md
  📖 125.md
  📖 127.md
  📖 129.md
  📖 62.md
  📖 71.md
  📖 78.md
📄 pytest.ini
📄 requirements.txt
📄 ruff.toml
📁 src/
  📄 __init__.py
  📄 __main__.py
  📄 cat_file_watcher.py
  📄 command_executor.py
  📄 config_loader.py
  📄 config_validator.py
  📄 error_logger.py
  📄 external_config_merger.py
  📄 file_monitor.py
  📄 interval_parser.py
  📄 process_detector.py
  📄 time_period_checker.py
  📄 timestamp_printer.py
📁 tests/
  📄 test_basics.py
  📄 test_cat_file_watcher.py
  📄 test_colorama.py
  📄 test_command_logging.py
  📄 test_command_suppression.py
  📄 test_commands_and_processes_sections.py
  📄 test_config_reload.py
  📄 test_cwd.py
  📄 test_directory_monitoring.py
  📄 test_empty_filename.py
  📄 test_empty_filename_messages.py
  📄 test_error_log_clarity.py
  📄 test_error_logging.py
  📄 test_external_files.py
  📄 test_external_files_reload.py
  📄 test_interval_parser.py
  📄 test_intervals.py
  📄 test_issue_129.py
  📄 test_main_loop_interval.py
  📄 test_multiple_empty_filenames.py
  📄 test_new_interval_format.py
  📄 test_no_focus.py
  📄 test_print_color_specification.py
  📄 test_process_detection.py
  📄 test_suppression_logging.py
  📄 test_terminate_if_process.py
  📄 test_terminate_if_window_title.py
  📄 test_terminate_message_color.py
  📄 test_time_periods.py
  📄 test_timestamp.py
  📄 test_timestamp_reset_on_reload.py
```

## ファイル詳細説明
- **`.editorconfig`**: 異なるエディタやIDEを使用する開発者間で、コードのインデントスタイル、文字コード、改行コードなどの基本設定を統一するためのファイルです。
- **`.gitignore`**: Gitがバージョン管理の対象外とするファイルやディレクトリを指定します。一時ファイルや生成物、ローカル設定などが含まれます。
- **`.pre-commit-config.yaml`**: `pre-commit`フレームワークの設定ファイル。コミット前に自動で実行されるフック（例: コードフォーマット、リンターチェック）を定義します。
- **`.vscode/`**: Visual Studio Code用の設定を格納するディレクトリです。
    - **`README.md`**: VS Code環境に関する説明や指示が含まれる可能性があります。
    - **`extensions.json`**: プロジェクト推奨のVS Code拡張機能リストを定義します。
    - **`settings.json`**: プロジェクト固有のVS Codeワークスペース設定（例: リンターの設定、フォーマッターの設定）を定義します。
- **`LICENSE`**: プロジェクトのライセンス情報（MIT License）が記載されています。ソフトウェアの使用、配布、変更に関する条件を示します。
- **`README.ja.md`**: プロジェクトの概要、特徴、インストール方法、使い方、設定方法などを日本語で説明するメインのドキュメントです。
- **`README.md`**: `README.ja.md`の英語版で、プロジェクト情報を英語で提供します。
- **`_config.yml`**: GitHub Pagesサイトの設定ファイル。ドキュメントサイトの構築に使用される場合があります。
- **`dev-requirements.txt`**: 開発時にのみ必要となるPythonパッケージ（例: テストフレームワーク、リンター）のリストを定義します。
- **`examples/`**: 設定ファイルの使用例を格納するディレクトリです。
    - **`config.example.toml`**: さまざまなユースケースに対応する設定例が記載されたTOMLファイルです。
    - **`monitoring-group-example.toml`**: 監視グループに関する具体的な設定例を示すTOMLファイルです。
- **`generated-docs/`**: AIによって自動生成されたドキュメントやレポートが格納されるディレクトリです。
- **`googled947dc864c270e07.html`**: 通常、Googleサイトの所有権確認（Google Search Consoleなど）に使用されるファイルであり、プロジェクトの実行機能には直接関係ありません。
- **`issue-notes/`**: 開発過程で発生した課題や検討事項に関するメモが格納されています。
- **`pytest.ini`**: `pytest`テストフレームワークの設定ファイル。テストの実行オプションなどを定義します。
- **`requirements.txt`**: プロジェクトの実行に最低限必要なPythonパッケージのリストを定義します。
- **`ruff.toml`**: Ruffリンターおよびフォーマッターの設定ファイル。コードスタイルのルールやチェック項目を定義します。
- **`src/`**: プロジェクトの主要なソースコードが格納されているディレクトリです。
    - **`__init__.py`**: Pythonパッケージの初期化ファイル。`src`ディレクトリをPythonパッケージとして認識させます。
    - **`__main__.py`**: `python -m src`のようにモジュールとして実行された際のエントリーポイントとなるファイルです。メインの処理を開始します。
    - **`cat_file_watcher.py`**: ファイル監視ツールの主要なロジックが含まれています。メインループ、設定の再読み込み、ファイル変更の調整などを行います。
    - **`command_executor.py`**: ファイル変更時に実行されるコマンドの処理を担当します。コマンドの実行、出力の処理、エラーハンドリングなどが含まれます。
    - **`config_loader.py`**: TOML形式の設定ファイルを読み込み、パースし、アプリケーションが利用できるデータ構造に変換する役割を担います。
    - **`config_validator.py`**: 読み込まれた設定ファイルの整合性や正当性を検証するロジックが含まれています。
    - **`error_logger.py`**: コマンド実行時のエラーやアプリケーション内部のエラーを記録するためのロギング機能を提供します。
    - **`external_config_merger.py`**: 複数の設定ソース（例: グローバル設定とファイル固有の設定）を適切にマージするロジックを扱います。
    - **`file_monitor.py`**: 特定のファイルやディレクトリのタイムスタンプ変更を検出し、監視間隔に基づいて変更を追跡するコアな監視ロジックを実装しています。
    - **`interval_parser.py`**: "1s", "2m"などの時間間隔を表す文字列を、プログラムで扱える秒数に変換する機能を持ちます。
    - **`process_detector.py`**: 特定のプロセスが実行中であるかどうかを検出し、コマンド実行抑制などの機能に利用されます。
    - **`time_period_checker.py`**: 設定で定義された時間帯（例: 営業時間、夜間）に基づいて、現在時刻がその時間帯内にあるかを判断する機能を提供します。
    - **`timestamp_printer.py`**: ログやコンソール出力にタイムスタンプを付与するためのユーティリティ機能を提供します。
- **`tests/`**: プロジェクトのテストコードが格納されているディレクトリです。各ファイルは特定の機能や側面に対するテストを担当します。

## 関数詳細説明
プロジェクト情報に具体的な関数名やシグネチャの詳細が提供されていないため、主要なファイル名から推測される役割に基づき、想定される関数とその機能について説明します。

- **`run_watcher()` (src/cat_file_watcher.py 内に想定)**
    - **役割**: ファイル監視ツールのメイン実行ループを制御します。
    - **機能**: 設定ファイルのロード、監視対象の初期化、指定された間隔でのファイル変更チェック、変更検知時のコマンド実行、設定ファイルの再読み込み処理などを継続的に管理します。
    - **引数**: 設定ファイルのパス、その他のグローバル設定オプションなど。
    - **戻り値**: なし。通常、ユーザーからの終了シグナル（Ctrl+Cなど）があるまで実行を続けます。

- **`load_config()` (src/config_loader.py 内に想定)**
    - **役割**: TOML形式の設定ファイルを読み込み、解析します。
    - **機能**: 指定された設定ファイルパスからTOMLデータを読み込み、Pythonの辞書オブジェクトに変換します。設定のデフォルト値の適用や基本的な構造のチェックも行う可能性があります。
    - **引数**: 設定ファイルへのパス（`config_filename`）。
    - **戻り値**: 解析された設定内容を含む辞書オブジェクト。

- **`validate_config()` (src/config_validator.py 内に想定)**
    - **役割**: 読み込まれた設定内容が有効であるかを検証します。
    - **機能**: 必須フィールドの存在確認、データ型の妥当性、時間帯定義の形式チェックなど、設定ルールに違反がないかを確認します。無効な設定に対してはエラーを報告します。
    - **引数**: 読み込まれた設定内容を含む辞書オブジェクト。
    - **戻り値**: 設定が有効であれば`True`、そうでなければ`False`（または例外を発生）。

- **`check_for_changes()` (src/file_monitor.py 内に想定)**
    - **役割**: 監視対象のファイルやディレクトリの変更を検出します。
    - **機能**: 各監視対象の最終更新タイムスタンプを定期的に取得し、前回のチェック時と比較して変更があったかを判断します。必要に応じて、監視間隔や時間帯の制約も考慮します。
    - **引数**: 監視対象のリスト（パス、前回のタイムスタンプなど）、現在の設定。
    - **戻り値**: 変更が検出された監視対象のリスト。

- **`execute_command()` (src/command_executor.py 内に想定)**
    - **役割**: 指定されたシェルコマンドを実行します。
    - **機能**: コマンド文字列をオペレーティングシステム上で実行し、その標準出力、標準エラー出力、終了コードを処理します。Windowsでのフォーカス抑制や作業ディレクトリの変更などのオプションもサポートする可能性があります。
    - **引数**: 実行するコマンド文字列、実行オプション（`cwd`、`no_focus`など）、ロギング設定。
    - **戻り値**: コマンドの実行結果（例: 成功/失敗を示すブール値、終了コード）。

- **`parse_interval()` (src/interval_parser.py 内に想定)**
    - **役割**: 時間間隔を表す文字列（例: "1s", "0.5s", "2m"）を秒数に変換します。
    - **機能**: 与えられた文字列を解析し、数値と単位（秒、分、時間）を抽出し、対応する秒数の浮動小数点値を返します。
    - **引数**: 時間間隔を表す文字列。
    - **戻り値**: 秒単位の数値（`float`）。

- **`is_process_running()` (src/process_detector.py 内に想定)**
    - **役割**: 特定のプロセスが現在実行中であるかを検出します。
    - **機能**: 指定されたプロセス名や正規表現パターンにマッチするプロセスがシステム上で動作しているかを確認します。コマンド実行の抑制機能で使用されます。
    - **引数**: プロセス名または正規表現パターン。
    - **戻り値**: マッチするプロセスが実行中であれば`True`、そうでなければ`False`。

- **`is_within_time_period()` (src/time_period_checker.py 内に想定)**
    - **役割**: 現在の時刻が定義された時間帯内にあるかを判断します。
    - **機能**: 定義された開始時刻と終了時刻を基に、現在時刻がその時間範囲に含まれるか（日をまたぐ時間帯も含む）をチェックします。
    - **引数**: 時間帯の定義（開始時刻、終了時刻）。
    - **戻り値**: 現在時刻が時間帯内であれば`True`、そうでなければ`False`。

## 関数呼び出し階層ツリー
```
[プロジェクト情報に、関数呼び出し階層ツリーを生成するための十分な情報が含まれていませんでした。]

---
Generated at: 2025-12-11 07:02:13 JST

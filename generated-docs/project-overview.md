Last updated: 2025-10-19

# Project Overview

## プロジェクト概要
- ファイルの変更をリアルタイムで検知し、自動的に指定されたコマンドを実行するツールです。
- 開発ワークフローの自動化、タスクの効率化、および継続的な監視を支援します。
- プロジェクトはPythonで実装され、設定はTOML形式で管理されます。

## 技術スタック
- フロントエンド: 該当なし
- 音楽・オーディオ:
  - Tone.js: Web Audio APIを利用した高度な音声処理を行うJavaScriptライブラリ。
  - Web Audio API: ブラウザ上で音声を生成、処理するためのAPI（Tone.jsを介して利用）。
  - MML (Music Macro Language): 音楽記法を解析し、音楽を生成するためのパーサー。
- 開発ツール:
  - Node.js runtime: JavaScriptコードを実行するための環境。主に自動化スクリプトやツールチェインで利用されます。
- テスト:
  - pytest: Pythonでテストを記述・実行するための強力なフレームワーク。
- ビルドツール: 該当なし
- 言語機能:
  - Python: プロジェクトの主要なプログラミング言語。
- 自動化・CI/CD:
  - GitHub Actions: コードの変更をトリガーに自動テスト、ビルド、デプロイなどのCI/CDパイプラインを実行するサービス。
  - i18n automation: 自動翻訳ワークフロー。
- 開発標準:
  - EditorConfig: 異なるエディタやIDE間で、インデントスタイルや文字コードなどのコーディングスタイルを統一するための設定ファイルフォーマット。
  - Ruff: Pythonコードの高速なリンターおよびフォーマッター。

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
📄 dev-requirements.txt
📁 examples/
  📄 config.example.toml
  📄 monitoring-group-example.toml
📁 generated-docs/
📁 issue-notes/
  📖 101.md
  📖 103.md
  📖 105.md
  📖 11.md
  📖 16-refactoring-summary.md
  📖 19-refactoring-summary.md
  📖 21.md
  📖 24.md
  📖 26.md
  📖 27.md
  📖 30.md
  📖 33.md
  📖 35.md
  📖 37.md
  📖 39.md
  📖 41.md
  📖 43.md
  📖 46.md
  📖 48.md
  📖 50.md
  📖 52.md
  📖 54.md
  📖 56.md
  📖 57.md
  📖 58.md
  📖 62.md
  📖 63.md
  📖 65.md
  📖 67.md
  📖 69.md
  📖 71-investigation-report.md
  📖 71.md
  📖 72.md
  📖 74.md
  📖 76.md
  📖 78.md
  📖 79-investigation-report.md
  📖 79.md
  📖 81.md
  📖 83-completion.md
  📖 85.md
  📖 87.md
  📖 89.md
  📖 91.md
  📖 93.md
  📖 95.md
  📖 97.md
  📖 99.md
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
  📄 test_error_log_clarity.py
  📄 test_error_logging.py
  📄 test_external_files.py
  📄 test_interval_parser.py
  📄 test_intervals.py
  📄 test_main_loop_interval.py
  📄 test_multiple_empty_filenames.py
  📄 test_new_interval_format.py
  📄 test_process_detection.py
  📄 test_suppression_logging.py
  📄 test_terminate_if_process.py
  📄 test_time_periods.py
  📄 test_timestamp.py
```

## ファイル詳細説明
- **`.editorconfig`**: コーディングスタイルをプロジェクト全体で統一するための設定ファイル。
- **`.gitignore`**: Gitがバージョン管理の対象としないファイルやディレクトリを指定するファイル。
- **`.pre-commit-config.yaml`**: `pre-commit`フックの設定ファイル。コミット前にコードの自動チェックを実行します。
- **`.vscode/`**: Visual Studio Codeエディタのワークスペース設定を格納するディレクトリ。
  - **`README.md`**: VS Code関連のドキュメントや補足情報。
  - **`extensions.json`**: プロジェクトで推奨されるVS Code拡張機能のリスト。
  - **`settings.json`**: プロジェクト固有のVS Code設定。
- **`LICENSE`**: プロジェクトの利用条件を定めるライセンス情報ファイル。
- **`README.ja.md`**, **`README.md`**: プロジェクトの概要、機能、使い方などを説明するドキュメント（日本語版と英語版）。
- **`dev-requirements.txt`**: 開発環境で必要となるPythonライブラリの一覧。
- **`examples/`**: 設定ファイルの記述例を格納するディレクトリ。
  - **`config.example.toml`**: メインの設定ファイル（`config.toml`）の記述例。
  - **`monitoring-group-example.toml`**: 監視グループ設定の記述例。
- **`generated-docs/`**: プロジェクト内で自動生成されたドキュメントを格納するディレクトリ。
- **`issue-notes/`**: AIエージェントによって生成されたIssueに関する詳細なノートや調査報告を格納するディレクトリ。
- **`pytest.ini`**: `pytest`テストフレームワークの設定ファイル。
- **`requirements.txt`**: プロジェクトの実行に必要となるPythonライブラリの一覧。
- **`ruff.toml`**: PythonのリンターおよびフォーマッターであるRuffの設定ファイル。
- **`src/`**: プロジェクトの主要なソースコードが格納されているディレクトリ。
  - **`__init__.py`**: Pythonパッケージとして`src`ディレクトリを認識させるためのファイル。
  - **`__main__.py`**: Pythonパッケージが直接実行された際のエントリポイントとなるスクリプト。
  - **`cat_file_watcher.py`**: ファイル変更監視の全体的なロジックとコマンド実行の調整を担うメインスクリプト。
  - **`command_executor.py`**: 外部コマンドを実行するための機能を提供するモジュール。
  - **`config_loader.py`**: TOML形式の設定ファイルを読み込む機能を提供するモジュール。
  - **`config_validator.py`**: 読み込まれた設定の構造と内容が正しいかを検証するモジュール。
  - **`error_logger.py`**: プロジェクト内で発生したエラーをログとして記録するためのモジュール。
  - **`external_config_merger.py`**: 外部から追加の設定ファイルを読み込み、現在の設定にマージする機能を提供するモジュール。
  - **`file_monitor.py`**: 指定されたファイルやディレクトリの変更を監視し、イベントを通知する機能を提供するモジュール。
  - **`interval_parser.py`**: 時間間隔を表す文字列（例: "10s", "5m"）を解析して数値に変換するモジュール。
  - **`process_detector.py`**: 特定のプロセスが現在実行中であるかを検出する機能を提供するモジュール。
  - **`time_period_checker.py`**: 現在時刻が特定の日時や時間帯の条件を満たしているかをチェックするモジュール。
  - **`timestamp_printer.py`**: ログ出力などに使用するタイムスタンプを整形して表示する機能を提供するモジュール。
- **`tests/`**: プロジェクトのテストコードが格納されているディレクトリ。
  - **`test_basics.py`**, **`test_cat_file_watcher.py`** など: 各モジュールや機能の正しさを検証するための単体テストおよび結合テストスクリプト。

## 関数詳細説明
このプロジェクトでは、`src/`ディレクトリ内の各Pythonファイルが特定の機能を持つ関数群を提供します。以下に主な機能とその役割を説明します。具体的な引数や戻り値はコードベースを参照する必要があります。

- **`src/__main__.py`**:
  - `main()`: アプリケーションの開始点となる関数。設定の読み込み、監視インスタンスの初期化、メインループの実行などを統括します。
- **`src/cat_file_watcher.py`**:
  - `CatFileWatcher` クラス (または関連関数): ファイル監視オブジェクトを管理し、変更イベントをトリガーとしてコマンド実行ロジックを呼び出します。監視対象の登録やイベントハンドリングの中核を担います。
- **`src/command_executor.py`**:
  - `execute_command()`: 指定された外部コマンドを新しいプロセスとして実行する機能を提供します。コマンドの出力や実行結果のハンドリングも含まれる可能性があります。
- **`src/config_loader.py`**:
  - `load_config()`: 指定されたファイルパスからTOML形式の設定ファイルを読み込み、Pythonの辞書やオブジェクトとして返します。
- **`src/config_validator.py`**:
  - `validate_config()`: 読み込まれた設定データが事前に定義されたルールやスキーマに従っているかを検証し、不備があればエラーを報告します。
- **`src/error_logger.py`**:
  - `log_error()`: エラーメッセージや例外情報を整形して、コンソールやログファイルに出力する機能を提供します。
- **`src/external_config_merger.py`**:
  - `merge_external_configs()`: 複数の設定ソース（例: メイン設定と外部設定ファイル）を読み込み、それらを結合して最終的な設定を生成します。
- **`src/file_monitor.py`**:
  - `start_monitoring()`, `stop_monitoring()`: 指定されたファイルやディレクトリの変更を非同期的に監視し、変更が検出された際に登録されたコールバック関数を呼び出す機能を提供します。
- **`src/interval_parser.py`**:
  - `parse_interval()`: "10s" (10秒) や "5m" (5分) のような時間間隔を表す文字列を解析し、適切な数値形式（例: 秒数）に変換します。
- **`src/process_detector.py`**:
  - `is_process_running()`: 特定の名前やIDを持つプロセスがシステム上で現在実行中であるかを検出する機能を提供します。
- **`src/time_period_checker.py`**:
  - `is_within_time_period()`: 現在の時刻が設定された特定の時間帯（例: 午前9時から午後5時まで）の中にあるかを判定する機能を提供します。
- **`src/timestamp_printer.py`**:
  - `print_timestamp()`, `format_timestamp()`: 現在の時刻を示すタイムスタンプを生成し、特定の形式で出力またはフォーマットする機能を提供します。

## 関数呼び出し階層ツリー
```
関数呼び出し階層を分析できませんでした

---
Generated at: 2025-10-19 07:02:11 JST

Last updated: 2025-11-10

# Project Overview

## プロジェクト概要
- TOML設定に基づき、指定されたファイルやディレクトリの変更を監視します。
- 変更が検知されると、定義されたカスタムコマンドを自動的に実行します。
- 軽量で柔軟なファイル変更監視ツールとして、様々なタスクの自動化を支援します。

## 技術スタック
- フロントエンド: 本プロジェクトはコマンドラインインターフェース(CLI)ツールであり、専用のフロントエンド技術は使用していません。
- 音楽・オーディオ: 該当する技術はありません。
- 開発ツール:
  - **Ruff**: Pythonコードのリンティングとフォーマットに使用され、コード品質の維持と統一されたコーディングスタイルを保証します。
  - **Git**: ソースコードのバージョン管理に使用されます。
- テスト:
  - **pytest**: Pythonアプリケーションのテストフレームワークとして、堅牢なテストスイートの作成と実行をサポートします。
- ビルドツール: 本プロジェクトはPythonスクリプトであり、特別なビルドツールは使用していません。
- 言語機能:
  - **Python**: プロジェクトの主要なプログラミング言語です。ファイルシステム操作、プロセス管理、設定ファイルのパースなどに活用されています。
  - **TOML**: 設定ファイルの記述形式として採用されており、人間が読み書きしやすい構造化された設定を可能にします。
- 自動化・CI/CD:
  - **GitHub Actions**: リポジトリの各種イベント（コミット、プルリクエストなど）をトリガーに、自動テスト実行やドキュメント生成などのCI/CDパイプラインを構築・実行するために使用されます。
- 開発標準:
  - **Ruff**: コード品質とスタイルガイドの強制に利用されます。

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
📁 issue-notes/
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
  📄 test_main_loop_interval.py
  📄 test_multiple_empty_filenames.py
  📄 test_new_interval_format.py
  📄 test_print_color_specification.py
  📄 test_process_detection.py
  📄 test_suppression_logging.py
  📄 test_terminate_if_process.py
  📄 test_terminate_message_color.py
  📄 test_time_periods.py
  📄 test_timestamp.py
```

## ファイル詳細説明
-   `.editorconfig`: 異なるエディタやIDE間で一貫したコーディングスタイルを維持するための設定ファイルです。
-   `.gitignore`: Gitによるバージョン管理から除外するファイルやディレクトリを指定するファイルです。
-   `.pre-commit-config.yaml`: Gitのpre-commitフックを管理するための設定ファイルで、コミット前にコード品質チェックなどを自動実行します。
-   `.vscode/`: Visual Studio Codeエディタ用の設定や推奨拡張機能を格納するディレクトリです。
    -   `README.md`: VS Code関連の追加情報や設定について説明するファイルです。
    -   `extensions.json`: プロジェクト推奨のVS Code拡張機能をリストするファイルです。
    -   `settings.json`: プロジェクト固有のVS Codeワークスペース設定ファイルです。
-   `LICENSE`: プロジェクトのライセンス情報（MIT License）を記載したファイルです。
-   `README.ja.md`: プロジェクトの日本語版概要ドキュメントです。
-   `README.md`: プロジェクトの英語版概要ドキュメントです。
-   `_config.yml`: GitHub Pagesなどの静的サイトジェネレータで利用される設定ファイルです。
-   `dev-requirements.txt`: 開発環境で使用されるPython依存パッケージ（例: Ruff, pytest）をリストするファイルです。
-   `examples/`: 設定ファイルの例を格納するディレクトリです。
    -   `config.example.toml`: フル機能のTOML設定例を示します。
    -   `monitoring-group-example.toml`: 監視グループ設定のTOML例を示します。
-   `generated-docs/`: AIエージェントなどによって自動生成されたドキュメントを格納するディレクトリです。
-   `issue-notes/`: 開発中に生成されたIssue関連のメモを格納するディレクトリです。
    -   `62.md`, `71.md`, `78.md`: 特定のIssueに関する詳細メモや経緯が記述されています。
-   `pytest.ini`: pytestテストフレームワークの設定ファイルです。
-   `requirements.txt`: プロジェクトの実行に必要なPython依存パッケージをリストするファイルです。
-   `ruff.toml`: Ruffリンター/フォーマッターの設定ファイルです。
-   `src/`: プロジェクトの主要なソースコードが格納されているディレクトリです。
    -   `__init__.py`: `src` ディレクトリをPythonパッケージとして識別するためのファイルです。
    -   `__main__.py`: プロジェクトの実行エントリポイントです。コマンドライン引数を処理し、メインのファイルウォッチャーロジックを起動します。
    -   `cat_file_watcher.py`: ファイル監視のメインロジックを実装します。設定を読み込み、ファイル変更を検出し、関連するコマンドを実行する主要なループを管理します。
    -   `command_executor.py`: 指定されたシェルコマンドを実行し、その出力やエラーを処理・記録する責任を負います。
    -   `config_loader.py`: TOML形式の設定ファイルを読み込み、パースしてアプリケーションが使用できる形式に変換します。
    -   `config_validator.py`: 読み込まれた設定オブジェクトの構造と値の妥当性を検証します。
    -   `error_logger.py`: コマンド実行時のエラーやその他のシステムエラーを記録するためのユーティリティを提供します。
    -   `external_config_merger.py`: 外部の設定ファイルをマージする機能を提供します。
    -   `file_monitor.py`: 個々のファイルやディレクトリのタイムスタンプを監視し、変更を検出するためのロジックをカプセル化します。
    -   `interval_parser.py`: "1s", "2m" のような時間文字列を秒数に変換するユーティリティ関数を提供します。
    -   `process_detector.py`: 特定のプロセスがシステム上で実行中であるかを検出する機能を提供します。コマンド実行抑制などに利用されます。
    -   `time_period_checker.py`: 定義された時間帯（例: 営業時間、夜間）に基づいて現在時刻がその時間帯内にあるかをチェックするロジックを実装します。
    -   `timestamp_printer.py`: ログやコンソール出力のために、フォーマットされたタイムスタンプを生成するユーティリティです。
-   `tests/`: プロジェクトのテストコードを格納するディレクトリです。各ファイルは特定の機能やコンポーネントのテストを担当します。
    -   `test_basics.py`: 基本的なファイル監視機能のテスト。
    -   `test_cat_file_watcher.py`: `cat_file_watcher.py` の主要機能のテスト。
    -   `test_colorama.py`: `colorama` ライブラリを使用した色付き出力のテスト。
    -   `test_command_logging.py`: コマンド実行ログ機能のテスト。
    -   `test_command_suppression.py`: コマンド実行抑制機能のテスト。
    -   `test_commands_and_processes_sections.py`: コマンドとプロセス関連の設定セクションのテスト。
    -   `test_config_reload.py`: 設定ファイルの自動再読み込み機能のテスト。
    -   `test_cwd.py`: `cwd` オプション（作業ディレクトリ変更）のテスト。
    -   `test_directory_monitoring.py`: ディレクトリ監視機能のテスト。
    -   `test_empty_filename.py`: 空のファイル名指定時のテスト。
    -   `test_empty_filename_messages.py`: 空のファイル名に関連するエラーメッセージのテスト。
    -   `test_error_log_clarity.py`: エラーログの明確さに関するテスト。
    -   `test_error_logging.py`: エラーログ機能のテスト。
    -   `test_external_files.py`: 外部ファイル（設定など）に関するテスト。
    -   `test_external_files_reload.py`: 外部ファイルの再読み込みテスト。
    -   `test_interval_parser.py`: インターバルパース機能のテスト。
    -   `test_intervals.py`: 監視間隔機能のテスト。
    -   `test_main_loop_interval.py`: メインループのインターバルに関するテスト。
    -   `test_multiple_empty_filenames.py`: 複数の空ファイル名指定時のテスト。
    -   `test_new_interval_format.py`: 新しいインターバルフォーマットのテスト。
    -   `test_print_color_specification.py`: 出力色の仕様に関するテスト。
    -   `test_process_detection.py`: プロセス検出機能のテスト。
    -   `test_suppression_logging.py`: コマンド実行抑制ログ機能のテスト。
    -   `test_terminate_if_process.py`: 特定プロセス実行時の終了機能のテスト。
    -   `test_terminate_message_color.py`: 終了メッセージの色に関するテスト。
    -   `test_time_periods.py`: 時間帯監視機能のテスト。
    -   `test_timestamp.py`: タイムスタンプ機能のテスト。

## 関数詳細説明
情報が提供されていないため、プロジェクトのソースコードから個々の関数の詳細を抽出することはできません。しかし、主要なモジュールは以下の機能を提供しています。

-   `src/__main__.py`: アプリケーションのエントリポイントとして、コマンドライン引数をパースし、ファイルウォッチャーの主要なインスタンスを初期化して開始する役割を担う機能。
-   `src/cat_file_watcher.py`: メインの監視ループを制御する機能。設定に基づいてファイル変更を定期的にチェックし、変更があった場合にコマンド実行機能を呼び出します。
-   `src/command_executor.py`: 外部コマンドを実行し、その標準出力、標準エラー、終了コードを処理する機能。ログ記録やエラーハンドリングも担当します。
-   `src/config_loader.py`: TOMLファイルを読み込み、パースしてPythonの辞書またはオブジェクトに変換する機能。
-   `src/file_monitor.py`: 特定のファイルパスやディレクトリパスの最終変更タイムスタンプを取得し、前回のチェック時と比較して変更を検出する機能。
-   `src/interval_parser.py`: "1s", "0.5m" のような時間表現文字列を秒単位の数値に変換する機能。
-   `src/process_detector.py`: 指定された正規表現パターンにマッチするプロセスが現在実行中であるかをシステム上でチェックする機能。
-   `src/time_period_checker.py`: 定義された開始時刻と終了時刻に基づいて、現在時刻が特定の時間帯内にあるかどうかを判断する機能。
-   `src/timestamp_printer.py`: ログやコンソール出力のために、フォーマットされたタイムスタンプを生成する機能。
-   その他のファイルも、それぞれの役割に応じたユーティリティ機能やロジックを提供します。

## 関数呼び出し階層ツリー
```
関数呼び出し階層を分析できませんでした

---
Generated at: 2025-11-10 07:02:01 JST

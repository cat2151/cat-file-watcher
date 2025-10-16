Last updated: 2025-10-17

# Project Overview

## プロジェクト概要
- ファイルの変更をリアルタイムで監視し、変更が検知された際に指定されたコマンドを自動実行するツールです。
- 開発ワークフローの自動化、テストの自動実行、特定のファイル変更時のタスク処理などを効率化します。
- 柔軟な設定（TOML形式）により、監視対象、実行コマンド、時間制限、プロセス検出などの詳細な制御が可能です。

## 技術スタック
- フロントエンド: (特になし - このプロジェクトはCLIツールです)
- 音楽・オーディオ:
  - Tone.js: Web Audio APIを抽象化するJavaScriptライブラリです。
  - Web Audio API: ブラウザで高度なオーディオ処理を行うためのAPIです。（CLIツールの直接機能ではありませんが、特定の拡張機能や関連用途で用いられる可能性があります。）
  - MML (Music Macro Language): 音楽をテキストで記述するための記法パーサーです。
- 開発ツール:
  - Node.js runtime: JavaScriptコードを実行するための環境です。
- テスト:
  - pytest: Pythonで書かれた強力なテストフレームワークです。
- ビルドツール: (特になし - 主にスクリプト実行形式です)
- 言語機能:
  - Python: プロジェクトの主要なプログラミング言語です。
- 自動化・CI/CD:
  - GitHub Actions: コードの変更に基づいて自動テスト、デプロイ、ドキュメント生成などを行うCI/CDプラットフォームです。具体的には、プロジェクト要約の自動生成、Issue管理、READMEの多言語翻訳、i18n自動化ワークフローが設定されています。
- 開発標準:
  - EditorConfig: 異なるエディタやIDE間でコードスタイル（インデント、改行コードなど）を統一するための設定ファイルです。
  - Ruff: Pythonのコードを高速にチェックし、フォーマットするリンター兼フォーマッターです。

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
- **.editorconfig**: エディタのコードスタイル設定を定義し、プロジェクト全体で一貫したコーディングスタイルを強制します。
- **.gitignore**: Gitがバージョン管理から無視すべきファイルやディレクトリを指定します。
- **.pre-commit-config.yaml**: pre-commitフレームワークの設定ファイルで、コミット前に特定のフック（コード整形、リンティングなど）を自動実行するために使用されます。
- **.vscode/**: Visual Studio Codeに関連する設定を格納するディレクトリです。
  - **README.md**: VS Codeの推奨設定や拡張機能に関する情報を提供するドキュメントです。
  - **extensions.json**: このプロジェクトで推奨されるVS Code拡張機能のリストです。
  - **settings.json**: このワークスペース固有のVS Code設定を定義します。
- **LICENSE**: プロジェクトの利用条件を定めるライセンス情報が記載されています。
- **README.ja.md**: プロジェクトの概要、使い方、設定方法などを日本語で説明するドキュメントです。
- **README.md**: プロジェクトの概要、使い方、設定方法などを英語で説明するドキュメントです。
- **dev-requirements.txt**: 開発環境で必要となるPythonパッケージの一覧を定義します。
- **examples/**: 設定ファイルの例が格納されているディレクトリです。
  - **config.example.toml**: メインの設定ファイル（TOML形式）の記述例です。
  - **monitoring-group-example.toml**: 監視グループに関する設定例（TOML形式）です。
- **generated-docs/**: 自動生成されたドキュメントやレポートを格納するディレクトリです。
- **issue-notes/**: 過去のIssueに関する議論、調査報告、解決策などの詳細なメモが格納されています。（開発者向け情報が主です）
- **pytest.ini**: pytestテストフレームワークの設定ファイルです。
- **requirements.txt**: プロジェクトの実行に必要なPythonパッケージの一覧を定義します。
- **ruff.toml**: Pythonのリンター/フォーマッターであるRuffの設定ファイルです。
- **src/**: プロジェクトの主要なソースコードを格納するディレクトリです。
  - **__init__.py**: Pythonパッケージであることを示すファイルです。
  - **__main__.py**: プログラムが直接実行された際のエントリポイントとなるスクリプトです。
  - **cat_file_watcher.py**: ファイル監視の全体的なロジックとコマンド実行フローを統括するメインスクリプトです。
  - **command_executor.py**: 設定に基づいて外部コマンドを実行する機能を提供します。
  - **config_loader.py**: TOML形式などの設定ファイルを読み込み、プログラムで利用可能な形式に変換します。
  - **config_validator.py**: 読み込んだ設定データの構造と内容が正しいかを検証します。
  - **error_logger.py**: 発生したエラーを適切にログに記録する機能を提供します。
  - **external_config_merger.py**: メイン設定ファイルと、そこから参照される外部設定ファイルを統合するロジックを扱います。
  - **file_monitor.py**: ファイルシステム上の特定のファイルやディレクトリの変更を効率的に監視するコアロジックを実装します。
  - **interval_parser.py**: "5s", "1m"のような文字列形式の時間間隔を、プログラムで扱える数値形式にパース（解析）します。
  - **process_detector.py**: 指定された名前のプロセスが現在システム上で実行中であるかを検出する機能を提供します。
  - **time_period_checker.py**: コマンド実行を特定の日時や時間帯に制限するための条件チェックを行います。
  - **timestamp_printer.py**: 現在の時刻を整形して出力する機能を提供します。
- **tests/**: プロジェクトのテストコードを格納するディレクトリです。
  - **test_basics.py**: プロジェクトの基本的な機能が正しく動作するかを検証するテストです。
  - **test_cat_file_watcher.py**: `cat_file_watcher.py`で実装されている主要なファイル監視機能に関するテストです。
  - **test_colorama.py**: ターミナル出力の色付けライブラリ`colorama`（もし使用されていれば）に関するテストです。
  - **test_command_logging.py**: コマンド実行のログ記録機能に関するテストです。
  - **test_command_suppression.py**: 特定の条件でコマンド実行を抑制する機能に関するテストです。
  - **test_commands_and_processes_sections.py**: 設定ファイル内の`commands`および`processes`セクションの正しい解析と動作に関するテストです。
  - **test_config_reload.py**: 実行中に設定が正しく再読み込みされるかに関するテストです。
  - **test_cwd.py**: コマンド実行時のカレントワーキングディレクトリ(CWD)の動作に関するテストです。
  - **test_directory_monitoring.py**: ファイルだけでなくディレクトリの変更監視機能に関するテストです。
  - **test_empty_filename.py**: 空のファイル名が指定された場合の挙動に関するテストです。
  - **test_error_logging.py**: エラーロギング機能が正しく動作するかに関するテストです。
  - **test_external_files.py**: 外部ファイルの取り扱い、特に外部設定のマージに関するテストです。
  - **test_interval_parser.py**: 時間間隔を解析するパーサーの機能に関するテストです。
  - **test_intervals.py**: 監視間隔の指定と動作に関するテストです。
  - **test_main_loop_interval.py**: メインの監視ループの実行間隔に関するテストです。
  - **test_multiple_empty_filenames.py**: 複数の空のファイル名が指定された場合の挙動に関するテストです。
  - **test_new_interval_format.py**: 新しい時間間隔フォーマットの対応に関するテストです。
  - **test_process_detection.py**: プロセス検出機能に関するテストです。
  - **test_suppression_logging.py**: 抑制されたコマンド実行が適切にログに記録されるかに関するテストです。
  - **test_terminate_if_process.py**: 特定のプロセスが実行中の場合に監視を終了する条件に関するテストです。
  - **test_time_periods.py**: 時間帯によるコマンド実行制限機能に関するテストです。
  - **test_timestamp.py**: タイムスタンプ出力機能に関するテストです。

## 関数詳細説明
- **main() (in `src/__main__.py`, `src/cat_file_watcher.py`)**: プログラムのエントリポイントで、設定のロード、ファイル監視ループの初期化と開始、全体の実行フローを管理します。
- **run_watcher() (in `src/cat_file_watcher.py`)**: 実際のファイル監視ロジックと、変更検知時のコマンド実行、各種条件判定（時間帯、プロセス検出など）を含むメインループを実行します。
- **execute_command(command_config) (in `src/command_executor.py`)**: 指定されたコマンド設定（コマンド文字列、実行ディレクトリ、環境変数など）に基づいて、外部のシェルコマンドを実行します。
- **load_config(path) (in `src/config_loader.py`)**: 指定されたファイルパスから設定ファイル（TOML形式を想定）を読み込み、Pythonのデータ構造に変換して返します。
- **validate_config(config_data) (in `src/config_validator.py`)**: 読み込んだ設定データのスキーマと値の妥当性を検証し、不正な設定があればエラーを報告します。
- **log_error(message, error_details) (in `src/error_logger.py`)**: 発生したエラーメッセージとその詳細情報を、標準エラー出力や設定されたログシステムに出力します。
- **merge_external_configs(main_config) (in `src/external_config_merger.py`)**: メイン設定ファイル内で参照されている可能性のある外部設定ファイルをロードし、それらの内容をメイン設定にマージします。
- **watch_files(paths, callback) (in `src/file_monitor.py`)**: 指定されたファイルパスまたはディレクトリパスの変更を継続的に監視し、変更が検知された際に登録されたコールバック関数を呼び出します。
- **get_file_status(path) (in `src/file_monitor.py`)**: 特定のファイルの現在の状態（例：最終更新タイムスタンプ、ファイルサイズなど）を取得し、変更検知のための比較に使用します。
- **parse_interval(interval_str) (in `src/interval_parser.py`)**: "10s" (10秒), "5m" (5分) のような時間間隔を表す文字列を解析し、対応する秒数などの数値に変換します。
- **is_process_running(process_name) (in `src/process_detector.py`)**: 指定された名前のプロセスが現在システム上で実行中であるかどうかをチェックし、真偽値を返します。
- **is_within_time_period(time_periods) (in `src/time_period_checker.py`)**: 現在時刻が、設定ファイルで定義された許可された時間帯のいずれかに含まれているかを判断します。
- **print_timestamp() (in `src/timestamp_printer.py`)**: 現在のタイムスタンプを整形された文字列として標準出力に出力します。
- **format_timestamp(dt) (in `src/timestamp_printer.py`)**: `datetime`オブジェクトを受け取り、特定のフォーマット（例: `YYYY-MM-DD HH:MM:SS`）で文字列に変換します。

## 関数呼び出し階層ツリー
```
関数呼び出し階層を分析できませんでした。

---
Generated at: 2025-10-17 07:02:44 JST

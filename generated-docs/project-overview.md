Last updated: 2025-10-30

# Project Overview

## プロジェクト概要
- 「cat-file-watcher」は、指定されたファイルの変更を自動で検知し、その変更に応じて任意のコマンドを実行するツールです。
- 開発者のワークフローを自動化し、手動での監視やコマンド実行の手間を削減することで、生産性向上を支援します。
- プロジェクト名にある「Cat」のように、目立たず静かにファイルの動きを監視し、必要なアクションをトリガーします。

## 技術スタック
- フロントエンド: 該当なし
- 音楽・オーディオ:
  - Tone.js: Web Audio APIを簡潔に扱うためのJavaScriptライブラリ。
  - Web Audio API: ウェブブラウザで高度な音声処理を行うための標準技術（Tone.jsを介して利用）。
  - MML (Music Macro Language): 音楽をテキストで記述するための記法パーサー。
- 開発ツール:
  - Node.js runtime: JavaScriptコードを実行するためのランタイム環境。
- テスト: 該当なし（ただし、`tests/` ディレクトリにPythonのテストコードが存在するため、pytestなどのPythonテストフレームワークが内部的に使用されている可能性があります）
- ビルドツール: 該当なし
- 言語機能: 該当なし
- 自動化・CI/CD:
  - GitHub Actions: コードの変更を検知して自動でビルド、テスト、デプロイなどのワークフローを実行するCI/CDサービス。以下のワークフローが含まれます:
    - プロジェクト要約自動生成: プロジェクトの情報を自動で要約するワークフロー。
    - Issue自動管理: 課題追跡システム（Issue）の管理を自動化するワークフロー。
    - README多言語翻訳: プロジェクトのREADMEドキュメントを多言語に自動翻訳するワークフロー。
    - i18n automation: 国際化（i18n）関連の自動化ワークフロー。
- 開発標準:
  - EditorConfig: 異なるエディタやIDE間で、コードのインデント、改行コード、エンコーディングなどの書式設定を統一するための設定ファイル。

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
  📖 101.md
  📖 103.md
  📖 105.md
  📖 107.md
  📖 109.md
  📖 11.md
  📖 111.md
  📖 113.md
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
  📄 test_empty_filename_messages.py
  📄 test_error_log_clarity.py
  📄 test_error_logging.py
  📄 test_external_files.py
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
- **.editorconfig**: 異なる開発環境（エディタ、IDE）間でのコードスタイル（インデント、エンコーディングなど）を統一するための設定ファイルです。
- **.gitignore**: Gitのバージョン管理から除外するファイルやディレクトリを指定するファイルです。
- **.pre-commit-config.yaml**: Gitコミット前に自動的に実行されるフック（コードフォーマット、リンティングなど）を設定するためのファイルです。
- **.vscode/**: Visual Studio Codeエディタ用の設定ディレクトリです。
  - **README.md**: VS Codeワークスペースに関する情報や設定の簡単な説明です。
  - **extensions.json**: このプロジェクトで推奨されるVS Code拡張機能のリストです。
  - **settings.json**: このVS Codeワークスペース固有の設定を定義するファイルです。
- **LICENSE**: プロジェクトの利用条件や配布に関するライセンス情報が記載されています。
- **README.ja.md, README.md**: プロジェクトの概要、インストール方法、使い方などを説明するドキュメント（日本語版と英語版）です。
- **_config.yml**: GitHub Pagesなどのサイトジェネレーターで利用される設定ファイルです。
- **dev-requirements.txt, requirements.txt**: Pythonプロジェクトの依存関係を定義するファイルで、それぞれ開発環境用と本番環境用のパッケージリストを記載しています。
- **examples/**: プロジェクトの設定ファイルの使用例が含まれるディレクトリです。
  - **config.example.toml**: cat-file-watcherの主要な設定項目を示すサンプル設定ファイルです。
  - **monitoring-group-example.toml**: 複数のファイルをグループ化して監視する設定のサンプルです。
- **generated-docs/**: GitHub Actionsなどによって自動生成されたドキュメントやレポートを格納するディレクトリです。
- **issue-notes/**: 開発過程で発生したIssue（課題）や検討事項に関するメモが格納されているディレクトリです。
- **pytest.ini**: Pythonのテストフレームワークであるpytestの設定ファイルです。
- **ruff.toml**: Pythonの高速なリンター・フォーマッターであるRuffの設定ファイルです。
- **src/**: プロジェクトの主要なソースコードが格納されているディレクトリです。
  - **__init__.py**: Pythonパッケージであることを示す初期化ファイルです。
  - **__main__.py**: プロジェクトがスクリプトとして直接実行された際のエントリポイントとなるファイルです。
  - **cat_file_watcher.py**: ファイル変更監視ツールのメインロジックを含むファイルで、全体の処理フローを管理します。
  - **command_executor.py**: ファイル変更を検知した際に実行される外部コマンドの実行ロジックを管理します。
  - **config_loader.py**: TOML形式などの設定ファイルを読み込み、プログラムで利用可能な形式に変換する機能を提供します。
  - **config_validator.py**: 読み込まれた設定ファイルの内容が正しく、必要な項目が全て揃っているかを検証します。
  - **error_logger.py**: プログラム実行中に発生したエラーを記録し、デバッグや問題解決に役立てるためのロギング機能を提供します。
  - **external_config_merger.py**: 外部に定義された設定ファイルを読み込み、メインの設定と統合（マージ）する機能を提供します。
  - **file_monitor.py**: 指定されたファイルのタイムスタンプや内容の変化を定期的に監視するコア機能です。
  - **interval_parser.py**: 監視間隔や時間指定など、時間に関する文字列をプログラムが理解できる形式に解析する機能です。
  - **process_detector.py**: 特定のプロセスが現在実行中であるかを検出し、その状態に基づいて処理を制御する機能を提供します。
  - **time_period_checker.py**: 特定の時間帯（例：営業時間内、夜間など）であるかを判定し、処理の実行可否を制御する機能です。
  - **timestamp_printer.py**: ログ出力やコンソール表示に、現在の時刻を示すタイムスタンプを付加する機能を提供します。
- **tests/**: プロジェクトの各種機能の単体テストや統合テストが記述されたファイル群です。各 `test_*.py` ファイルは特定のモジュールや機能のテストを担当します。

## 関数詳細説明
このプロジェクトの具体的な関数リストは提供されていませんが、`src/` ディレクトリ内のファイル名から、以下のような役割を持つ関数群が存在すると推測されます。各関数の引数と戻り値は一般的な設計に基づいた推測です。

- **`cat_file_watcher.py` 内の関数**:
    - `main()`: プログラムのエントリポイント。設定の読み込み、ファイル監視の初期化、メインループの開始などを担当します。
        - 引数: なし (またはコマンドライン引数)
        - 戻り値: なし
    - `start_monitoring(config)`: ファイル監視を開始し、監視ループを管理します。
        - 引数: `config` (設定オブジェクト): 監視対象ファイルや実行コマンドなどの情報を含む。
        - 戻り値: なし
    - `_watch_files(monitor_config)`: 実際のファイル変更を定期的にチェックし、変更があれば通知します。
        - 引数: `monitor_config` (監視設定): 監視対象の詳細情報。
        - 戻り値: なし

- **`command_executor.py` 内の関数**:
    - `execute_command(command, cwd=None)`: 指定されたコマンド文字列をサブプロセスとして実行します。
        - 引数: `command` (str): 実行するコマンド文字列。`cwd` (str, optional): コマンドを実行する作業ディレクトリ。
        - 戻り値: `tuple` (int, str, str): 終了コード、標準出力、標準エラー出力。
    - `run_subprocess(command_list, shell=False)`: コマンドリストを受け取り、より詳細なサブプロセス実行を制御します。
        - 引数: `command_list` (list[str]): コマンドと引数のリスト。`shell` (bool): シェル経由で実行するかどうか。
        - 戻り値: `subprocess.CompletedProcess` オブジェクト。

- **`config_loader.py` 内の関数**:
    - `load_config(file_path)`: 指定されたTOMLファイルパスから設定を読み込み、Pythonオブジェクトとして返します。
        - 引数: `file_path` (str): 設定ファイルのパス。
        - 戻り値: `dict` または `ConfigObject`: パースされた設定データ。
    - `parse_toml_file(file_path)`: TOML形式のファイルを解析し、その内容を辞書形式で返します。
        - 引数: `file_path` (str): TOMLファイルのパス。
        - 戻り値: `dict`: TOMLファイルの内容。

- **`file_monitor.py` 内の関数**:
    - `check_for_changes(file_path, last_timestamp)`: 指定ファイルの現在のタイムスタンプと前回のタイムスタンプを比較し、変更があったかを確認します。
        - 引数: `file_path` (str): 監視対象ファイルのパス。`last_timestamp` (float): 前回の変更タイムスタンプ。
        - 戻り値: `tuple` (bool, float): 変更があったか (True/False)、新しいタイムスタンプ。
    - `get_file_timestamp(file_path)`: 指定されたファイルの最終変更タイムスタンプを取得します。
        - 引数: `file_path` (str): ファイルのパス。
        - 戻り値: `float`: 最終変更タイムスタンプ（Unix時間）。

- **その他、各ファイルの主要な関数（推測）**:
    - **`config_validator.py`**: `validate_config(config)` (設定のスキーマ検証)
    - **`error_logger.py`**: `log_error(message, exception=None)` (エラーメッセージの記録)
    - **`external_config_merger.py`**: `merge_external_configs(main_config, external_paths)` (外部設定の読み込みと統合)
    - **`interval_parser.py`**: `parse_interval_string(interval_str)` (時間文字列を秒数に変換)
    - **`process_detector.py`**: `is_process_running(process_name)` (特定のプロセスが実行中か判定)
    - **`time_period_checker.py`**: `is_within_time_period(start_time_str, end_time_str)` (現在が指定時間帯内か判定)
    - **`timestamp_printer.py`**: `print_with_timestamp(message, color=None)` (タイムスタンプ付きでメッセージ出力)

## 関数呼び出し階層ツリー
```
関数呼び出し階層を分析できませんでした。

---
Generated at: 2025-10-30 07:02:20 JST

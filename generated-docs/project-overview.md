Last updated: 2026-03-03

# Project Overview

## プロジェクト概要
- ファイルのタイムスタンプ変更を監視し、指定されたファイルやディレクトリが更新された際にカスタムコマンドを実行します。
- 複数のファイルやディレクトリを同時に監視し、TOML設定ファイルを通じて柔軟な監視条件やコマンド実行オプションを定義できます。
- 軽量でありながら、プロセス抑制、時間帯指定、Windowsでのフォーカス非奪取など、様々なユースケースに対応する機能を備えています。

## 技術スタック
- フロントエンド: なし (CLIツールのため)
- 音楽・オーディオ: なし
- 開発ツール:
    - **Python**: プロジェクトの主要なプログラミング言語。
    - **pip**: Pythonパッケージのインストールと管理に使用されるツール。
    - **git**: バージョン管理システム。
    - **pytest**: Pythonアプリケーションのテストフレームワーク。
    - **Ruff**: 高速なPythonリンターおよびフォーマッター。
- テスト:
    - **pytest**: Pythonコードのテストを実行するために使用されます。
- ビルドツール: なし (Pythonスクリプトとして直接実行されるため、特定のビルドステップは不要)
- 言語機能:
    - **Python**: 高レベルで汎用的なプログラミング言語。
- 自動化・CI/CD:
    - **GitHub Actions**: リポジトリのREADME生成やテスト実行などの自動化フローに利用されています。
- 開発標準:
    - **Ruff**: コードの品質を維持し、一貫したコーディングスタイルを適用するために使用されます。

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
  📖 137.md
  📖 139.md
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
  📄 color_scheme.py
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
  📄 test_color_scheme_config.py
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
  📄 test_no_focus_validation.py
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
-   **`.editorconfig`**: 異なるエディタやIDE間で一貫したコーディングスタイルを維持するための設定ファイル。
-   **`.gitignore`**: Gitでバージョン管理しないファイルやディレクトリを指定するファイル。
-   **`.pre-commit-config.yaml`**: Gitのpre-commitフックで実行されるツール（Ruffなど）の設定ファイル。
-   **`.vscode/`**: Visual Studio Code用の設定ファイル群。
    -   `README.md`: `.vscode`ディレクトリに関する説明。
    -   `extensions.json`: 推奨されるVS Code拡張機能を定義するファイル。
    -   `settings.json`: ワークスペース固有のVS Code設定を定義するファイル。
-   **`LICENSE`**: プロジェクトのライセンス情報（MIT License）が記述されたファイル。
-   **`README.ja.md`**: プロジェクトの概要、使い方、設定などの情報を提供する日本語版のメインドキュメント。
-   **`README.md`**: プロジェクトの概要、使い方、設定などの情報を提供する英語版のメインドキュメント。
-   **`_config.yml`**: GitHub Pagesなどの設定ファイル（存在する場合）。
-   **`dev-requirements.txt`**: 開発時に必要なPythonパッケージ（Ruff、pytestなど）をリストアップしたファイル。
-   **`examples/`**: 設定ファイルの例や使用例を格納するディレクトリ。
    -   `config.example.toml`: プロジェクトの基本的な設定例を示すTOMLファイル。
    -   `monitoring-group-example.toml`: 複数の監視グループ設定の例を示すTOMLファイル。
-   **`generated-docs/`**: 自動生成されたドキュメントを格納するディレクトリ。
-   **`googled947dc864c270e07.html`**: Googleサイト認証用の空ファイル。
-   **`issue-notes/`**: GitHub Issuesに関連するメモや情報を格納するディレクトリ。
-   **`pytest.ini`**: pytestの動作をカスタマイズするための設定ファイル。
-   **`requirements.txt`**: プロジェクトの実行に必要なPythonパッケージをリストアップしたファイル。
-   **`ruff.toml`**: Ruffリンターおよびフォーマッターのルールを設定するファイル。
-   **`src/`**: プロジェクトのソースコードを格納するディレクトリ。
    -   `__init__.py`: Pythonパッケージであることを示す空ファイル。
    -   `__main__.py`: プロジェクトがモジュールとして実行された際のエントリポイント。CLI引数のパースとメイン処理の呼び出しを行います。
    -   `cat_file_watcher.py`: ファイル監視の主要ロジックとメインループを実装しているファイル。
    -   `color_scheme.py`: ターミナル出力の配色を管理・適用するためのロジックを提供します。
    -   `command_executor.py`: ファイル変更時に指定されたコマンドを実行するための処理を担当します。
    -   `config_loader.py`: TOML設定ファイルを読み込み、パースしてPythonオブジェクトに変換します。
    -   `config_validator.py`: 読み込まれたTOML設定の構造と内容を検証するロジックを含みます。
    -   `error_logger.py`: コマンド実行時のエラーやその他のエラーメッセージをログファイルに記録する機能を提供します。
    -   `external_config_merger.py`: 外部設定ファイル（例: `monitoring-group-example.toml`）をメイン設定にマージするロジック。
    -   `file_monitor.py`: 個々のファイルまたはディレクトリの変更タイムスタンプを監視し、変更を検出する役割を担います。
    -   `interval_parser.py`: "1s"や"2m"のような時間間隔文字列を秒数に変換するユーティリティ。
    -   `process_detector.py`: 指定されたプロセスが現在実行中であるかを検出し、コマンド抑制機能に利用されます。
    -   `time_period_checker.py`: 設定された時間帯（例: "09:00-17:00"）が現在時刻と一致するかをチェックするロジック。
    -   `timestamp_printer.py`: ターミナルにタイムスタンプ付きメッセージを出力するユーティリティ関数を提供します。
-   **`tests/`**: プロジェクトのテストコードを格納するディレクトリ。各ファイルは特定の機能やモジュールのテストを担当します。

## 関数詳細説明
-   `src/__main__.py`:
    -   `main()`: プログラムのエントリポイント。コマンドライン引数を解析し、`cat_file_watcher`のメイン監視ループを開始します。
-   `src/cat_file_watcher.py`:
    -   `run_watcher()`: ファイル監視のメインループを実行します。設定ファイルに基づいてファイルの変更を定期的にチェックし、対応するコマンドを実行します。
    -   `_load_and_validate_config()`: 設定ファイルを読み込み、バリデーションを実行します。
    -   `_process_file_change()`: ファイル変更が検出された際に、関連するコマンド実行ロジックをトリガーします。
-   `src/color_scheme.py`:
    -   `get_color_scheme()`: 設定に基づき、指定された配色スキーム（monokai, classic, カスタム色）を適用した色定義を返します。
    -   `print_color()`: 指定された色とメッセージでターミナルに出力します。
-   `src/command_executor.py`:
    -   `execute_command()`: 指定されたコマンドをサブプロセスとして実行します。`no_focus`オプションや作業ディレクトリの指定をサポートします。
    -   `_run_command_with_shell()`: シェル経由でコマンドを実行します。
    -   `_run_command_without_shell()`: シェルを使わずにコマンドを実行します。
-   `src/config_loader.py`:
    -   `load_config()`: 指定されたTOMLファイルから設定を読み込み、Pythonの辞書形式で返します。
    -   `merge_external_configs()`: 外部設定ファイルをメイン設定にマージします。
-   `src/config_validator.py`:
    -   `validate_config()`: 読み込まれた設定辞書が期待される構造とデータ型に準拠しているか検証します。
    -   `_validate_file_entry()`: 個々のファイル監視エントリの形式を検証します。
-   `src/error_logger.py`:
    -   `log_error()`: 発生したエラーの詳細（メッセージ、スタックトレースなど）を専用のエラーログファイルに記録します。
-   `src/file_monitor.py`:
    -   `check_for_changes()`: 監視対象のファイルまたはディレクトリの最終更新タイムスタンプをチェックし、前回の記録から変更があったかどうかを判断します。
    -   `update_timestamps()`: 監視対象のファイルの現在のタイムスタンプを記録します。
-   `src/interval_parser.py`:
    -   `parse_interval()`: "1s"や"5m"のような文字列形式の時間間隔を秒単位の数値に変換します。
-   `src/process_detector.py`:
    -   `is_process_running()`: 指定された正規表現パターンにマッチするプロセスが現在実行中であるかを検出します。
-   `src/time_period_checker.py`:
    -   `is_within_time_period()`: 現在時刻が設定された時間帯（例: "09:00-17:00"）内にあるかどうかを判断します。日をまたぐ時間帯もサポートします。
-   `src/timestamp_printer.py`:
    -   `print_timestamped_message()`: 現在のタイムスタンプを含むメッセージをコンソールに出力します。

## 関数呼び出し階層ツリー
```
関数呼び出し階層を分析できませんでした。

---
Generated at: 2026-03-03 07:05:15 JST

Last updated: 2026-03-04

# Project Overview

## プロジェクト概要
- ファイルの変更を監視し、変更が検知された際に指定されたコマンドを自動で実行するツールです。
- TOML形式の設定ファイルを通じて、監視対象のファイルやディレクトリ、実行するコマンド、監視間隔などを柔軟に設定できます。
- 軽量で使いやすく、複数のファイルやディレクトリの同時監視、特定のプロセス実行時のコマンド抑制、時間帯ごとの監視などの高度な機能を備えています。

## 技術スタック
- フロントエンド: 該当なし（本プロジェクトはCUIベースのバックエンドツールです）
- 音楽・オーディオ: 該当なし
- 開発ツール:
    - **Python**: プロジェクトの主要な開発言語です。
    - **pip**: Pythonパッケージのインストールと管理に使用されます。
    - **Git**: バージョン管理システムとして、ソースコードの管理とリポジトリのクローンに利用されます。
    - **VS Code (`.vscode/`)**: 開発環境としてVisual Studio Codeが推奨されており、その設定ファイルが含まれています。
    - **pre-commit**: コミット前にコード品質チェックなどのフックを自動実行するために使用されます。
- テスト:
    - **pytest**: Pythonコードの単体テストおよび統合テストに使用されるテストフレームワークです。
- ビルドツール:
    - **Pythonインタープリタ**: プロジェクトはPythonスクリプトとして直接実行されるため、特定のビルドツールは使用されていません。
- 言語機能:
    - **Python**: 主要なプログラミング言語です。
    - **TOML**: 設定ファイルの記述に利用される人間が読みやすいデータシリアライゼーション形式です。
- 自動化・CI/CD:
    - **GitHub Actions**: README.mdの自動生成（日本語版からの翻訳）などに利用されており、継続的インテグレーション・デリバリーの自動化に貢献しています。
- 開発標準:
    - **Ruff**: 高速なPythonリンターおよびフォーマッターとして、コード品質の維持とコーディングスタイルの統一に活用されています。
    - **.editorconfig**: 複数の開発者やエディタ間で、一貫したコーディングスタイルを強制するための設定ファイルです。

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
  📖 139.md
  📖 141.md
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
  📄 repo_updater.py
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
  📄 test_repo_updater.py
  📄 test_suppression_logging.py
  📄 test_terminate_if_process.py
  📄 test_terminate_if_window_title.py
  📄 test_terminate_message_color.py
  📄 test_time_periods.py
  📄 test_timestamp.py
  📄 test_timestamp_reset_on_reload.py
```

## ファイル詳細説明

-   **`.editorconfig`**: 異なるエディタやIDE間で一貫したコーディングスタイルを維持するための設定ファイルです。
-   **`.gitignore`**: Gitがバージョン管理の対象から除外するファイルやディレクトリを指定します。
-   **`.pre-commit-config.yaml`**: Gitのpre-commitフックを管理する`pre-commit`ツールの設定ファイルです。コード品質チェックなどを自動化するために使用されます。
-   **`.vscode/`**: Visual Studio Codeのワークスペース設定を格納するディレクトリです。
    -   **`README.md`**: VS Code関連の追加情報や設定方法を説明するドキュメントです。
    -   **`extensions.json`**: プロジェクト推奨のVS Code拡張機能をリストアップするファイルです。
    -   **`settings.json`**: プロジェクト固有のVS Code設定を定義するファイルです。
-   **`LICENSE`**: 本プロジェクトのライセンス情報（MIT License）を記載したファイルです。
-   **`README.ja.md`**: プロジェクトの日本語版説明ドキュメントです。
-   **`README.md`**: プロジェクトの英語版説明ドキュメントです。日本語版を元に自動生成されています。
-   **`_config.yml`**: GitHub Pagesなどの静的サイトジェネレータで使用される設定ファイルです。
-   **`dev-requirements.txt`**: 開発環境でのみ必要なPython依存パッケージ（例: テストツール、リンター）をリストアップするファイルです。
-   **`examples/`**: 設定ファイルの具体的な使用例を格納するディレクトリです。
    -   **`config.example.toml`**: `cat-file-watcher`の様々な設定オプションを示す主要なサンプル設定ファイルです。
    -   **`monitoring-group-example.toml`**: 複数のファイルをグループ化して監視する設定例を示唆するファイルです。
-   **`generated-docs/`**: 自動生成されたドキュメントを格納するディレクトリです。
    -   **`development-status.md`**: プロジェクトの開発状況に関するドキュメントです。
-   **`googled947dc864c270e07.html`**: Googleサイト認証用のHTMLファイルです。
-   **`issue-notes/`**: 過去のGitHub Issuesに関するメモや議論を格納するディレクトリです。
    -   **`139.md`, `141.md`, `62.md`, `71.md`, `78.md`**: 特定のissueに関する詳細なメモや背景情報を記録したMarkdownファイルです。
-   **`pytest.ini`**: Pythonのテストフレームワーク`pytest`の動作を設定するファイルです。
-   **`requirements.txt`**: プロジェクトの実行に必要なPython依存パッケージをリストアップするファイルです。
-   **`ruff.toml`**: PythonコードリンターRuffの設定ファイルです。
-   **`src/`**: プロジェクトの主要なソースコードを格納するディレクトリです。
    -   **`__init__.py`**: `src`ディレクトリがPythonパッケージであることを示します。
    -   **`__main__.py`**: `python -m src` の形式で実行された際に起動されるエントリポイントとなるファイルで、プログラムのメイン処理を開始します。
    -   **`cat_file_watcher.py`**: ファイル監視のメインロジックや、変更検知後の処理フローを管理する中心的なファイルです。
    -   **`color_scheme.py`**: ターミナル出力の配色に関するロジックを定義しています。
    -   **`command_executor.py`**: ファイル変更時に実行される外部コマンドの実行を抽象化し、通常実行やフォーカスを奪わない実行などを管理します。
    -   **`config_loader.py`**: TOML形式の設定ファイルを読み込み、パースしてプログラムで扱える形式に変換するロジックを担います。
    -   **`config_validator.py`**: 読み込んだ設定の内容が正しい構造と値を持っているかを検証するロジックを提供します。
    -   **`error_logger.py`**: コマンド実行時のエラーやその他の例外発生時に、詳細な情報をログファイルに記録する機能を提供します。
    -   **`external_config_merger.py`**: 外部の設定ファイルを結合する（あるいは、異なる設定を統合する）ロジックを処理します。
    -   **`file_monitor.py`**: 個々のファイルやディレクトリの最終更新タイムスタンプを監視し、変更を検知する低レベルな機能を提供します。
    -   **`interval_parser.py`**: "1s", "2m", "0.5s"といった時間文字列を適切な監視間隔（秒数など）に変換するロジックを扱います。
    -   **`process_detector.py`**: 特定の名前やパターンにマッチするプロセスが現在実行中であるかを検知するロジックを提供します（`suppress_if_process`機能用）。
    -   **`repo_updater.py`**: リポジトリの更新に関連する処理を扱うモジュールです。
    -   **`time_period_checker.py`**: 設定で定義された特定の時間帯（例: "09:00-17:00"）であるかどうかをチェックするロジックを提供します。
    -   **`timestamp_printer.py`**: タイムスタンプや関連情報を整形してコンソールに出力する機能を提供します。
-   **`tests/`**: プロジェクトの単体テストおよび統合テストコードを格納するディレクトリです。各`test_*.py`ファイルが特定の機能やモジュールのテストを担当します。

## 関数詳細説明
プロジェクト情報からは具体的な各関数の引数や戻り値までは読み取れませんが、ファイル名とプロジェクトの機能から主要な関数の役割を推測します。

-   **`src/__main__.py`**
    -   `main()`: プログラムのエントリポイント。設定の読み込み、ファイル監視の初期化、メインループの開始を orchestrate します。
-   **`src/cat_file_watcher.py`**
    -   `start_watching()`: ファイル監視を開始し、メインループを実行します。
    -   `check_for_changes()`: 監視対象ファイルの変更を定期的にチェックします。
    -   `run_command_on_change()`: ファイル変更が検知された際に、関連するコマンドを実行するための処理をトリガーします。
-   **`src/color_scheme.py`**
    -   `get_color_code()`: 指定された配色名やカスタムカラー設定に基づいて、ターミナル出力用のカラーコードを返します。
    -   `apply_color()`: 指定された文字列にカラーコードを適用し、色付きの文字列を生成します。
-   **`src/command_executor.py`**
    -   `execute_command(command, cwd=None, log_config=None, error_log_file=None)`: シェルコマンドを実行します。標準出力、標準エラー出力の処理、ログ記録、エラーハンドリングを含みます。
    -   `execute_command_no_focus(argv, cwd=None, error_log_file=None)`: Windows環境で、実行されたアプリケーションにフォーカスを奪わせずにコマンドを実行します。
-   **`src/config_loader.py`**
    -   `load_config(filename)`: 指定されたTOMLファイルから設定を読み込み、Pythonの辞書形式で返します。
    -   `parse_config_time_format(time_str)`: "1s"などの時間文字列を秒数に変換します。
-   **`src/config_validator.py`**
    -   `validate_config(config)`: 読み込まれた設定の構造と値が、期待される形式に従っているかを検証します。
    -   `_validate_file_entry(file_config)`: 各ファイルエントリーの設定が正しいかを検証する内部関数です。
-   **`src/error_logger.py`**
    -   `log_error(file_path, command, stdout, stderr, exception=None, stack_trace=None)`: コマンド実行エラーや例外の詳細をエラーログファイルに記録します。
-   **`src/external_config_merger.py`**
    -   `merge_configs(main_config, external_config)`: 複数の設定を結合し、優先順位に基づいて最終的な設定を構築します。
-   **`src/file_monitor.py`**
    -   `get_last_modified_timestamp(path)`: 指定されたファイルまたはディレクトリの最終更新タイムスタンプを取得します。
    -   `has_file_changed(path, known_timestamp)`: ファイルまたはディレクトリが前回の記録から変更されているかをチェックします。
-   **`src/interval_parser.py`**
    -   `parse_interval_string(interval_str)`: "1s", "2m", "3h"といった文字列から対応する秒数を計算して返します。
-   **`src/process_detector.py`**
    -   `is_process_running(pattern)`: 指定された正規表現パターンにマッチするプロセスが実行中であるかをチェックします。
    -   `get_matching_processes(pattern)`: 指定されたパターンにマッチする実行中のプロセス名をリストで返します。
-   **`src/repo_updater.py`**
    -   `update_repository()`: Gitリポジトリの更新（例: pull）を実行する機能を提供します。
-   **`src/time_period_checker.py`**
    -   `is_within_time_period(time_period_config)`: 現在時刻が設定された時間帯の範囲内であるかを判定します。
-   **`src/timestamp_printer.py`**
    -   `print_timestamped_message(message, color=None)`: 現在のタイムスタンプを含むメッセージを整形してコンソールに出力します。

## 関数呼び出し階層ツリー
```
関数呼び出し階層を分析できませんでした

---
Generated at: 2026-03-04 07:04:02 JST

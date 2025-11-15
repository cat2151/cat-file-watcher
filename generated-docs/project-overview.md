Last updated: 2025-11-16

# Project Overview

## プロジェクト概要
- ファイルのタイムスタンプ変更を監視し、更新検知時に指定されたコマンドを自動実行するツールです。
- TOML設定ファイルを通じて複数のファイルやディレクトリを同時に監視し、実行コマンドや監視間隔を柔軟に設定できます。
- 軽量で使いやすく、特定のプロセス実行中のコマンド抑制や、時間帯による監視の有効化など豊富な機能を備えています。

## 技術スタック
- フロントエンド: このプロジェクトはCLIツールであり、特定のフロントエンド技術は使用していません。
- 音楽・オーディオ: 音楽・オーディオ関連技術は使用していません。
- 開発ツール:
    - Git: ソースコードのバージョン管理に使用されています。
    - pip: Pythonパッケージのインストールと管理に使用されるツールです。
    - Ruff: Pythonコードのリンティングとフォーマットに使用され、コード品質と一貫性を保ちます。
    - pytest: Pythonアプリケーションのテストフレームワークで、機能テストの作成と実行に使用されます。
    - Visual Studio Code: 開発環境として推奨され、`.vscode` ディレクトリに設定ファイルが含まれています。
- テスト:
    - pytest: Pythonコードの単体テスト、統合テスト、およびシステムテストの実行に使用されます。
- ビルドツール:
    - 本プロジェクト自体はPythonスクリプトであり、専用のビルドツールは使用しません。設定例で`make build`や`gcc`が示されていますが、これらはユーザーが定義するコマンドの例です。
- 言語機能:
    - Python: プロジェクトの主要なプログラミング言語です。
    - TOML: 設定ファイルの記述形式として使用され、人間にとって読み書きしやすい構造化されたデータ形式を提供します。
- 自動化・CI/CD:
    - GitHub Actions: READMEの自動生成やテストの実行に利用され、継続的なインテグレーションとデリバリーをサポートします。
    - pre-commit: コミット前にコード品質チェック（Ruffなど）を自動実行するためのフレームワークです。
- 開発標準:
    - Ruff: コードのスタイルガイドを適用し、一貫性のあるコードフォーマットとリンティングを強制します。
    - EditorConfig: 複数のエディタやIDE間で一貫したコーディングスタイルを維持するための設定ファイルです。

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
  📖 117.md
  📖 119.md
  📖 121.md
  📖 123.md
  📖 125.md
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
  📄 test_no_focus.py
  📄 test_print_color_specification.py
  📄 test_process_detection.py
  📄 test_suppression_logging.py
  📄 test_terminate_if_process.py
  📄 test_terminate_message_color.py
  📄 test_time_periods.py
  📄 test_timestamp.py
```

## ファイル詳細説明
- **`.editorconfig`**: さまざまなエディタやIDE間でコードのインデントスタイル、文字コード、改行コードなどの書式設定を一貫させるための設定ファイルです。
- **`.gitignore`**: Gitがバージョン管理の対象外とするファイルやディレクトリのパターンを定義します。ビルド生成物や一時ファイルなどが含まれます。
- **`.pre-commit-config.yaml`**: Gitのpre-commitフックを管理するための設定ファイルで、コミット前にコードの自動整形やリンティングなどのチェックを実行します。
- **`.vscode/`**: Visual Studio Codeエディタ用の設定や推奨事項を格納するディレクトリです。
    - **`README.md`**: VS Code設定に関する補足説明が含まれている可能性があります。
    - **`extensions.json`**: プロジェクトで推奨されるVS Code拡張機能のリストを定義し、チーム開発における環境統一を助けます。
    - **`settings.json`**: ワークスペース固有のVS Code設定を定義し、コードスタイルや動作を調整します。
- **`LICENSE`**: プロジェクトのライセンス情報 (MIT License) が記載されており、ソフトウェアの使用、変更、配布に関する条件を定めます。
- **`README.ja.md`**: プロジェクトの日本語版概要、インストール方法、使い方、設定方法などを詳細に説明するドキュメントです。
- **`README.md`**: プロジェクトの英語版概要、インストール方法、使い方、設定方法などを詳細に説明するドキュメントです。
- **`_config.yml`**: GitHub Pagesなどで使用されるJekyllのサイト設定ファイルである可能性があります。
- **`dev-requirements.txt`**: 開発環境でのみ必要となるPythonパッケージ（テストツール、リンター、フォーマッターなど）のリストです。
- **`examples/`**: プロジェクトの設定ファイルや使用例を格納するディレクトリです。
    - **`config.example.toml`**: `cat-file-watcher` の設定方法を示す完全なサンプルTOML設定ファイルです。
    - **`monitoring-group-example.toml`**: 監視グループ機能の具体的な設定例を示すTOMLファイルです。
- **`generated-docs/`**: AIによって自動生成されたドキュメントを格納するディレクトリです。
- **`issue-notes/`**: GitHub Issuesに関するメモや詳細情報を格納するディレクトリです。
- **`pytest.ini`**: Pythonのテストフレームワークであるpytestの動作を設定するためのファイルです。
- **`requirements.txt`**: プロジェクトを実行するために最低限必要なPythonパッケージのリストです。
- **`ruff.toml`**: Ruffリンターおよびフォーマッターのルールや設定を定義するファイルです。
- **`src/`**: プロジェクトの主要なソースコードが格納されているディレクトリです。
    - **`__init__.py`**: `src` ディレクトリがPythonパッケージであることを示し、パッケージの初期化処理を記述する場合があります。
    - **`__main__.py`**: `python -m src` コマンドでプロジェクトを実行した際のエントリポイントとなるファイルです。
    - **`cat_file_watcher.py`**: ファイル変更監視のメインロジックを実装し、設定の読み込み、ファイル監視、コマンド実行の調整を行います。
    - **`command_executor.py`**: ファイル変更検知時に実行される外部コマンドの処理を担当します。ログ記録、エラーハンドリング、ノンブロッキング実行などを制御します。
    - **`config_loader.py`**: TOML形式の設定ファイルを読み込み、パースしてアプリケーションが利用できるデータ構造に変換します。
    - **`config_validator.py`**: 読み込まれた設定ファイルの構造と値が正当であるかを検証し、不適切な設定を検出します。
    - **`error_logger.py`**: コマンド実行エラーやその他のシステムエラーを特定のログファイルに記録する機能を提供します。
    - **`external_config_merger.py`**: 複数の設定ファイルが存在する場合に、それらを適切に結合するロジックを実装します。
    - **`file_monitor.py`**: 個々のファイルやディレクトリのタイムスタンプ変更を検知し、変更イベントをトリガーする役割を担います。
    - **`interval_parser.py`**: "1s", "2m"といった時間表記文字列を、プログラムが処理できる秒数に変換する機能を提供します。
    - **`process_detector.py`**: 特定のプロセスが現在システムで実行中であるかを検出するためのロジックを提供します。
    - **`time_period_checker.py`**: 設定された時間帯（例: 9:00-17:00）に基づいて、現在時刻がその時間帯内にあるかを判断します。
    - **`timestamp_printer.py`**: ログ出力などの際に、タイムスタンプを読みやすい形式で整形して表示する機能を提供します。
- **`tests/`**: プロジェクトの機能を検証するためのテストコードが格納されているディレクトリです。各`test_*.py`ファイルが特定の機能に対するテストケースを含みます。

## 関数詳細説明
プロジェクト情報に具体的な関数のシグネチャや実装が提供されていないため、詳細な関数情報は提供できません。一般的なPythonプロジェクトの構造とファイル名から推測される主要な機能ブロックと、それに伴う代表的な関数を以下に記述します。

- `src/__main__.py`:
    - **`main()`**: プログラムのエントリポイントとなる関数。コマンドライン引数のパース、設定の読み込み、`CatFileWatcher`の初期化と実行ループ開始を担います。
- `src/cat_file_watcher.py`:
    - **`CatFileWatcher.__init__(self, config)`**: ウォッチャーの初期化関数。設定を受け取り、ファイルモニターやコマンド実行器などのコンポーネントをセットアップします。
    - **`CatFileWatcher.run(self)`**: メインの監視ループを実行する関数。ファイル変更を定期的にチェックし、変更があれば対応するコマンドをトリガーします。
    - **`CatFileWatcher._check_file_changes(self)`**: 監視対象ファイルのタイムスタンプをチェックし、変更があったファイルを特定します。
- `src/command_executor.py`:
    - **`execute_command(command, cwd=None, no_focus=False, enable_log=False, log_file=None, error_log_file=None)`**: 指定されたシェルコマンドを実行する関数。作業ディレクトリの変更、Windowsでのフォーカス制御、コマンド実行ログとエラーログの記録を行います。
- `src/config_loader.py`:
    - **`load_config(filename)`**: 指定されたTOMLファイルから設定を読み込み、Pythonの辞書形式で返却する関数。ファイルパスの解決やファイルが存在しない場合のハンドリングも行います。
- `src/config_validator.py`:
    - **`validate_config(config)`**: 読み込まれた設定辞書が、プロジェクトの要件に沿った正しい形式と値を持っているかを検証する関数。無効な設定に対してはエラーを発生させます。
- `src/error_logger.py`:
    - **`log_error(filepath, command, stderr, exit_code, stack_trace=None)`**: コマンド実行時のエラー詳細やスタックトレースを、指定されたエラーログファイルに記録する関数。
- `src/file_monitor.py`:
    - **`FileMonitor.__init__(self, path, interval_seconds, time_period_name=None)`**: 個別のファイルまたはディレクトリの監視インスタンスを初期化します。
    - **`FileMonitor.has_changed(self)`**: 監視対象のファイルまたはディレクトリのタイムスタンプが前回のチェック以降に変更されたかを確認する関数。
- `src/interval_parser.py`:
    - **`parse_interval(interval_string)`**: "1s", "0.5m", "2h"などの文字列形式の時間間隔を、秒単位の浮動小数点数に変換する関数。
- `src/process_detector.py`:
    - **`is_process_running(pattern)`**: 指定された正規表現パターンにマッチするプロセスが現在システムで実行中であるかをチェックする関数。
- `src/time_period_checker.py`:
    - **`is_within_time_period(current_time, start_time_str, end_time_str)`**: 現在時刻が定義された開始時刻と終了時刻の範囲内にあるかを確認する関数。日をまたぐ時間帯も考慮します。
- `src/timestamp_printer.py`:
    - **`get_formatted_timestamp()`**: 現在時刻を特定のフォーマット（例: `YYYY-MM-DD HH:MM:SS`）の文字列で取得する関数。

## 関数呼び出し階層ツリー
```

---
Generated at: 2025-11-16 07:01:55 JST

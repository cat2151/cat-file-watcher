Last updated: 2025-12-06

# Project Overview

## プロジェクト概要
- ファイル変更を監視し、指定されたコマンドを自動実行する汎用ツールです。
- TOML形式の設定ファイルを使用し、複数のファイルやディレクトリと実行コマンドを柔軟に定義できます。
- 軽量で使いやすく、特にWindows環境でコマンド実行時にフォーカスを奪わない機能も提供します。

## 技術スタック
- フロントエンド: なし (本プロジェクトはCUIベースのツールです)
- 音楽・オーディオ: なし
- 開発ツール:
    - Git: ソースコードのバージョン管理とリポジトリ操作に使用します。
    - pip: Pythonパッケージの依存関係管理とインストールに使用します。
    - pytest: Pythonで書かれたテストコードの実行フレームワークです。
    - Ruff: Pythonコードのリンティング（構文チェック）とフォーマット（コード整形）を高速に行うツールです。
    - GitHub Actions: コードの変更があった際に自動でテストを実行したり、ドキュメントを生成したりするCI/CD（継続的インテグレーション/継続的デリバリー）プラットフォームです。
    - TOML: 設定ファイルを記述するためのシンプルで人間が読みやすいデータ形式です。
    - Visual Studio Code: `.vscode`ディレクトリが存在するため、開発において推奨されるエディタ環境です。
- テスト:
    - pytest: プロジェクトの自動テストを記述し、実行するためのPythonテスティングフレームワークです。
- ビルドツール:
    - pip: Pythonプロジェクトの依存関係をインストールし、実行環境を構築するために使用されます。
    - make (例示): `make build`といったコマンド例から、開発者がカスタムスクリプトやタスクを自動化するために利用する可能性があります。
- 言語機能:
    - Python: プロジェクトの主要なプログラミング言語です。
- 自動化・CI/CD:
    - GitHub Actions: コードの変更をトリガーとして、テストの実行、ドキュメントの自動生成、その他の自動化タスクを実行します。
- 開発標準:
    - Ruff: コードの品質と一貫性を保つため、リンティングとフォーマットのルールを適用します。

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
  📄 test_terminate_if_window_title.py
  📄 test_terminate_message_color.py
  📄 test_time_periods.py
  📄 test_timestamp.py
```

## ファイル詳細説明
- `.editorconfig`: 異なる開発環境やエディタ間でコードスタイル（インデント、改行コードなど）の一貫性を保つための設定ファイルです。
- `.gitignore`: Gitのバージョン管理から除外するファイルやディレクトリを指定します。例えば、コンパイル生成物や一時ファイルなどが含まれます。
- `.pre-commit-config.yaml`: Gitの`pre-commit`フックで実行されるツールの設定ファイルです。コードをコミットする前に、Ruffのようなリンターやフォーマッターを自動実行して品質をチェックします。
- `.vscode/`: Visual Studio Codeエディタのワークスペース固有の設定を格納するディレクトリです。
    - `README.md`: VS Code環境に関する追加情報やメモです。
    - `extensions.json`: プロジェクトで推奨されるVS Code拡張機能のリストです。
    - `settings.json`: VS Codeのワークスペース設定（フォーマットルール、リンター設定など）です。
- `LICENSE`: プロジェクトがMIT Licenseで配布されていることを示すライセンス情報ファイルです。
- `README.ja.md`: プロジェクトの日本語版説明ドキュメントです。
- `README.md`: プロジェクトの英語版説明ドキュメントです。日本語版から自動生成されています。
- `_config.yml`: GitHub Pagesでプロジェクトのウェブサイトを公開する際に使用されるJekyllの設定ファイルです。
- `dev-requirements.txt`: 開発中に必要となるPythonパッケージ（Ruffやpytestなど）の一覧を定義しています。
- `examples/`: プロジェクトの設定ファイルの具体例を格納するディレクトリです。
    - `config.example.toml`: `cat-file-watcher`の主要な設定オプションと使用方法を示す包括的なTOML設定例です。
    - `monitoring-group-example.toml`: 監視対象をグループ化するような高度な設定の例を示すTOML設定ファイルです。
- `generated-docs/`: AIエージェントによって生成されたドキュメントや、開発状況に関するレポートなどを格納するディレクトリです。
- `googled947dc864c270e07.html`: Googleのサイト所有権確認のために使用される単一行のHTMLファイルです。
- `issue-notes/`: 開発中の特定のイシューに関するメモや、AIエージェントとのやり取りの記録を格納するディレクトリです。
- `pytest.ini`: `pytest`テストフレームワークの挙動をカスタマイズするための設定ファイルです。
- `requirements.txt`: プロジェクトを実行するために最低限必要なPythonパッケージの一覧を定義しています。
- `ruff.toml`: `Ruff`リンターおよびフォーマッターの具体的なルールや設定を定義するファイルです。
- `src/`: プロジェクトの主要なPythonソースコードが格納されているディレクトリです。
    - `__init__.py`: `src`ディレクトリがPythonパッケージであることを示します。
    - `__main__.py`: パッケージが`python -m src`のようにスクリプトとして実行された際の最初のエントリポイントです。コマンドライン引数の解析とメイン処理の開始を担当します。
    - `cat_file_watcher.py`: ファイル監視ツールの中心的なロジックを実装しています。設定の読み込み、監視対象ファイルの管理、変更検知、および関連コマンドの実行調整を行います。
    - `command_executor.py`: ファイル変更時に指定されたシェルコマンドを実行する役割を担います。プロセスの起動、出力の処理、タイムアウト管理、そしてWindows環境でのフォーカス抑制機能を提供します。
    - `config_loader.py`: TOML形式の設定ファイルを読み込み、パースして、アプリケーションが利用できるデータ構造に変換します。設定ファイルの自動再読み込み機能も担当します。
    - `config_validator.py`: 読み込まれた設定ファイルの構造と値が、期待される形式とルールに準拠しているかを検証します。
    - `error_logger.py`: コマンド実行時のエラーやアプリケーション内部で発生した例外情報を、指定されたログファイルに記録する機能を提供します。
    - `external_config_merger.py`: 外部で定義された設定ファイル（例えば、監視対象リストなど）をメインの設定にマージするためのロジックを提供します。
    - `file_monitor.py`: 個々のファイルまたはディレクトリの監視ロジックをカプセル化します。タイムスタンプの比較、変更の検知、および監視間隔の管理を行います。
    - `interval_parser.py`: "1s", "2m", "0.5s"といった時間指定文字列を、アプリケーションで処理可能な秒数に変換するユーティリティです。
    - `process_detector.py`: 指定された正規表現にマッチするプロセスが現在システム上で実行中であるかを検出し、コマンド実行の抑制などに利用されます。
    - `time_period_checker.py`: 設定ファイルで定義された時間帯（例: "09:00-17:00"）に基づいて、現在時刻がその時間帯内にあるかを判定するロジックを提供します。
    - `timestamp_printer.py`: メッセージにタイムスタンプを付加して、コンソールやログファイルに整形して出力するためのユーティリティ関数を提供します。
- `tests/`: プロジェクトの各機能に対するテストコードが格納されているディレクトリです。
    - `test_*.py`: `pytest`によって実行される、プロジェクトの様々な側面をテストするためのファイル群です。

## 関数詳細説明
- `src/__main__.py`:
    - `main()`: このスクリプトが直接実行されたときのエントリポイントです。コマンドライン引数を解析し、ファイルウォッチャーのメインループを開始します。
- `src/cat_file_watcher.py`:
    - `run_watcher()`: ファイル監視のコアとなるメインループを管理します。設定の再読み込み、監視対象ファイルのポーリング、および検出された変更に基づくコマンド実行を調整します。
    - `_check_for_file_changes()`: 監視対象の各ファイルやディレクトリのタイムスタンプ変更を内部的にチェックし、必要に応じて関連するコマンド実行をトリガーします。
- `src/command_executor.py`:
    - `execute_command()`: 指定されたシェルコマンドをシステム上で実行します。コマンドの出力処理、エラー検出、タイムアウト処理、Windows特有のフォーカス抑制オプションなどを扱います。
- `src/config_loader.py`:
    - `load_config()`: 指定されたTOMLファイルから設定を読み込み、Pythonのデータ構造に変換します。
    - `reload_config_if_changed()`: 設定ファイルの変更を監視し、ファイルの内容が更新された場合に設定を自動的に再読み込みします。
- `src/config_validator.py`:
    - `validate_config()`: 読み込まれた設定オブジェクトの構造と値の妥当性を検証し、無効な設定がないかを確認します。
- `src/error_logger.py`:
    - `log_error()`: アプリケーション内で発生したエラーメッセージや例外情報を、指定されたエラーログファイルに記録します。
- `src/file_monitor.py`:
    - `FileMonitor` クラス: 特定のファイルまたはディレクトリの監視状態を管理するオブジェクトです。
    - `check_for_change()`: `FileMonitor`オブジェクトに属するメソッドで、監視対象のファイルまたはディレクトリの変更（主にタイムスタンプ）をチェックします。
- `src/interval_parser.py`:
    - `parse_interval_string()`: "1s" (1秒) や "2m" (2分), "0.5s" (0.5秒) のような文字列形式の時間間隔を、アプリケーションが処理できる秒数に変換します。
- `src/process_detector.py`:
    - `is_process_running()`: 指定された正規表現パターンにマッチするプロセスが、現在システム上で実行中であるかを検出する機能を提供します。
- `src/time_period_checker.py`:
    - `is_in_time_period()`: 現在時刻が、設定ファイルで定義された特定の時間帯（例：ビジネスアワー、夜間シフト）内に含まれるかどうかを判断します。
- `src/timestamp_printer.py`:
    - `print_timestamped_message()`: メッセージに現在時刻のタイムスタンプを付加し、視認しやすい形式でコンソールやログに出力します。

## 関数呼び出し階層ツリー
```
関数呼び出し階層を分析できませんでした

---
Generated at: 2025-12-06 07:02:00 JST

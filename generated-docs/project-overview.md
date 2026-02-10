Last updated: 2026-02-11

# Project Overview

## プロジェクト概要
- このプロジェクトは、ファイルやディレクトリの変更をリアルタイムで監視し、変更が検知された際に指定されたコマンドを自動実行するツールです。
- TOML形式の設定ファイルを通じて、監視対象のパス、実行コマンド、監視間隔、特定の条件でのコマンド抑制など、柔軟な設定が可能です。
- 軽量で使いやすく、Windows環境でのフォーカスを奪わないコマンド実行機能など、特定のユースケースにも対応した設計が特徴です。

## 技術スタック
- フロントエンド: このプロジェクトはコマンドラインインターフェース (CLI) ツールであり、特定のフロントエンド技術は使用していません。
- 音楽・オーディオ: 音楽・オーディオ関連の技術は使用していません。
- 開発ツール:
    - Ruff: Pythonコードのリンティングとフォーマットに使用され、コード品質と一貫性を保ちます。
    - pytest: Pythonアプリケーションのテストフレームワークで、機能の正確性を検証します。
    - VS Code (settings.json, extensions.json): 開発環境の設定ファイルであり、開発体験を統一・最適化します。
- テスト:
    - pytest: Pythonで記述されたテストコードを実行し、機能の検証を行います。
- ビルドツール:
    - pip: Pythonパッケージのインストールと管理に使用されます。
- 言語機能:
    - Python: プロジェクトの主要な開発言語であり、スクリプトの実行、ファイル監視、コマンド実行などの機能を提供します。
    - TOML: 設定ファイルの記述に用いられるデータフォーマットで、人間が読みやすく、柔軟な設定を可能にします。
- 自動化・CI/CD:
    - GitHub Actions: (READMEより推測) 自動テスト、ドキュメント生成、翻訳などのCI/CDパイプラインを構築します。
- 開発標準:
    - .editorconfig: 異なるエディタやIDE間で一貫したコーディングスタイルを維持するための設定ファイルです。
    - .pre-commit-config.yaml: コミット前にコード品質チェックやフォーマットを自動実行するための設定です。

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
  📖 131.md
  📖 133.md
  📖 135.md
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
- **`.editorconfig`**: 異なるエディタ間での一貫したコードスタイル（インデント、改行コードなど）を強制するための設定ファイルです。
- **`.gitignore`**: Gitがバージョン管理の対象外とするファイルやディレクトリ（例: ログファイル、一時ファイル、依存関係のディレクトリ）を指定します。
- **`.pre-commit-config.yaml`**: Gitのpre-commitフックを設定し、コードコミット前にRuffによるリンティングやフォーマットなどを自動実行するための設定ファイルです。
- **`.vscode/`**: Visual Studio Codeエディタ用の設定ファイル群を格納するディレクトリです。
    - **`README.md`**: VS Codeの拡張機能や設定に関する説明です。
    - **`extensions.json`**: プロジェクト開発で推奨されるVS Code拡張機能をリストアップします。
    - **`settings.json`**: VS Codeのワークスペース固有の設定を定義し、開発環境を統一します。
- **`LICENSE`**: プロジェクトのライセンス情報（MIT License）を記載したファイルで、ソフトウェアの使用、変更、配布に関する条件を示します。
- **`README.ja.md`**: プロジェクトの概要、インストール方法、使用方法、設定、機能などについて日本語で詳細に説明したメインドキュメントです。
- **`README.md`**: プロジェクトの概要、インストール方法、使用方法、設定、機能などについて英語で詳細に説明したメインドキュメントです。`README.ja.md`を元に自動生成されます。
- **`_config.yml`**: GitHub Pagesなどの静的サイトジェネレーターの設定ファイルである可能性があります。
- **`dev-requirements.txt`**: プロジェクトの開発環境で必要なPythonパッケージ（Ruff, pytestなど、実行時には不要なもの）をリストアップしたファイルです。
- **`examples/`**: 設定ファイルの具体的な使用例を含むディレクトリです。
    - **`config.example.toml`**: さまざまなユースケースに対応する設定例が記載されたTOMLファイルです。
    - **`monitoring-group-example.toml`**: 複数のファイルをグループ化して監視するような、より複雑な設定例が含まれる可能性があります。
- **`generated-docs/`**: AIによって生成されたドキュメントや、開発状況レポートなどが格納されるディレクトリです。
- **`googled947dc864c270e07.html`**: Googleサイト認証用のファイルで、ウェブサイトの所有権確認に使用されます。
- **`issue-notes/`**: 開発中の特定のIssueに関連するメモや情報、議論の履歴などがMarkdown形式で格納されたディレクトリです。
- **`pytest.ini`**: pytestの設定ファイルで、テストの挙動やオプションを定義します。
- **`requirements.txt`**: プロジェクトの実行に必要なPythonパッケージをリストアップしたファイルです。
- **`ruff.toml`**: Ruffリンターおよびフォーマッターの設定ファイルで、コードのスタイルと品質に関するルールを定義します。
- **`src/`**: プロジェクトの主要なソースコードを格納するディレクトリです。
    - **`__init__.py`**: `src`ディレクトリがPythonパッケージであることを示すファイルです。
    - **`__main__.py`**: `python -m src`のようにパッケージが直接実行されたときに呼び出されるエントリポイントとなるファイルです。
    - **`cat_file_watcher.py`**: ファイル監視ツールのメインロジックを含むコアファイルで、監視ループや設定のリロードなどを管理します。
    - **`color_scheme.py`**: ターミナル出力の配色を管理するロジックが含まれており、ユーザーが配色をカスタマイズできるようにします。
    - **`command_executor.py`**: ファイル変更時に実行される外部コマンドの処理ロジックを担当し、コマンドの実行、出力の処理、エラーハンドリングを行います。
    - **`config_loader.py`**: TOML形式の設定ファイルを読み込み、パースしてPythonのデータ構造に変換する役割を持ちます。
    - **`config_validator.py`**: 読み込んだ設定の内容が、定義されたスキーマやルールに則って正しいか検証するロジックを提供します。
    - **`error_logger.py`**: コマンド実行時のエラーやアプリケーションエラーを記録するロジックを担当し、ログファイルへの書き込みなどを行います。
    - **`external_config_merger.py`**: 外部設定ファイルの読み込みや、既存の設定への結合に関連するロジックを持つ可能性があります。
    - **`file_monitor.py`**: ファイルやディレクトリのタイムスタンプ変更を監視する具体的なメカニズムを実装し、変更イベントを検出します。
    - **`interval_parser.py`**: "1s"（1秒）、"2m"（2分）のような時間フォーマット文字列を解析し、プログラムが扱える秒数に変換するロジックです。
    - **`process_detector.py`**: 特定のプロセスが現在実行中であるかを検出し、コマンド抑制機能（例: エディタが起動中はコマンドを実行しない）に利用されます。
    - **`time_period_checker.py`**: 定義された時間帯（例: 営業時間、夜間シフト）に基づいて、コマンドの実行が現在許可されているかを判断するロジックです。
    - **`timestamp_printer.py`**: 監視イベントやコマンド実行イベントに関するタイムスタンプを整形し、ターミナルやログファイルに出力する機能を提供します。
- **`tests/`**: プロジェクトのテストコードを格納するディレクトリです。各`test_*.py`ファイルは、特定の機能やモジュールに対する単体テストや統合テストを含み、プロジェクトの品質を保証します。

## 関数詳細説明
現状では、プロジェクト内の具体的な関数名、引数、戻り値、機能の詳細を自動で抽出できる情報が提供されていません。通常、このセクションでは各Pythonファイルの主要な関数について、その役割、期待される引数、返却される値、そして実行される具体的な処理内容を説明します。

## 関数呼び出し階層ツリー
```
関数呼び出し階層を分析できませんでした

---
Generated at: 2026-02-11 07:11:59 JST

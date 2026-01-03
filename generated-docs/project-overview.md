Last updated: 2026-01-04

# Project Overview

## プロジェクト概要
- このツールは、ファイルのタイムスタンプ変更を監視し、更新を検知すると設定されたコマンドを自動で実行します。
- 複数のファイルやディレクトリを同時に監視でき、TOML形式の設定ファイルにより柔軟なコマンド実行条件を定義可能です。
- 軽量で使いやすく、特定の時間帯や実行中プロセスに応じたコマンド抑制など、高度な自動化要件に対応します。

## 技術スタック
- フロントエンド: 該当なし（本プロジェクトはコマンドラインツールであり、ユーザーインターフェースを持ちません。）
- 音楽・オーディオ: 該当なし
- 開発ツール:
    - **Git**: ソースコードのバージョン管理に使用されます。
    - **Ruff**: Pythonコードのリンティングとフォーマットを自動化し、コード品質と一貫性を保ちます。
    - **pytest**: Pythonアプリケーションのテストフレームワークであり、機能の検証と品質保証のために使用されます。
    - **VS Code**: 開発環境としてVisual Studio Codeが使用されており、設定ファイル（`.vscode/`）が存在します。
- テスト:
    - **pytest**: Pythonコードの単体テストおよび結合テストを実行するための主要なフレームワークです。
- ビルドツール: 該当なし（本プロジェクトはPythonスクリプトであり、通常意味でのビルドプロセスは持ちません。）
- 言語機能:
    - **Python**: プロジェクト全体の主要なプログラミング言語です。
    - **TOML**: 設定ファイル形式として使用されており、設定ファイルの読み込み・解析に利用されます。
    - **colorama**: （テストファイルから推測）ターミナル出力に色付けを行い、ユーザーへの視認性を高めるために使用される可能性があります。
- 自動化・CI/CD:
    - **GitHub Actions**: リポジトリの各種自動化ワークフロー、例えばテスト実行、ドキュメント生成、翻訳などに利用されます。
- 開発標準:
    - **Ruff**: コードのスタイルガイドと品質チェックを強制します。
    - **.editorconfig**: 異なるエディタやIDE間で一貫したコードスタイルを維持するための設定ファイルです。

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
- **`.editorconfig`**: さまざまなエディタやIDE間でコードのスタイル（インデント、改行コードなど）の一貫性を維持するための設定ファイルです。
- **`.gitignore`**: Gitがバージョン管理の対象から外すファイルやディレクトリを指定します。
- **`.pre-commit-config.yaml`**: Gitのpre-commitフックを定義し、コミット前にコードの自動チェック（リンティング、フォーマットなど）を実行します。
- **`.vscode/`**: Visual Studio Codeエディタ用の設定ファイルが含まれるディレクトリです。
    - **`README.md`**: VS Codeディレクトリに関する説明または指示。
    - **`extensions.json`**: プロジェクト推奨のVS Code拡張機能リスト。
    - **`settings.json`**: プロジェクト固有のVS Code設定。
- **`LICENSE`**: 本プロジェクトのソフトウェアライセンス情報（MIT License）が記述されています。
- **`README.ja.md`**: プロジェクトの概要、使い方、設定などの情報が日本語で記述された主要なドキュメントです。
- **`README.md`**: `README.ja.md`の英語版で、GitHub Actionsによって自動生成されます。
- **`_config.yml`**: GitHub Pagesなどのサイト設定ファイルとして利用されることが多いですが、本プロジェクトでの具体的な用途はプロジェクト情報からは不明です。
- **`dev-requirements.txt`**: 開発環境で必要となるPythonの依存パッケージ（例: Ruff, pytestなど）がリストされています。
- **`examples/`**: サンプルとして用意されたTOML設定ファイルが含まれるディレクトリです。
    - **`config.example.toml`**: さまざまな設定オプションを使った設定例を提供します。
    - **`monitoring-group-example.toml`**: 監視グループ機能の例を示す設定ファイル（詳細不明だが、拡張機能の可能性）。
- **`generated-docs/`**: AIによって生成された開発状況などのドキュメントが格納されるディレクトリです。
- **`googled947dc864c270e07.html`**: Googleのサイト所有者確認などで使用されるHTMLファイルです。本プロジェクトでは特定のサービス連携のために配置されている可能性があります。
- **`issue-notes/`**: 過去のGitHub Issueに関するメモやAIが生成した情報が格納されるディレクトリです。
- **`pytest.ini`**: Pythonのテストフレームワークであるpytestの設定ファイルです。
- **`requirements.txt`**: 本プロジェクトの実行環境で必要となるPythonの依存パッケージがリストされています。
- **`ruff.toml`**: コード品質ツールRuffの設定ファイルであり、リンティングやフォーマットのルールを定義します。
- **`src/`**: プロジェクトのコアロジックを含むPythonソースコードが格納されているディレクトリです。
    - **`__init__.py`**: `src`ディレクトリがPythonパッケージであることを示します。
    - **`__main__.py`**: `python -m src`のようにモジュールとして実行された際のエントリーポイントです。
    - **`cat_file_watcher.py`**: ファイル監視ツールの中心的なロジックを含み、設定の読み込み、監視ループの開始、コマンド実行の調整などを行います。
    - **`command_executor.py`**: ファイル変更が検知された際に、指定されたシェルコマンドを実行する役割を担います。ログ記録やエラー処理も担当します。
    - **`config_loader.py`**: TOML形式の設定ファイルを読み込み、解析して、プログラムで利用可能なPythonオブジェクトに変換します。
    - **`config_validator.py`**: 読み込まれた設定ファイルの構造と値が正しいかどうかを検証し、不正な設定を検出します。
    - **`error_logger.py`**: コマンド実行中に発生したエラーや例外を捕捉し、指定されたエラーログファイルに記録します。
    - **`external_config_merger.py`**: 外部の設定ファイルをマージする機能（もしあれば）を管理するモジュール。
    - **`file_monitor.py`**: 指定されたファイルやディレクトリの最終更新タイムスタンプを定期的にチェックし、変更を検出する主要なロジックを提供します。
    - **`interval_parser.py`**: "1s", "2m"といった時間文字列を、監視間隔として使用できる秒数に変換する機能を提供します。
    - **`process_detector.py`**: `suppress_if_process`設定に基づいて、特定のプロセスが実行中であるかを検出する機能を提供します。
    - **`time_period_checker.py`**: `time_period`設定に基づいて、現在時刻が定義された特定の時間帯内にあるかをチェックする機能を提供します。
    - **`timestamp_printer.py`**: ログやデバッグのために、タイムスタンプなどの情報を整形してコンソールに出力する機能を提供します。
- **`tests/`**: プロジェクトのコードの信頼性を保証するためのテストスクリプトが格納されているディレクトリです。各`test_*.py`ファイルは特定の機能やモジュールに対するテストを含みます。

## 関数詳細説明
プロジェクト情報から具体的な関数名は特定できませんでしたが、`src`ディレクトリ内の各モジュールが担う役割に基づき、主要な機能を持つであろう関数は以下の通りと推測されます。

- **`cat_file_watcher.py`**:
    - **`run_watcher()`**: メインのファイル監視ループを開始し、設定の再読み込み、ファイル変更の検出、コマンド実行の調整など、ツール全体のライフサイクルを管理します。
- **`command_executor.py`**:
    - **`execute_command()`**: 指定されたシェルコマンドを新しいプロセスとして実行します。コマンドの引数、作業ディレクトリ、ログ記録、エラー処理、`no_focus`オプションの適用などを処理します。
- **`config_loader.py`**:
    - **`load_config()`**: 指定されたTOMLファイルから設定データを読み込み、それをPythonの辞書形式で返します。設定の解析と、必要に応じて外部設定ファイルのロードも担当します。
- **`config_validator.py`**:
    - **`validate_config()`**: 読み込まれた設定データが、必須フィールドの存在や値の形式など、定義されたルールに従っているかを確認し、不正な設定に対してエラーを報告します。
- **`error_logger.py`**:
    - **`log_error()`**: コマンド実行の失敗時や予期せぬエラーが発生した場合に、エラーメッセージ、スタックトレース、関連情報を指定されたエラーログファイルに記録します。
- **`file_monitor.py`**:
    - **`monitor_files()`**: 登録された各ファイルやディレクトリの最終更新タイムスタンプを定期的に取得し、前回のチェック時と比較して変更があったかを検出します。
- **`interval_parser.py`**:
    - **`parse_interval()`**: "1s", "0.5m", "2h"などの人間が読める時間文字列を、プログラムで利用可能な秒数に変換します。
- **`process_detector.py`**:
    - **`is_process_running()`**: 指定された正規表現パターンにマッチするプロセスが現在システム上で実行中であるかをチェックします。
- **`time_period_checker.py`**:
    - **`is_within_time_period()`**: 現在の時刻が、設定ファイルで定義された特定の時間帯（例: "09:00-17:00"）内に収まっているかを判定します。
- **`timestamp_printer.py`**:
    - **`print_timestamped_message()`**: 指定されたメッセージに現在のタイムスタンプを付加してコンソールに出力し、実行状況を視覚的に追跡しやすくします。

## 関数呼び出し階層ツリー
```
提供された情報では関数呼び出し階層を分析できませんでした。そのため、具体的なツリー構造は提示できません。
```

---
Generated at: 2026-01-04 07:01:54 JST

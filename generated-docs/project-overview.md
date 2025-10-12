Last updated: 2025-10-13

# Project Overview

## プロジェクト概要
- このツールは、指定されたファイルやディレクトリの変更をリアルタイムで監視します。
- 変更が検知されると、事前に設定されたコマンドやスクリプトを自動的に実行します。
- 開発ワークフローの自動化、テストのトリガー、特定のイベントに基づくアクション実行に利用できます。

## 技術スタック
- フロントエンド: CLIツールとして機能するため、特に関連するフロントエンド技術は使用されていません。
- 音楽・オーディオ:
    - Tone.js: Web Audio APIを抽象化した音声ライブラリです（プロジェクトの主要機能であるファイル監視とは直接関係ありませんが、情報として含まれています）。
    - Web Audio API: ブラウザで高度な音声処理を行うためのAPIです（Tone.js経由で利用される可能性があります）。
    - MML (Music Macro Language): 音楽をテキストで記述するための言語パーサーです（同上）。
- 開発ツール:
    - Node.js runtime: JavaScriptの実行環境です（Pythonプロジェクトですが、補助的なツールやビルドプロセスなどで間接的に利用されている可能性があります）。
    - Python: プロジェクトの主要な実装言語です。
- テスト:
    - Pytest: Pythonでテストコードを記述し実行するための、広く利用されているテストフレームワークです。
- ビルドツール:
    - pip: Pythonパッケージのインストールと管理を行うための標準的なツールです。
    - Ruff: Pythonコードのフォーマットとリンティングを高速に行うツールです。
- 言語機能:
    - Python: 高レベルで汎用的なプログラミング言語であり、このプロジェクトの全ての主要ロジックがPythonで記述されています。
- 自動化・CI/CD:
    - GitHub Actions: コードの変更を検知し、テストの実行、ドキュメントの自動生成、多言語翻訳などのCI/CDパイプラインを自動化します。
        - プロジェクト要約自動生成: プロジェクトの概要を自動で生成します。
        - Issue自動管理: Issueのライフサイクルを自動で管理します。
        - README多言語翻訳: READMEファイルを複数の言語に自動翻訳します。
        - i18n automation: 国際化（i18n）関連の自動翻訳ワークフローを実行します。
- 開発標準:
    - EditorConfig: 異なるエディタやIDEを使用する開発者間で、インデントスタイルや改行コードなどの基本的なコードスタイルを統一するための設定ファイルです。

## ファイル階層ツリー
```
📄 .editorconfig
📄 .gitignore
📁 .vscode/
  📖 README.md
  📊 extensions.json
  📊 settings.json
📄 =0.6.0
📄 LICENSE
📖 README.ja.md
📖 README.md
📄 dev-requirements.txt
📁 examples/
  📄 config.example.toml
  📄 monitoring-group-example.toml
📁 generated-docs/
📁 issue-notes/
  📖 11.md
  📖 13.md
  📖 15.md
  📖 16-refactoring-summary.md
  📖 16.md
  📖 19-refactoring-summary.md
  📖 19.md
  📖 21.md
  📖 23.md
  📖 24.md
  📖 26.md
  📖 27.md
  📖 30.md
  📖 32.md
  📖 33.md
  📖 35.md
  📖 37.md
  📖 39.md
  📖 41.md
  📖 43.md
  📖 45.md
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
  📖 71.md
  📖 72.md
  📖 74.md
  📖 76.md
  📖 78.md
  📖 9.md
📄 pytest.ini
📄 requirements.txt
📄 ruff.toml
📁 src/
  📄 __init__.py
  📄 __main__.py
  📄 cat_file_watcher.py
  📄 command_executor.py
  📄 config_loader.py
  📄 error_logger.py
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
-   `.editorconfig`: プロジェクト全体でコードのスタイル（インデント、エンコーディングなど）を統一するための設定ファイルです。
-   `.gitignore`: Gitのバージョン管理から除外するファイルやディレクトリを指定します。
-   `.vscode/`: Visual Studio Codeエディタ用の設定や推奨事項を格納するディレクトリです。
    -   `README.md`: `.vscode`ディレクトリの目的や内容に関する説明です。
    -   `extensions.json`: プロジェクト推奨のVS Code拡張機能をリストアップします。
    -   `settings.json`: プロジェクト固有のVS Code設定（例: リンターの設定）を定義します。
-   `=0.6.0`: (具体的な用途は不明ですが、バージョン管理や特定の依存関係に関するファイルかもしれません。)
-   `LICENSE`: プロジェクトの配布および使用に関するライセンス情報が記載されています。
-   `README.ja.md`: プロジェクトの日本語版の説明書です。
-   `README.md`: プロジェクトの英語版のメイン説明書です。
-   `dev-requirements.txt`: 開発環境でのみ必要なPythonパッケージ（テストツールなど）がリストされています。
-   `examples/`: プロジェクトの設定ファイルのサンプルが格納されているディレクトリです。
    -   `config.example.toml`: メインの設定ファイル（監視対象、実行コマンドなど）のテンプレートです。
    -   `monitoring-group-example.toml`: 複数の監視グループを設定する際の例です。
-   `generated-docs/`: GitHub Actionsなどによって自動生成されたドキュメントやレポートが格納されます。
-   `issue-notes/`: 開発中に記録されたGitHub Issuesに関連するメモや詳細情報が、issue番号ごとにファイルとして格納されています。
-   `pytest.ini`: Pythonのテストフレームワーク`pytest`の設定ファイルです。
-   `requirements.txt`: プロジェクトを実行するために必要なPythonパッケージがリストされています。
-   `ruff.toml`: Pythonの高速なリンター兼フォーマッターである`Ruff`の設定ファイルです。
-   `src/`: プロジェクトの主要なPythonソースコードが格納されているディレクトリです。
    -   `__init__.py`: `src`ディレクトリがPythonパッケージとして認識されるための初期化ファイルです。
    -   `__main__.py`: このプロジェクトをコマンドラインから直接実行する際のエントリーポイントとなるスクリプトです。
    -   `cat_file_watcher.py`: ファイルやディレクトリの変更を監視し、イベントを処理するコアロジックを実装しています。
    -   `command_executor.py`: ファイル変更イベントに応じて、外部のシェルコマンドを実行する機能を提供します。
    -   `config_loader.py`: `toml`形式の設定ファイルを読み込み、パースしてアプリケーションで使用可能な形式に変換します。
    -   `error_logger.py`: エラー発生時に詳細な情報を記録し、デバッグやトラブルシューティングを支援するロギング機能を提供します。
    -   `interval_parser.py`: 設定ファイルで指定された監視間隔（例: "5s", "1m"）を解析し、適切な数値に変換します。
    -   `process_detector.py`: 特定の名前を持つプロセスがシステム上で実行中であるかを検出する機能を提供します。
    -   `time_period_checker.py`: コマンドの実行を指定された時間帯に限定するためのロジックを実装しています。
    -   `timestamp_printer.py`: ログメッセージや出力に現在のタイムスタンプを付加するユーティリティ機能を提供します。
-   `tests/`: プロジェクトの各機能に対する単体テストや統合テストが格納されているディレクトリです。
    -   `test_basics.py`: プロジェクトの基本的な動作に関するテストケース。
    -   `test_cat_file_watcher.py`: `cat_file_watcher.py`モジュールの主要機能に関するテスト。
    -   `test_colorama.py`: （おそらく色付き出力に使われる）`colorama`ライブラリの利用に関するテスト。
    -   `test_command_logging.py`: コマンド実行のロギング機能に関するテスト。
    -   `test_command_suppression.py`: コマンド実行の抑制（条件付き実行）機能に関するテスト。
    -   `test_commands_and_processes_sections.py`: 設定ファイルの`[commands]`および`[processes]`セクションの解析と動作に関するテスト。
    -   `test_config_reload.py`: 実行中の設定ファイル再読み込み機能に関するテスト。
    -   `test_cwd.py`: コマンド実行時のカレントワーキングディレクトリ(CWD)の動作に関するテスト。
    -   `test_directory_monitoring.py`: ディレクトリ全体を監視する機能に関するテスト。
    -   `test_empty_filename.py`: 空のファイル名が設定された場合の挙動に関するテスト。
    -   `test_error_logging.py`: エラーロギング機能の動作に関するテスト。
    -   `test_external_files.py`: 外部ファイルとの連携（設定ファイルなど）に関するテスト。
    -   `test_interval_parser.py`: `interval_parser.py`モジュールのテスト。
    -   `test_intervals.py`: 監視間隔の設定と動作に関するテスト。
    -   `test_main_loop_interval.py`: メイン監視ループの間隔設定に関するテスト。
    -   `test_multiple_empty_filenames.py`: 複数の空のファイル名設定に関するテスト。
    -   `test_new_interval_format.py`: 新しい監視間隔フォーマットのサポートに関するテスト。
    -   `test_process_detection.py`: `process_detector.py`モジュールのテスト。
    -   `test_suppression_logging.py`: コマンド実行抑制時のロギングに関するテスト。
    -   `test_terminate_if_process.py`: 特定のプロセスが実行中にプログラムを終了させる機能に関するテスト。
    -   `test_time_periods.py`: `time_period_checker.py`モジュールのテスト。
    -   `test_timestamp.py`: `timestamp_printer.py`モジュールのテスト。

## 関数詳細説明
このプロジェクトでは、以下の主要な関数が各モジュールで提供されていると推測されます。具体的な引数や戻り値は提供された情報からは特定できないため、一般的な機能と役割を説明します。

-   **`src/__main__.py`**
    -   `main()`: プログラムのエントリーポイント。設定の読み込み、ファイルウォッチャーの初期化、監視ループの開始を調整します。
        -   役割: コマンドラインツールとしての起動処理全般を管理します。
        -   引数: 通常はコマンドライン引数（設定ファイルのパスなど）を受け取ります。
        -   戻り値: プログラムの終了コード。

-   **`src/cat_file_watcher.py`**
    -   `start_watching(config)`: 指定された設定（監視対象パス、間隔など）に基づいてファイル監視を開始します。
        -   役割: メインのファイル監視ループを実行し、変更を検知した際に適切なハンドラを呼び出します。
        -   引数: `config` (dict) - 監視設定を含む辞書。
        -   戻り値: なし（通常、無限ループで実行）。
    -   `_on_file_change(file_path)`: ファイル変更イベントが発生した際に内部的に呼び出されるコールバック関数。
        -   役割: 変更されたファイルパスを受け取り、コマンド実行などの後続処理をトリガーします。
        -   引数: `file_path` (str) - 変更が検知されたファイルのパス。
        -   戻り値: なし。

-   **`src/command_executor.py`**
    -   `execute_command(command, cwd=None)`: 指定されたシェルコマンドを新しいプロセスとして実行します。
        -   役割: 外部コマンドの実行と、その標準出力・エラー出力の処理を行います。
        -   引数: `command` (str) - 実行するシェルコマンド文字列。`cwd` (str, optional) - コマンドを実行する作業ディレクトリ。
        -   戻り値: コマンドの実行結果（成功/失敗、出力など）。
    -   `check_and_execute_commands(config, changed_file)`: 変更されたファイルに基づき、設定されたコマンドを実行すべきかを判断し、実行します。
        -   役割: 設定、時間帯、プロセス状況などの条件を評価し、適切なコマンドを選択して実行します。
        -   引数: `config` (dict) - 監視設定。`changed_file` (str) - 変更が検知されたファイルパス。
        -   戻り値: なし。

-   **`src/config_loader.py`**
    -   `load_config(config_path)`: 指定されたパスからTOML形式の設定ファイルを読み込み、Pythonの辞書として返します。
        -   役割: 設定ファイルのI/Oと基本的なパースを行います。
        -   引数: `config_path` (str) - 設定ファイルのパス。
        -   戻り値: `dict` - パースされた設定データ。
    -   `validate_config(config)`: 読み込んだ設定辞書が期待される構造と有効な値を持っているか検証します。
        -   役割: 設定のエラーチェックとデフォルト値の適用を行います。
        -   引数: `config` (dict) - ロードされた設定データ。
        -   戻り値: `dict` - 検証され、場合によっては補完された設定データ。

-   **`src/error_logger.py`**
    -   `log_error(message, error=None)`: エラーメッセージとオプションで例外オブジェクトをログに記録します。
        -   役割: プログラム内で発生したエラーを記録し、デバッグ情報を提供します。
        -   引数: `message` (str) - エラーの説明。`error` (Exception, optional) - 関連する例外オブジェクト。
        -   戻り値: なし。

-   **`src/interval_parser.py`**
    -   `parse_interval(interval_str)`: "5s", "1m"のような文字列形式の監視間隔を、数値（秒）に変換します。
        -   役割: ユーザーフレンドリーな時間指定をプログラムで扱える形式に変換します。
        -   引数: `interval_str` (str) - 時間指定文字列。
        -   戻り値: `int` - 秒単位の間隔。

-   **`src/process_detector.py`**
    -   `is_process_running(process_name)`: 指定された名前のプロセスが現在システム上で実行中であるかを判定します。
        -   役割: コマンド実行条件の一部として、特定のプロセス状況を確認します。
        -   引数: `process_name` (str) - 検出したいプロセスの名前またはキーワード。
        -   戻り値: `bool` - プロセスが実行中であれば`True`、そうでなければ`False`。

-   **`src/time_period_checker.py`**
    -   `is_within_time_period(time_periods)`: 現在時刻が、設定で指定された複数の時間帯（例: "9:00-17:00"）のいずれかに含まれているかを判定します。
        -   役割: 特定の時間帯でのみコマンド実行を許可する条件チェックを行います。
        -   引数: `time_periods` (list of str) - "HH:MM-HH:MM"形式の時間帯リスト。
        -   戻り値: `bool` - 現在時刻が有効な時間帯内であれば`True`、そうでなければ`False`。

-   **`src/timestamp_printer.py`**
    -   `print_with_timestamp(message)`: 指定されたメッセージの先頭に現在の日時を付加して標準出力に表示します。
        -   役割: ログやコンソール出力の視認性を高めます。
        -   引数: `message` (str) - 表示する文字列。
        -   戻り値: なし。

## 関数呼び出し階層ツリー
```
関数呼び出し階層を分析できませんでした。

---
Generated at: 2025-10-13 07:02:26 JST

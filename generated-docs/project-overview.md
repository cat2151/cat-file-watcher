Last updated: 2025-10-14

# Project Overview

## プロジェクト概要
- ファイルシステム上の特定のファイルやディレクトリの変更を効率的に監視します。
- 変更が検知された際に、あらかじめ設定されたコマンドを自動で実行します。
- 開発作業の自動化、定期的な処理のトリガー、あるいは特定のイベント応答に利用できるツールです。

## 技術スタック
- フロントエンド: N/A (直接的なWeb UIは提供していません)
- 音楽・オーディオ:
    - Tone.js: Web Audio APIを抽象化し、ブラウザ上で高度な音声処理を行うためのJavaScriptライブラリ。
    - Web Audio API: ブラウザに内蔵された音声処理用のAPIで、Tone.jsを通じて利用されます。
    - MML (Music Macro Language): 音楽をテキストで記述するための記法パーサー。
- 開発ツール:
    - Node.js runtime: JavaScriptの実行環境で、開発スクリプトや一部のツール実行に利用されます。
- テスト: N/A (テストフレームワークの具体的な記載はありませんが、`pytest.ini`からPythonのPytestが使用されていると推測できます。)
- ビルドツール: N/A
- 言語機能: N/A (主要言語はPythonと推測されますが、特定の言語機能は明記されていません。)
- 自動化・CI/CD:
    - GitHub Actions: コードの変更をトリガーに自動テスト、ドキュメント生成、翻訳などを行うCI/CDワークフロー。
        - プロジェクト要約自動生成: プロジェクトの概要を自動で生成します。
        - Issue自動管理: GitHub Issueのライフサイクルを自動で管理します。
        - README多言語翻訳: READMEファイルを複数の言語に自動翻訳します。
        - i18n automation: 国際化（i18n）関連の自動処理を行います。
- 開発標準:
    - EditorConfig: 異なるIDEやエディタ間でコードスタイルの一貫性を保つための設定ファイル。

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
- **.editorconfig**: 複数の開発者や異なるエディタ間で、インデントスタイル、文字コード、改行コードなど、コードの基本的な書式設定を一貫させるための設定ファイル。
- **.gitignore**: Gitのバージョン管理から除外するファイルやディレクトリを指定するファイル。ビルド生成物や一時ファイルなどが含まれます。
- **.pre-commit-config.yaml**: Gitのpre-commitフックで実行される処理を設定するファイル。コミット前にコードのフォーマットチェックやリンティングなどを自動で行います。
- **.vscode/**: Visual Studio Codeエディタのワークスペース固有の設定を格納するディレクトリ。
    - **.vscode/README.md**: VS Codeユーザー向けの追加情報や推奨設定が記述されている可能性があります。
    - **.vscode/extensions.json**: このプロジェクトで推奨されるVS Code拡張機能のリスト。
    - **.vscode/settings.json**: VS Codeのワークスペース固有の設定（例: 言語設定、フォーマット設定）。
- **LICENSE**: このプロジェクトのソフトウェアライセンス情報。利用条件が記載されています。
- **README.ja.md**: プロジェクトの概要、使い方、機能などを日本語で説明する主要なドキュメント。
- **README.md**: プロジェクトの概要、使い方、機能などを英語で説明する主要なドキュメント。
- **dev-requirements.txt**: 開発環境で必要となるPythonライブラリのリスト。テストツールやリンターなどが含まれます。
- **examples/**: プロジェクトの設定ファイルや使用例が格納されているディレクトリ。
    - **examples/config.example.toml**: メインの設定ファイル（`cat-file-watcher`の動作設定）の例。
    - **examples/monitoring-group-example.toml**: 監視対象のファイルグループとその設定の例。
- **generated-docs/**: 自動生成されたドキュメントを格納するディレクトリ。開発状況レポートなどが含まれる可能性があります。
- **issue-notes/**: 開発中の特定のGitHub Issueに関連するメモや詳細な調査結果を格納するディレクトリ。
- **pytest.ini**: Pythonのテストフレームワークであるpytestの設定ファイル。テストの実行方法やオプションを定義します。
- **requirements.txt**: プロジェクトの実行に必要なPythonライブラリのリスト。
- **ruff.toml**: Pythonの高速なLinterおよびFormatterであるRuffの設定ファイル。コードの品質と一貫性を保つためのルールを定義します。
- **src/**: プロジェクトの主要なソースコードを格納するディレクトリ。
    - **src/__init__.py**: Pythonパッケージとして`src`ディレクトリを初期化するためのファイル。
    - **src/__main__.py**: `python -m src`のようにパッケージを直接実行した際のプログラムのエントリーポイント。
    - **src/cat_file_watcher.py**: ファイルやディレクトリの変更を監視し、指定されたコマンドを実行するメインロジックを含むファイル。
    - **src/command_executor.py**: 監視対象の変更をトリガーとして実行される外部コマンドを安全に実行するための機能を提供します。
    - **src/config_loader.py**: TOML形式などの設定ファイルを読み込み、プログラムが使用できる形式に解析する機能を提供します。
    - **src/error_logger.py**: プログラム実行中に発生したエラーを記録し、適切な方法で報告するためのロギング機能を提供します。
    - **src/interval_parser.py**: 監視間隔や時間指定などの文字列を解析し、数値形式に変換するユーティリティ機能を提供します。
    - **src/process_detector.py**: 特定の名前のプロセスが現在実行中であるかを検出し、その状態に基づいてアクションを決定する機能を提供します。
    - **src/time_period_checker.py**: 設定された時間帯（例: 業務時間内）にプログラムの動作を制限または調整するための時間チェック機能を提供します。
    - **src/timestamp_printer.py**: イベントの発生時刻などを分かりやすい形式で出力するためのタイムスタンプ生成・表示機能を提供します。
- **tests/**: プロジェクトのテストコードを格納するディレクトリ。
    - `test_*.py` ファイル群: 各モジュールや機能の単体テスト、統合テストなどが記述されています。

## 関数詳細説明
プロジェクト情報から具体的な関数の引数や戻り値の詳細を直接抽出することはできませんでしたが、各ファイルが担当する主要な機能に基づき、関連するであろう関数とその役割を以下に示します。

- **`src/cat_file_watcher.py`**
    - `watch_files(config)`:
        - 役割: 指定された設定情報に基づき、ファイルやディレクトリの変更を継続的に監視するメインループを実行します。
        - 機能: 監視対象の変更を検知し、必要に応じて`command_executor`を呼び出す。
- **`src/command_executor.py`**
    - `execute_command(command_args, cwd=None)`:
        - 役割: 指定されたコマンドとその引数を新しいサブプロセスとして実行します。
        - 機能: コマンドの実行、ワーキングディレクトリの指定、実行結果のハンドリング。
- **`src/config_loader.py`**
    - `load_config(config_path)`:
        - 役割: 指定されたパスにある設定ファイル（例: TOML）を読み込み、パースして設定オブジェクトを返します。
        - 機能: ファイルの読み込み、TOML形式の解析、設定値のバリデーション。
- **`src/error_logger.py`**
    - `log_error(message, level='error')`:
        - 役割: 指定されたエラーメッセージをログに出力します。
        - 機能: エラーメッセージのフォーマット、ログファイルやコンソールへの出力、ログレベルの管理。
- **`src/interval_parser.py`**
    - `parse_interval(interval_str)`:
        - 役割: "10s", "5m" のような文字列形式の時間間隔を、秒数などの数値形式に解析して変換します。
        - 機能: 文字列解析、時間単位（秒、分など）の変換。
- **`src/process_detector.py`**
    - `is_process_running(process_name)`:
        - 役割: 指定された名前のプロセスがシステム上で現在実行中であるかを検出します。
        - 機能: 実行中プロセスのリスト取得、プロセス名との比較。
- **`src/time_period_checker.py`**
    - `is_within_time_period(time_periods)`:
        - 役割: 現在の時刻が、設定された特定の時間帯の範囲内にあるかを判定します。
        - 機能: 現在時刻の取得、設定された開始・終了時刻との比較。
- **`src/timestamp_printer.py`**
    - `print_timestamp()`:
        - 役割: 現在のタイムスタンプ（日時）を整形して標準出力に表示します。
        - 機能: 現在時刻の取得、フォーマット指定、出力。

## 関数呼び出し階層ツリー
```
関数呼び出し階層を分析できませんでした

---
Generated at: 2025-10-14 07:02:17 JST

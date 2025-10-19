Last updated: 2025-10-20

# Project Overview

## プロジェクト概要
- ファイルシステムの変更をリアルタイムで監視し、特定の条件に基づいてコマンドを自動実行するツールです。
- 開発プロセスの自動化、タスクの効率化、および特定のイベントへの自動応答を目的としています。
- AIによるドキュメント生成や多言語対応のREADMEを備え、継続的な改善が行われています。

## 技術スタック
- フロントエンド: [該当なし] (プロジェクトは主にバックエンド/CLIツールとして機能します)
- 音楽・オーディオ:
    - Tone.js: Web Audio APIを抽象化し、ブラウザ上で高度な音声処理やシンセサイザー機能を可能にするJavaScriptライブラリです。
    - Web Audio API: ウェブブラウザ上で高度な音声処理を行うためのAPIです。Tone.jsを介して利用されます。
    - MML (Music Macro Language): 音楽をテキストベースで記述するための記法パーサーで、音楽生成に関連する可能性があります。
- 開発ツール:
    - Node.js runtime: JavaScriptコードを実行するためのオープンソースのサーバーサイド実行環境です。
- テスト: [プロジェクト情報に特定のテストフレームワークの記載はありませんが、`pytest.ini`が存在するためPythonのPytestが使用されている可能性が高いです。]
- ビルドツール: [該当なし]
- 言語機能: [該当なし]
- 自動化・CI/CD:
    - GitHub Actions: コードの変更を検知してテストの実行、ドキュメントの自動生成、多言語翻訳などのCI/CDパイプラインを自動化します。
        - プロジェクト要約自動生成: プロジェクトの概要を自動的に生成するワークフローです。
        - Issue自動管理: GitHub Issueのライフサイクル管理を自動化するワークフローです。
        - README多言語翻訳: プロジェクトのREADMEファイルを複数の言語に自動翻訳するワークフローです。
        - i18n automation: 国際化 (i18n) に関連する自動化ワークフローです。
- 開発標準:
    - EditorConfig: 異なるIDEやエディタ間で、インデントスタイル、文字コードなどのコーディングスタイルを統一するための設定ファイルです。

## ファイル階層ツリー
```
.editorconfig
.gitignore
.pre-commit-config.yaml
.vscode/
  README.md
  extensions.json
  settings.json
LICENSE
README.ja.md
README.md
_config.yml
dev-requirements.txt
examples/
  config.example.toml
  monitoring-group-example.toml
generated-docs/
issue-notes/
  101.md
  103.md
  105.md
  11.md
  16-refactoring-summary.md
  19-refactoring-summary.md
  21.md
  24.md
  26.md
  27.md
  30.md
  33.md
  35.md
  37.md
  39.md
  41.md
  43.md
  46.md
  48.md
  50.md
  52.md
  54.md
  56.md
  57.md
  58.md
  62.md
  63.md
  65.md
  67.md
  69.md
  71-investigation-report.md
  71.md
  72.md
  74.md
  76.md
  78.md
  79-investigation-report.md
  79.md
  81.md
  83-completion.md
  85.md
  87.md
  89.md
  91.md
  93.md
  95.md
  97.md
  99.md
pytest.ini
requirements.txt
ruff.toml
src/
  __init__.py
  __main__.py
  cat_file_watcher.py
  command_executor.py
  config_loader.py
  config_validator.py
  error_logger.py
  external_config_merger.py
  file_monitor.py
  interval_parser.py
  process_detector.py
  time_period_checker.py
  timestamp_printer.py
tests/
  test_basics.py
  test_cat_file_watcher.py
  test_colorama.py
  test_command_logging.py
  test_command_suppression.py
  test_commands_and_processes_sections.py
  test_config_reload.py
  test_cwd.py
  test_directory_monitoring.py
  test_empty_filename.py
  test_error_log_clarity.py
  test_error_logging.py
  test_external_files.py
  test_interval_parser.py
  test_intervals.py
  test_main_loop_interval.py
  test_multiple_empty_filenames.py
  test_new_interval_format.py
  test_process_detection.py
  test_suppression_logging.py
  test_terminate_if_process.py
  test_time_periods.py
  test_timestamp.py
```

## ファイル詳細説明
- **.editorconfig**: エディタのコードスタイル設定を定義し、プロジェクト全体のコードの一貫性を保ちます。
- **.gitignore**: Gitがバージョン管理の対象外とするファイルやディレクトリを指定します。
- **.pre-commit-config.yaml**: pre-commitフックの設定ファイルで、コミット前にコードの品質チェックを自動実行します。
- **.vscode/**: Visual Studio Codeのワークスペース設定を格納するディレクトリです。
    - **README.md**: `.vscode`ディレクトリに関する説明ドキュメントです。
    - **extensions.json**: 推奨されるVS Code拡張機能のリストを定義します。
    - **settings.json**: ワークスペース固有のVS Code設定を定義します。
- **LICENSE**: プロジェクトのライセンス情報（例: MIT License）が記述されています。
- **README.ja.md**: プロジェクトの概要、使い方、機能などを日本語で説明するメインドキュメントです。
- **README.md**: プロジェクトの概要、使い方、機能などを英語で説明するメインドキュメントです。
- **_config.yml**: Jekyllなどの静的サイトジェネレーターの設定ファイルである可能性があります。
- **dev-requirements.txt**: 開発環境で必要となるPythonパッケージとそのバージョンをリストアップします。
- **examples/**: 設定ファイルや使用例を格納するディレクトリです。
    - **config.example.toml**: メインの設定ファイル（TOML形式）の記述例です。
    - **monitoring-group-example.toml**: 監視グループに関する設定例です。
- **generated-docs/**: AIによって自動生成されたドキュメントやレポートが格納されるディレクトリです。
- **issue-notes/**: GitHub Issuesに関連するメモや調査レポートを格納するディレクトリです。
- **pytest.ini**: Pythonのテストフレームワークであるpytestの設定ファイルです。
- **requirements.txt**: プロジェクトの実行に必要となるPythonパッケージとそのバージョンをリストアップします。
- **ruff.toml**: Pythonの高速LinterであるRuffの設定ファイルです。
- **src/**: プロジェクトの主要なソースコードが格納されるディレクトリです。
    - **__init__.py**: Pythonパッケージとして`src`ディレクトリを認識させるためのファイルです。
    - **__main__.py**: プロジェクトがPythonパッケージとして実行された際のエントリポイントとなるファイルです。
    - **cat_file_watcher.py**: ファイル変更監視のメインロジックとイベントハンドリングを担う主要なモジュールです。
    - **command_executor.py**: ファイル変更が検出された際に、指定された外部コマンドを実行する機能を提供します。
    - **config_loader.py**: TOML形式などの設定ファイルを読み込み、アプリケーションに設定を供給します。
    - **config_validator.py**: 読み込まれた設定ファイルの構造と値の正当性を検証します。
    - **error_logger.py**: アプリケーション実行中に発生したエラーを記録するロギング機能を提供します。
    - **external_config_merger.py**: 複数の外部設定ファイルを統合し、最終的な設定オブジェクトを生成します。
    - **file_monitor.py**: ファイルシステムイベント（作成、変更、削除など）を監視し、通知する機能を提供します。
    - **interval_parser.py**: 時間間隔を表す文字列を解析し、適切な時間単位に変換します。
    - **process_detector.py**: 特定のプロセスが実行中であるかどうかを検出し、その状態に応じて動作を制御します。
    - **time_period_checker.py**: 特定の時間帯（例: 午前9時から午後5時まで）に現在時刻が該当するかどうかをチェックします。
    - **timestamp_printer.py**: ログや出力にタイムスタンプを付加する機能を提供します。
- **tests/**: プロジェクトのテストコードが格納されるディレクトリです。
    - **test_basics.py**: 基本的な機能のテストケースを記述します。
    - **test_cat_file_watcher.py**: `cat_file_watcher.py`モジュールの主要な機能をテストします。
    - **test_colorama.py**: コンソール出力の色付けライブラリColoramaのテストケースを記述します。
    - **test_command_logging.py**: コマンド実行のロギング機能に関するテストケースを記述します。
    - **test_command_suppression.py**: コマンドの実行抑制機能に関するテストケースを記述します。
    - **test_commands_and_processes_sections.py**: 設定ファイルのコマンドおよびプロセスセクションに関するテストケースを記述します。
    - **test_config_reload.py**: 設定ファイルの動的リロード機能に関するテストケースを記述します。
    - **test_cwd.py**: カレントワーキングディレクトリ(CWD)の挙動に関するテストケースを記述します。
    - **test_directory_monitoring.py**: ディレクトリ監視機能に関するテストケースを記述します。
    - **test_empty_filename.py**: 空のファイル名が指定された場合の挙動に関するテストケースを記述します。
    - **test_error_log_clarity.py**: エラーログの明確さに関するテストケースを記述します。
    - **test_error_logging.py**: エラーロギング機能全般に関するテストケースを記述します。
    - **test_external_files.py**: 外部ファイルとの連携に関するテストケースを記述します。
    - **test_interval_parser.py**: 時間間隔パーサーのテストケースを記述します。
    - **test_intervals.py**: 時間間隔の指定と解釈に関するテストケースを記述します。
    - **test_main_loop_interval.py**: メインループの間隔に関するテストケースを記述します。
    - **test_multiple_empty_filenames.py**: 複数の空ファイル名が指定された場合の挙動に関するテストケースを記述します。
    - **test_new_interval_format.py**: 新しい時間間隔フォーマットに関するテストケースを記述します。
    - **test_process_detection.py**: プロセス検出機能に関するテストケースを記述します。
    - **test_suppression_logging.py**: コマンド抑制時のロギングに関するテストケースを記述します。
    - **test_terminate_if_process.py**: 特定のプロセスが実行中の場合に終了する機能に関するテストケースを記述します。
    - **test_time_periods.py**: 時間帯チェック機能に関するテストケースを記述します。
    - **test_timestamp.py**: タイムスタンプ出力機能に関するテストケースを記述します。

## 関数詳細説明
プロジェクト情報には具体的な関数の詳細な説明が提供されていません。しかし、主要なモジュールから推測される機能の単位として、以下のような役割を持つ関数群が存在すると考えられます。

- `src/cat_file_watcher.py`:
    - ファイルシステムイベントの監視を開始・停止する機能。
    - 検出されたイベントに応じて、適切なコマンド実行ロジックを呼び出すイベントハンドリング機能。
    - アプリケーションのメインループを制御し、設定された間隔で処理を繰り返す機能。
- `src/command_executor.py`:
    - 外部コマンドを指定された引数で実行する機能。
    - コマンドの出力（標準出力、標準エラー出力）をキャプチャし、ロギングする機能。
    - コマンドの実行環境（カレントディレクトリ、環境変数など）を制御する機能。
- `src/config_loader.py`:
    - TOML形式などの設定ファイルをファイルパスから読み込む機能。
    - 読み込んだ設定データをPythonのデータ構造（辞書など）にパースする機能。
- `src/config_validator.py`:
    - 読み込まれた設定データが、期待されるスキーマと型に準拠しているかを検証する機能。
    - 不正な設定項目や値に対してエラーを報告する機能。
- `src/error_logger.py`:
    - アプリケーション実行中に発生した例外やエラーメッセージをログファイルやコンソールに出力する機能。
    - エラーの深刻度（info, warning, error, criticalなど）に応じてログレベルを管理する機能。
- `src/external_config_merger.py`:
    - 複数の設定ソース（例: 基本設定、ユーザー設定、環境変数）をマージし、最終的な設定を生成する機能。
    - 設定の上書き順序や優先度を管理する機能。
- `src/file_monitor.py`:
    - 指定されたファイルやディレクトリの変更を非同期的に監視する機能。
    - ファイル作成、変更、削除などのイベントをアプリケーションのメインロジックに通知する機能。
- `src/interval_parser.py`:
    - "10s", "5m", "1h" のような文字列形式の時間間隔を、秒数などの数値形式に変換する機能。
    - 無効な時間間隔フォーマットを検出し、エラーを報告する機能。
- `src/process_detector.py`:
    - 指定された名前やIDを持つプロセスが現在実行中であるかを検出する機能。
    - プロセスの状態（起動中、終了済みなど）を取得する機能。
- `src/time_period_checker.py`:
    - 現在時刻が、設定された特定の時間帯（例: 業務時間内、メンテナンス時間帯）に含まれるかを判断する機能。
    - 日付や曜日の条件も考慮する機能。
- `src/timestamp_printer.py`:
    - 指定された文字列に現在のタイムスタンプを付加して出力する機能。
    - タイムスタンプのフォーマットをカスタマイズする機能。

## 関数呼び出し階層ツリー
```
関数呼び出し階層を分析できませんでした

---
Generated at: 2025-10-20 07:02:14 JST

Last updated: 2025-10-12

# Project Overview

## プロジェクト概要
- ファイルの変更をリアルタイムで監視し、指定されたコマンドを自動実行するツールです。
- 設定可能なルールに基づき、効率的なタスク自動化とワークフロー改善を支援します。
- Pythonで実装されており、設定ファイルを介して柔軟な監視・実行ロジックを定義できます。

## 技術スタック
- フロントエンド: 該当なし（本プロジェクトはバックエンド/CLIツールのため）
- 音楽・オーディオ:
    - Tone.js: Web Audio APIを抽象化し、Webブラウザ上で音楽やオーディオを生成・操作するためのJavaScriptライブラリです。
    - Web Audio API: Webブラウザで高度な音声処理を行うためのAPIで、Tone.jsを通じて利用されています。
    - MML (Music Macro Language): 音楽をテキストで記述するための記法パーサーです。特定のユースケースで音声通知などに利用される可能性があります。
- 開発ツール:
    - Node.js runtime: JavaScript実行環境で、Web Audio API関連のツールやビルドスクリプトなどに利用される可能性があります。
    - Python: プロジェクトの主要なプログラミング言語であり、ファイル監視ロジックやコマンド実行機能の実装に使用されています。
- テスト:
    - Pytest: Pythonで書かれたテストコードを効率的に実行するためのテストフレームワークです。
- ビルドツール: 該当なし（特別なビルドプロセスは明記されていません）
- 言語機能:
    - Python: プロジェクトの主要言語であり、その豊富なライブラリとシンプルな構文が活用されています。
- 自動化・CI/CD:
    - GitHub Actions: コードの変更を検知して自動でテスト実行、ドキュメント生成、多言語翻訳などのワークフローを処理するCI/CDサービスです。（プロジェクト要約自動生成、Issue自動管理、README多言語翻訳、i18n automationを含む3個のワークフロー）
- 開発標準:
    - EditorConfig: 異なるIDEやエディタ間でも一貫したコーディングスタイル（インデント、改行コードなど）を維持するための設定ファイルです。
    - Ruff: Pythonの高速なLinterおよびFormatterで、コードの品質と一貫性を保つために利用されています。

## ファイル階層ツリー
```
📄 .editorconfig
📄 .gitignore
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
📁 tests/
  📄 test_basics.py
  📄 test_cat_file_watcher.py
  📄 test_command_logging.py
  📄 test_command_suppression.py
  📄 test_config_reload.py
  📄 test_cwd.py
  📄 test_directory_monitoring.py
  📄 test_empty_filename.py
  📄 test_error_logging.py
  📄 test_external_files.py
  📄 test_interval_parser.py
  📄 test_intervals.py
  📄 test_main_loop_interval.py
  📄 test_new_interval_format.py
  📄 test_process_detection.py
  📄 test_suppression_logging.py
  📄 test_time_periods.py
```

## ファイル詳細説明
- **`.editorconfig`**: コードエディタの設定を統一し、異なる開発環境間での一貫したコーディングスタイルを保証するための設定ファイルです。
- **`.gitignore`**: Gitによるバージョン管理から除外するファイルやディレクトリを指定します。
- **`.vscode/`**: Visual Studio Codeエディタ用の設定や推奨拡張機能を格納するディレクトリです。
    - **`README.md`**: VS Code関連の追加説明や使い方について記述されています。
    - **`extensions.json`**: プロジェクトで推奨されるVS Code拡張機能のリストです。
    - **`settings.json`**: プロジェクト固有のVS Code設定（例: フォーマッタ、リンターの設定）です。
- **`LICENSE`**: プロジェクトの配布条件や利用許諾を定めたライセンス情報ファイルです。
- **`README.ja.md`**, **`README.md`**: プロジェクトの概要、インストール方法、使い方、機能説明などを記述した多言語対応のドキュメントファイルです。
- **`dev-requirements.txt`**: 開発環境で必要となるPythonパッケージのリストです。
- **`examples/`**: 設定ファイルの記述例を格納するディレクトリで、ユーザーが設定を作成する際の参考になります。
    - **`config.example.toml`**: メインとなる設定ファイルの例です。
    - **`monitoring-group-example.toml`**: 監視グループの設定例を示します。
- **`generated-docs/`**: 自動生成されたドキュメントやレポートを格納するディレクトリです。
    - **`daily-summaries`**: 日次での開発状況や進捗のサマリーなどが含まれます。
- **`issue-notes/`**: GitHub Issuesに関連する自動生成されたメモや議論を格納するディレクトリです。
    - **`*.md`**: 個別のIssueに関する詳細な情報、議論、解決策などが記述されています。
- **`pytest.ini`**: PythonのテストフレームワークであるPytestの設定ファイルです。
- **`requirements.txt`**: プロジェクトの実行に最低限必要なPythonパッケージのリストです。
- **`ruff.toml`**: PythonのLinterおよびFormatterであるRuffの設定ファイルです。
- **`src/`**: プロジェクトの主要なソースコードが格納されているディレクトリです。
    - **`__init__.py`**: Pythonパッケージの初期化ファイルです。
    - **`__main__.py`**: パッケージが直接実行された際のエントリーポイントとなるスクリプトです。
    - **`cat_file_watcher.py`**: ファイル変更を監視し、イベントを処理するためのメインロジックを実装しています。
    - **`command_executor.py`**: ファイル変更検知時に実行される外部コマンドを安全に実行し、その結果を処理する機能を提供します。
    - **`config_loader.py`**: TOML形式の設定ファイルを読み込み、パースしてアプリケーションの設定を管理するモジュールです。
    - **`error_logger.py`**: アプリケーション内で発生したエラーを記録し、デバッグや監視に役立てるためのロギング機能を提供します。
    - **`interval_parser.py`**: "10s", "5m" といった文字列形式の時間間隔を、アプリケーションが扱える数値形式に変換する機能を提供します。
    - **`process_detector.py`**: 特定の名前を持つプロセスがシステム上で実行中であるかを検出し、その状態を確認する機能を提供します。
    - **`time_period_checker.py`**: 特定の時間帯（例: 業務時間内）にコマンド実行などのアクションを制限するための時間判定機能を提供します。
- **`tests/`**: プロジェクトの機能が正しく動作するかを確認するためのテストコードを格納するディレクトリです。
    - **`test_basics.py`**, **`test_cat_file_watcher.py`**, など: 各モジュールや機能に特化したユニットテストや結合テストコードが含まれています。

## 関数詳細説明
本プロジェクト情報には関数の詳細なシグネチャ（引数、戻り値）や具体的な実装は提供されていません。しかし、ファイル名と機能概要から、主要なモジュールに含まれるであろう関数とその役割を以下に推測して説明します。

-   **`src/__main__.py`**
    -   `main()`: プログラムのエントリーポイント。設定の読み込み、ファイルウォッチャーの初期化、監視ループの開始をオーケストレーションします。

-   **`src/cat_file_watcher.py`**
    -   `FileWatcher.__init__(config)`: ファイルウォッチャーオブジェクトを初期化します。設定オブジェクトを受け取り、監視対象ファイル、監視間隔、実行コマンドなどを設定します。
    -   `FileWatcher.start_monitoring()`: ファイル監視のメインループを開始します。設定された間隔でファイルの変更をチェックし、変更が検知された場合にコマンド実行などのアクションをトリガーします。
    -   `FileWatcher._check_file_changes()`: 監視対象ファイルの最終変更時刻などを確認し、前回のチェック時からの変更を検出します。
    -   `FileWatcher._execute_action(file_path)`: ファイル変更が検知された際に、設定に基づいたコマンドを実行したり、通知を行ったりする内部関数です。

-   **`src/command_executor.py`**
    -   `CommandExecutor.__init__(logger=None)`: コマンド実行器を初期化します。オプションでロガーを受け取り、実行ログやエラーログを記録します。
    -   `CommandExecutor.run_command(command_line, cwd=None)`: 指定されたコマンドラインを新しいプロセスで実行します。コマンドの標準出力、標準エラー出力、終了コードをキャプチャし、必要に応じてロギングします。`cwd`で実行ディレクトリを指定できます。

-   **`src/config_loader.py`**
    -   `load_config(config_path)`: 指定されたパスにあるTOML形式の設定ファイルを読み込み、パースして辞書またはオブジェクト形式で設定データを返します。
    -   `get_setting(config_data, key_path, default=None)`: 読み込んだ設定データから、指定されたキーパス（例: `['watch', 'interval']`）に対応する設定値を取得します。値が存在しない場合はデフォルト値を返します。

-   **`src/error_logger.py`**
    -   `log_error(message, exception=None)`: エラーメッセージと、必要であれば関連する例外オブジェクトを受け取り、ログファイルやコンソールに出力します。

-   **`src/interval_parser.py`**
    -   `parse_interval(interval_string)`: "5s" (5秒), "10m" (10分), "1h" (1時間) といった文字列形式の時間間隔を、アプリケーションが内部で利用できる秒数などの数値に変換して返します。

-   **`src/process_detector.py`**
    -   `is_process_running(process_name)`: 指定されたプロセス名を持つプロセスが、現在システム上で実行中であるかをブール値で返します。

-   **`src/time_period_checker.py`**
    -   `is_within_period(start_time_str, end_time_str)`: 現在時刻が、指定された開始時刻と終了時刻の範囲内にあるかをブール値で判断します。時刻は "HH:MM" 形式の文字列で指定されます。

## 関数呼び出し階層ツリー
```
関数呼び出し階層を分析できませんでした。

---
Generated at: 2025-10-12 07:02:08 JST

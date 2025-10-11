Last updated: 2025-10-11

# Project Overview

## プロジェクト概要
- ファイルの変更を検知し、指定されたコマンドを自動実行するファイル監視ツールです。
- タイムスタンプを監視することで、リアルタイムに近い自動化を実現します。
- 開発や運用の効率化を目的とした、柔軟性の高いファイル監視ソリューションを提供します。

## 技術スタック
- フロントエンド: [情報なし]
- 音楽・オーディオ:
    - Tone.js: Web Audio APIを用いた音声ライブラリで、ブラウザでの複雑なオーディオ処理を可能にします。
    - Web Audio API: ブラウザに組み込まれたオーディオ処理のAPIで、Tone.js経由で利用されます。
    - MML (Music Macro Language): 音楽をテキストで記述するための言語パーサーで、音声生成に関連します。
- 開発ツール:
    - Node.js runtime: JavaScriptの実行環境です。
- テスト: [情報なし]
- ビルドツール: [情報なし]
- 言語機能: [情報なし] (主にPythonが使用されていますが、明示的な記述がないため記載していません)
- 自動化・CI/CD:
    - GitHub Actions: コードの変更を検知して自動でビルド、テスト、デプロイなどを行うCI/CDプラットフォームです。
        - プロジェクト要約自動生成: プロジェクトの概要ドキュメントを自動で生成します。
        - Issue自動管理: GitHub Issueのライフサイクル管理を自動化します。
        - README多言語翻訳: READMEファイルを複数の言語に自動で翻訳します。
        - i18n automation: 国際化対応のための自動翻訳ワークフローです。
- 開発標準: [情報なし]

## ファイル階層ツリー
```
📄 .gitignore
📄 LICENSE
📖 README.ja.md
📖 README.md
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
  📖 9.md
📄 requirements.txt
📁 src/
  📄 __init__.py
  📄 __main__.py
  📄 cat_file_watcher.py
  📄 command_executor.py
  📄 config_loader.py
  📄 process_detector.py
📁 tests/
  📄 test_basics.py
  📄 test_cat_file_watcher.py
  📄 test_command_suppression.py
  📄 test_config_reload.py
  📄 test_interval_division.py
  📄 test_intervals.py
  📄 test_process_detection.py
```

## ファイル詳細説明
-   `.gitignore`: Gitでバージョン管理しないファイルやディレクトリを指定するファイルです。
-   `LICENSE`: プロジェクトのライセンス情報が記載されています。
-   `README.ja.md`: プロジェクトの日本語版の概要、使い方、開発情報などが記載されたドキュメントです。
-   `README.md`: プロジェクトの英語版の概要、使い方、開発情報などが記載されたドキュメントです。
-   `examples/`: 設定ファイルのサンプルが格納されているディレクトリです。
    -   `config.example.toml`: プロジェクトの設定ファイル（TOML形式）の例です。ユーザーがこれを参考に自分用の設定ファイルを作成できます。
    -   `monitoring-group-example.toml`: 外部ファイル読み込み機能で使用する設定ファイルのグループ化の例です。
-   `generated-docs/`: プロジェクトのドキュメントが自動生成されて格納されるディレクトリです。
-   `issue-notes/`: 開発中のGitHub Issueに関する詳細なメモや補足情報が格納されるディレクトリです。
    -   `[数字].md`, `[数字]-refactoring-summary.md`: 特定のIssueやリファクタリングに関する詳細な議論や決定事項を記録したMarkdownファイルです。
-   `requirements.txt`: Pythonプロジェクトが依存する外部ライブラリとそのバージョンをリストアップしたファイルです。`pip install -r`で依存関係をインストールするために使用されます。
-   `src/`: プロジェクトの主要なPythonソースコードを格納するディレクトリです。
    -   `__init__.py`: `src`ディレクトリがPythonパッケージであることを示し、パッケージの初期化処理を定義できます。
    -   `__main__.py`: `python -m src`のようにパッケージが直接実行された際に呼び出されるエントリポイントとなるファイルです。
    -   `cat_file_watcher.py`: ファイルの変更を監視し、その変更を検知する主要なロジックが実装されています。
    -   `command_executor.py`: ファイルの変更が検知された際に、指定された外部コマンドを実行するロジックを管理します。
    -   `config_loader.py`: 設定ファイル（例: `config.toml`）を読み込み、アプリケーション内で使用できる形にパースするロジックを提供します。
    -   `process_detector.py`: 外部プロセスの実行状態などを検知・管理するためのロジックが含まれており、コマンドの多重実行防止などに利用される可能性があります。
-   `tests/`: プロジェクトのテストコードを格納するディレクトリです。
    -   `test_basics.py`: プロジェクトの基本的な機能やコンポーネントが正しく動作するかを確認するテストです。
    -   `test_cat_file_watcher.py`: `cat_file_watcher.py`モジュールに実装されたファイル監視ロジックの単体テストや統合テストを行います。
    -   `test_command_suppression.py`: コマンドの多重実行抑制や特定の条件での実行停止機能に関するテストです。
    -   `test_config_reload.py`: アプリケーション実行中に設定ファイルをリロードする機能のテストです。
    -   `test_interval_division.py`: 監視間隔の分割や管理に関するロジックのテストです。
    -   `test_intervals.py`: 監視間隔に関連する一般的なテストケースを扱います。
    -   `test_process_detection.py`: `process_detector.py`モジュールに実装されたプロセス検知機能のテストです。

## 関数詳細説明
現在、このプロジェクトの具体的な関数情報は提供されていません。

## 関数呼び出し階層ツリー
```
関数呼び出し階層を分析できませんでした

---
Generated at: 2025-10-11 07:02:03 JST

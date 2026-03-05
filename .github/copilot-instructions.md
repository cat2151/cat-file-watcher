# cat-file-watcher GitHub Copilot 指示書

## プロジェクト概要

cat-file-watcherは、ファイルのタイムスタンプ変化を監視し、ファイルが更新されたときにコマンドを実行するPythonベースのファイル変更監視ツールです。TOMLで設定できる軽量なツールです。

## コードスタイルと規約

### Pythonスタイル

- Python 3.12+互換の構文を使用する
- PEP 8スタイルガイドラインに従う
- わかりやすい変数名・関数名を使用する
- 実行可能スクリプトの先頭にシバン `#!/usr/bin/env python3` を記述する
- 最大限の互換性のため、相対インポートと絶対インポートの両方をサポートする:
  ```python
  try:
      from .module import Class
  except ImportError:
      from module import Class
  ```

### ドキュメント

- すべてのクラスとpublicメソッドにdocstringを追加する
- 明確な説明を持つトリプルクォート文字列を使用する
- 該当する場合はdocstringにArgs、Returns、Raisesセクションを含める
- 記述例:
  ```python
  def method_name(self, param):
      """Brief description.

      Args:
          param: Description of the parameter

      Returns:
          type: Description of the return value

      Raises:
          ErrorType: Description of when the error occurs
      """
  ```

### コメント

- 実装意図を説明するためにコメントを追加する
- インラインコメントは上記において必須な場合にのみ控えめに使用する
- 過剰なコメントよりも自己文書化コードを優先する

## テスト

### テストフレームワーク

- すべてのテストにモダンな `pytest` フレームワークを使用する

### テストカバレッジ

- すべての新機能とバグ修正に対してテストを書く
- 正常系と異常系の両方のテストケースを含める
- エッジケースやエラー条件をテストする
- エラーメッセージと例外処理を検証する

## 設定

### TOML設定

- すべての設定ファイルにTOML形式を使用する

## アーキテクチャ

### 設計原則

- モジュールは単一責任に集中させる
- インスタンス状態を必要としないユーティリティ関数にはstaticメソッドを使用する
- ユーザー向け出力とログには `print()` を使用する

## エラーハンドリング

## セキュリティ

### コマンド実行

- 適切なパラメータで `subprocess.run()` を使用する
- シェルコマンド実行には `shell=True` を設定する（このツールの用途上必要）
- コマンドがハングするのを防ぐため `timeout=30` を使用する
- `capture_output=True` でstdoutとstderrの両方をキャプチャする

### 入力検証

- TOML設定の構造を検証する
- 無効な正規表現パターンを適切に処理する
- ファイルパスを適切にサニタイズする

## 依存関係

### 依存関係の追加

- バージョン制約を `requirements.txt` に更新する

## 互換性

### プラットフォームサポート

- Windowsを優先してサポートする
- クロスプラットフォームのファイルパス処理には `os.path` を使用する

### Pythonバージョン

- Python 3.11+を対象にする
- Python 3.10未満はサポート対象外とし、ムダな機能を削除してシンプル化する
- 最低Pythonバージョン要件を文書化する

## 開発ワークフロー

### ドキュメント

- README.ja.mdを更新せよ。README.mdは更新禁止（README.ja.mdからCIで自動生成されるため）
- 設定形式が変更されたらexamplesを更新する
- すべての設定オプションを明確に文書化する

## コードフォーマットと品質

### コミット前の手順

**重要**: Pythonコードの変更をコミットする前に、必ず以下のコマンドを実行すること:

```bash
# Ruffでコードをフォーマット
ruff format src/ tests/

# 自動修正可能なlint問題を修正
ruff check --fix src/ tests/

# フォーマットとlintを確認（エラーなしで通過すること）
ruff format --check src/ tests/
ruff check src/ tests/
```

これらの手順はすべてのコード変更において**必須**です。フォーマットを怠ると以下の結果をまねく:
- PRレビューの遅延
- メンテナーによる手動フォーマットが必要になる
- PRが却下される可能性がある

### なぜ重要か

- このプロジェクトはRuffを使用して一貫したコードスタイルを強制している
- セキュリティ上の懸念から自動フォーマットのGitHub Actionsワークフローが削除された（issue #71参照）
- コミット前の手動フォーマットが最も安全で効率的なアプローチである

## ベストプラクティス

- わかりやすい変数名で自己文書化コードを書く
- 関数は小さく、集中した内容にする
- 早期最適化を避ける
- コミット前に変更を徹底的にテストする
- **コミット前に必ずruff formatとruff check --fixを実行する**
- 意味のあるコミットメッセージを使用する
- 既存のコードパターンと規約に従う

# userからの指示
- 作業報告は、プルリクエストのコメントに書く。document作成禁止
  - DRY原則に準拠し、「codeやbuild scriptと同じことを、documentに書いたせいで、そのdocumentが陳腐化してハルシネーションやuserレビューコスト増大や混乱ほか様々なトラブル原因になる」を防止する
  - なおissue-notes/は、user（人間）がissueごとの意図を記録する用途で使う。coding agentからはread onlyとする

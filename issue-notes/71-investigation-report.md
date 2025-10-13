# Issue #71 調査報告書

## 調査対象
[Issue #71](https://github.com/cat2151/cat-file-watcher/issues/71): agentによるPRに対して、自動でRuffの実行がされず、毎回「GitHub Actionsの実行を承認する」ボタンをuserが押す必要があり、不便

## 問題の概要
GitHub Copilot等のagentがPull Requestを作成した際、Ruff Code Quality Checkワークフローが自動実行されず、リポジトリ管理者が毎回手動で「GitHub Actionsの実行を承認する」ボタンを押す必要がある。

## 根本原因

### 1. `pull_request_target`の使用による承認要求

現在の`.github/workflows/ruff-check.yml`は`pull_request_target`トリガーを使用している:

```yaml
on:
  pull_request_target:
    paths:
      - 'src/**/*.py'
      ...
```

`pull_request_target`を使用すると、以下の理由で承認が必要になる:

1. **セキュリティ上の制約**: `pull_request_target`はベースリポジトリのコンテキストで実行され、リポジトリシークレットやwrite権限へのアクセスが可能。このため、GitHubは初回コントリビューターやbotからのワークフロー実行を自動的にブロックする。

2. **Botの扱い**: GitHub Copilot等のbotアカウント（`copilot[bot]`）も「first-time contributor」として扱われ、セキュリティポリシーにより手動承認が必要となる。

### 2. 現在のワークフローの問題点

現在のワークフローには以下のセキュリティリスクがある:

```yaml
- name: Checkout repository
  uses: actions/checkout@v4
  with:
    ref: ${{ github.event.pull_request.head.ref || github.ref }}
    repository: ${{ github.event.pull_request.head.repo.full_name || github.repository }}
```

このチェックアウト方法は、PRのheadブランチ（潜在的に信頼できないコード）をチェックアウトし、そのコードを実行する。これは`pull_request_target`使用時の**重大なセキュリティリスク**である。

### 3. なぜこの構成が採用されたか

このワークフローは自動フォーマット機能を実装するために設計されている:

```yaml
- name: Auto-format code with Ruff
  run: |
    ruff format src/
    ruff check --fix src/

- name: Commit formatting changes
  if: github.event_name == 'pull_request_target'
  run: |
    git commit -m "Auto-format code with Ruff [skip ci]"
    git push
```

PRブランチへの自動コミット・プッシュには`contents: write`権限が必要であり、これを実現するために`pull_request_target`が使用されている。

## 技術的背景

### `pull_request` vs `pull_request_target`の違い

| 特性 | pull_request | pull_request_target |
|------|--------------|---------------------|
| 実行コンテキスト | PRのマージコミット | ベースブランチ（main等） |
| シークレットアクセス | 制限あり | フルアクセス |
| Write権限 | なし | あり |
| セキュリティリスク | 低 | 高（要注意） |
| 承認要求 | なし（通常） | あり（初回/bot） |

### なぜ承認が必要か

GitHubの公式ドキュメントとセキュリティガイドラインによると:

1. **悪意あるコード実行の防止**: `pull_request_target`はシークレットアクセスを持つため、信頼できないPRが悪意あるコードを実行してシークレットを盗むことを防ぐ必要がある。

2. **first-time contributorポリシー**: 2021年4月のGitHub変更により、初めてコントリビュートするユーザーやbotからのワークフロー実行は、メンテナーの明示的な承認が必須となった。

3. **Botもコントリビューター扱い**: GitHub Copilot等のbotアカウントも「外部コントリビューター」として扱われ、同じ承認要件が適用される。

## 既知の制限と回避策

### GitHubコミュニティでの議論

以下のGitHubコミュニティディスカッションで同様の問題が報告されている:

- [Avoid "workflows awaiting approval" when copilot agent create PR](https://github.com/orgs/community/discussions/167493)
- [How to auto-approve workflow execution when Copilot coding agent creates PRs](https://github.com/orgs/community/discussions/162826)

これらのディスカッションから判明した事実:

1. **完全な自動承認は不可能**: GitHubの設計上、リポジトリオーナーであっても、first-time contributorやbotからのワークフロー実行を完全に自動承認する設定は存在しない。

2. **リポジトリ設定の限界**: `Settings > Actions > General`の「Fork pull request workflows from external contributors」設定も、同一リポジトリ内のbotには適用されない。

3. **一度承認すれば以降は不要**: 同じコントリビューター（bot含む）からの初回PRが承認されれば、2回目以降は自動的に実行される可能性があるが、botは毎回新しいブランチから作業するため、この恩恵を受けられない場合がある。

### 検討された回避策とその問題点

#### 1. `pull_request`への変更
**問題**: PRブランチへの自動コミット・プッシュができなくなる（write権限がないため）。

#### 2. Personal Access Token (PAT)の使用
**問題**: セキュリティリスクが増大し、根本的な承認要求問題は解決しない。

#### 3. GitHub Actions APIによる自動承認スクリプト
**問題**: ワークフローが承認待ち状態では、そのワークフロー自体が実行されないため、自己承認は不可能。

#### 4. 別ワークフローからのAPI呼び出し
**問題**: 技術的に可能だが、複雑性が増し、セキュリティポリシーの意図を損なう。

## セキュリティ上の重大な問題

現在のワークフロー構成には、以下の**セキュリティ脆弱性**が存在する:

```yaml
on:
  pull_request_target:  # ベースリポジトリのコンテキストで実行

steps:
  - uses: actions/checkout@v4
    with:
      ref: ${{ github.event.pull_request.head.ref }}  # PRのコードをチェックアウト
      
  - name: Auto-format code with Ruff
    run: |
      ruff format src/  # 信頼できないPRのコードを実行！
```

この構成は「[PWN Request](https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/)」として知られる攻撃パターンに対して脆弱である:

1. 攻撃者が悪意あるコードを含むPRを作成
2. リポジトリ管理者が承認
3. ワークフローが`pull_request_target`コンテキスト（シークレット付き）で悪意あるコードを実行
4. シークレット窃取やリポジトリへの不正アクセスが可能に

## 関連するTech Blog記事とドキュメント

### GitHub公式ドキュメント
1. **[Approving workflow runs from forks](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/approve-runs-from-forks)**
   - ワークフロー承認の仕組みと要件

2. **[Events that trigger workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)**
   - `pull_request`と`pull_request_target`の違い

3. **[Managing GitHub Actions settings for a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository)**
   - リポジトリレベルの承認設定

### セキュリティとベストプラクティス
4. **[Keeping your GitHub Actions and workflows secure Part 1: Preventing pwn requests](https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/)**
   - `pull_request_target`の安全な使用方法
   - PWN Request攻撃パターンの解説

5. **[GitHub Actions Security Best Practices](https://blog.gitguardian.com/github-actions-security-cheat-sheet/)**
   - GitHub Actionsのセキュリティチートシート
   - 最小権限の原則

6. **[Secure GitHub Actions by pull_request_target](https://dev.to/suzukishunsuke/secure-github-actions-by-pullrequesttarget-641)**
   - `pull_request_target`の安全な実装パターン

### コミュニティディスカッション
7. **[pull_request_target Misconfiguration Leads to RCE](https://orca.security/resources/blog/pull-request-nightmare-github-actions-rce/)**
   - 実際の脆弱性事例とリモートコード実行のリスク

8. **[Mitigating Attack Vectors in GitHub Workflows](https://openssf.org/blog/2024/08/12/mitigating-attack-vectors-in-github-workflows/)**
   - ワークフローにおける攻撃ベクトルの軽減策

### 関連する技術記事
9. **[Pull Request vs Pull Request Target trigger](https://runs-on.com/github-actions/pull-request-vs-pull-request-target/)**
   - 2つのトリガーの使い分けと推奨パターン

10. **[What is the difference between pull_request and pull_request_target event](https://stackoverflow.com/questions/74957218/what-is-the-difference-between-pull-request-and-pull-request-target-event-in-git)**
    - Stack Overflowでの詳細な技術解説

## 結論

### 問題の本質
Issue #71の根本原因は、以下の3つの要因が組み合わさったものである:

1. **GitHubのセキュリティポリシー**: first-time contributorとbotからの`pull_request_target`ワークフローは必ず手動承認が必要
2. **機能要件**: PRブランチへの自動コミット・プッシュには`pull_request_target`が必要
3. **設計上の制約**: この承認要求を完全に回避する方法はGitHubの仕様上存在しない

### 現在のワークフローのセキュリティリスク
現在の実装は、`pull_request_target`で信頼できないコードをチェックアウト・実行するため、**重大なセキュリティ脆弱性**を含んでいる。手動承認は、この脆弱性に対する唯一の防御層となっている。

### 推奨される対応

以下の理由により、**現在の手動承認プロセスを維持することを推奨**:

1. **セキュリティ優先**: 承認プロセスは脆弱性を悪用した攻撃を防ぐ重要な防御層
2. **仕様上の制限**: GitHubの設計思想として、この承認は回避できない
3. **トレードオフ**: 利便性よりもセキュリティを優先すべき

### 代替アプローチの可能性

もし自動承認を本当に実現したい場合、以下の根本的な設計変更が必要:

1. **自動フォーマット機能の削除**: `pull_request`トリガーに変更し、チェックのみ実行（コミット・プッシュなし）
2. **事前フォーマット要求**: PRを作成する前に、ローカルまたは別プロセスでフォーマットを完了させる
3. **別ワークフローへの分離**: チェック用とコミット用でワークフローを分離し、異なるトリガーを使用

いずれのアプローチも現在の「自動フォーマット＋自動コミット」機能を犠牲にすることになる。

## 参考情報

- [Issue #71](https://github.com/cat2151/cat-file-watcher/issues/71)
- [Issue #67](https://github.com/cat2151/cat-file-watcher/issues/67) - Ruffワークフローの初期実装
- 現在のワークフローファイル: `.github/workflows/ruff-check.yml`

---
**調査日**: 2025-10-13  
**調査者**: GitHub Copilot Agent

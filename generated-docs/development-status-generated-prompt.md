Last updated: 2025-10-13

# 開発状況生成プロンプト（開発者向け）

## 生成するもの：
- 現在openされているissuesを3行で要約する
- 次の一手の候補を3つlistする
- 次の一手の候補3つそれぞれについて、極力小さく分解して、その最初の小さな一歩を書く

## 生成しないもの：
- 「今日のissue目標」などuserに提案するもの
  - ハルシネーションの温床なので生成しない
- ハルシネーションしそうなものは生成しない（例、無価値なtaskや新issueを勝手に妄想してそれをuserに提案する等）
- プロジェクト構造情報（来訪者向け情報のため、別ファイルで管理）

## 「Agent実行プロンプト」生成ガイドライン：
「Agent実行プロンプト」作成時は以下の要素を必ず含めてください：

### 必須要素
1. **対象ファイル**: 分析/編集する具体的なファイルパス
2. **実行内容**: 具体的な分析や変更内容（「分析してください」ではなく「XXXファイルのYYY機能を分析し、ZZZの観点でmarkdown形式で出力してください」）
3. **確認事項**: 変更前に確認すべき依存関係や制約
4. **期待する出力**: markdown形式での結果や、具体的なファイル変更

### Agent実行プロンプト例

**良い例（上記「必須要素」4項目を含む具体的なプロンプト形式）**:
```
対象ファイル: `.github/workflows/translate-readme.yml`と`.github/workflows/call-translate-readme.yml`

実行内容: 対象ファイルについて、外部プロジェクトから利用する際に必要な設定項目を洗い出し、以下の観点から分析してください：
1) 必須入力パラメータ（target-branch等）
2) 必須シークレット（GEMINI_API_KEY）
3) ファイル配置の前提条件（README.ja.mdの存在）
4) 外部プロジェクトでの利用時に必要な追加設定

確認事項: 作業前に既存のworkflowファイルとの依存関係、および他のREADME関連ファイルとの整合性を確認してください。

期待する出力: 外部プロジェクトがこの`call-translate-readme.yml`を導入する際の手順書をmarkdown形式で生成してください。具体的には：必須パラメータの設定方法、シークレットの登録手順、前提条件の確認項目を含めてください。
```

**避けるべき例**:
- callgraphについて調べてください
- ワークフローを分析してください
- issue-noteの処理フローを確認してください

## 出力フォーマット：
以下のMarkdown形式で出力してください：

```markdown
# Development Status

## 現在のIssues
[以下の形式で3行でオープン中のissuesを要約。issue番号を必ず書く]
- [1行目の説明]
- [2行目の説明]
- [3行目の説明]

## 次の一手候補
1. [候補1のタイトル。issue番号を必ず書く]
   - 最初の小さな一歩: [具体的で実行可能な最初のアクション]
   - Agent実行プロンプト:
     ```
     対象ファイル: [分析/編集する具体的なファイルパス]

     実行内容: [具体的な分析や変更内容を記述]

     確認事項: [変更前に確認すべき依存関係や制約]

     期待する出力: [markdown形式での結果や、具体的なファイル変更の説明]
     ```

2. [候補2のタイトル。issue番号を必ず書く]
   - 最初の小さな一歩: [具体的で実行可能な最初のアクション]
   - Agent実行プロンプト:
     ```
     対象ファイル: [分析/編集する具体的なファイルパス]

     実行内容: [具体的な分析や変更内容を記述]

     確認事項: [変更前に確認すべき依存関係や制約]

     期待する出力: [markdown形式での結果や、具体的なファイル変更の説明]
     ```

3. [候補3のタイトル。issue番号を必ず書く]
   - 最初の小さな一歩: [具体的で実行可能な最初のアクション]
   - Agent実行プロンプト:
     ```
     対象ファイル: [分析/編集する具体的なファイルパス]

     実行内容: [具体的な分析や変更内容を記述]

     確認事項: [変更前に確認すべき依存関係や制約]

     期待する出力: [markdown形式での結果や、具体的なファイル変更の説明]
     ```
```


# 開発状況情報
- 以下の開発状況情報を参考にしてください。
- Issue番号を記載する際は、必ず [Issue #番号](../issue-notes/番号.md) の形式でMarkdownリンクとして記載してください。

## プロジェクトのファイル一覧
- .editorconfig
- .github/actions-tmp/.github/workflows/call-callgraph.yml
- .github/actions-tmp/.github/workflows/call-daily-project-summary.yml
- .github/actions-tmp/.github/workflows/call-issue-note.yml
- .github/actions-tmp/.github/workflows/call-translate-readme.yml
- .github/actions-tmp/.github/workflows/callgraph.yml
- .github/actions-tmp/.github/workflows/check-recent-human-commit.yml
- .github/actions-tmp/.github/workflows/daily-project-summary.yml
- .github/actions-tmp/.github/workflows/issue-note.yml
- .github/actions-tmp/.github/workflows/translate-readme.yml
- .github/actions-tmp/.github_automation/callgraph/codeql-queries/callgraph.ql
- .github/actions-tmp/.github_automation/callgraph/codeql-queries/codeql-pack.lock.yml
- .github/actions-tmp/.github_automation/callgraph/codeql-queries/qlpack.yml
- .github/actions-tmp/.github_automation/callgraph/config/example.json
- .github/actions-tmp/.github_automation/callgraph/docs/callgraph.md
- .github/actions-tmp/.github_automation/callgraph/presets/callgraph.js
- .github/actions-tmp/.github_automation/callgraph/presets/style.css
- .github/actions-tmp/.github_automation/callgraph/scripts/analyze-codeql.cjs
- .github/actions-tmp/.github_automation/callgraph/scripts/callgraph-utils.cjs
- .github/actions-tmp/.github_automation/callgraph/scripts/check-codeql-exists.cjs
- .github/actions-tmp/.github_automation/callgraph/scripts/check-node-version.cjs
- .github/actions-tmp/.github_automation/callgraph/scripts/common-utils.cjs
- .github/actions-tmp/.github_automation/callgraph/scripts/copy-commit-results.cjs
- .github/actions-tmp/.github_automation/callgraph/scripts/extract-sarif-info.cjs
- .github/actions-tmp/.github_automation/callgraph/scripts/find-process-results.cjs
- .github/actions-tmp/.github_automation/callgraph/scripts/generate-html-graph.cjs
- .github/actions-tmp/.github_automation/callgraph/scripts/generateHTML.cjs
- .github/actions-tmp/.github_automation/check_recent_human_commit/scripts/check-recent-human-commit.cjs
- .github/actions-tmp/.github_automation/project_summary/docs/daily-summary-setup.md
- .github/actions-tmp/.github_automation/project_summary/prompts/development-status-prompt.md
- .github/actions-tmp/.github_automation/project_summary/prompts/project-overview-prompt.md
- .github/actions-tmp/.github_automation/project_summary/scripts/ProjectSummaryCoordinator.cjs
- .github/actions-tmp/.github_automation/project_summary/scripts/development/DevelopmentStatusGenerator.cjs
- .github/actions-tmp/.github_automation/project_summary/scripts/development/GitUtils.cjs
- .github/actions-tmp/.github_automation/project_summary/scripts/development/IssueTracker.cjs
- .github/actions-tmp/.github_automation/project_summary/scripts/generate-project-summary.cjs
- .github/actions-tmp/.github_automation/project_summary/scripts/overview/CodeAnalyzer.cjs
- .github/actions-tmp/.github_automation/project_summary/scripts/overview/ProjectAnalysisOrchestrator.cjs
- .github/actions-tmp/.github_automation/project_summary/scripts/overview/ProjectDataCollector.cjs
- .github/actions-tmp/.github_automation/project_summary/scripts/overview/ProjectDataFormatter.cjs
- .github/actions-tmp/.github_automation/project_summary/scripts/overview/ProjectOverviewGenerator.cjs
- .github/actions-tmp/.github_automation/project_summary/scripts/overview/TechStackAnalyzer.cjs
- .github/actions-tmp/.github_automation/project_summary/scripts/shared/BaseGenerator.cjs
- .github/actions-tmp/.github_automation/project_summary/scripts/shared/FileSystemUtils.cjs
- .github/actions-tmp/.github_automation/project_summary/scripts/shared/ProjectFileUtils.cjs
- .github/actions-tmp/.github_automation/translate/docs/TRANSLATION_SETUP.md
- .github/actions-tmp/.github_automation/translate/scripts/translate-readme.cjs
- .github/actions-tmp/.gitignore
- .github/actions-tmp/.vscode/settings.json
- .github/actions-tmp/LICENSE
- .github/actions-tmp/README.ja.md
- .github/actions-tmp/README.md
- .github/actions-tmp/generated-docs/callgraph.html
- .github/actions-tmp/generated-docs/callgraph.js
- .github/actions-tmp/generated-docs/development-status-generated-prompt.md
- .github/actions-tmp/generated-docs/development-status.md
- .github/actions-tmp/generated-docs/project-overview.md
- .github/actions-tmp/generated-docs/style.css
- .github/actions-tmp/issue-notes/10.md
- .github/actions-tmp/issue-notes/11.md
- .github/actions-tmp/issue-notes/12.md
- .github/actions-tmp/issue-notes/13.md
- .github/actions-tmp/issue-notes/14.md
- .github/actions-tmp/issue-notes/15.md
- .github/actions-tmp/issue-notes/16.md
- .github/actions-tmp/issue-notes/17.md
- .github/actions-tmp/issue-notes/18.md
- .github/actions-tmp/issue-notes/19.md
- .github/actions-tmp/issue-notes/2.md
- .github/actions-tmp/issue-notes/20.md
- .github/actions-tmp/issue-notes/21.md
- .github/actions-tmp/issue-notes/22.md
- .github/actions-tmp/issue-notes/23.md
- .github/actions-tmp/issue-notes/24.md
- .github/actions-tmp/issue-notes/25.md
- .github/actions-tmp/issue-notes/26.md
- .github/actions-tmp/issue-notes/27.md
- .github/actions-tmp/issue-notes/28.md
- .github/actions-tmp/issue-notes/3.md
- .github/actions-tmp/issue-notes/4.md
- .github/actions-tmp/issue-notes/7.md
- .github/actions-tmp/issue-notes/8.md
- .github/actions-tmp/issue-notes/9.md
- .github/actions-tmp/package-lock.json
- .github/actions-tmp/package.json
- .github/actions-tmp/src/main.js
- .github/copilot-instructions.md
- .github/workflows/call-daily-project-summary.yml
- .github/workflows/call-issue-note.yml
- .github/workflows/call-translate-readme.yml
- .github/workflows/ruff-check.yml
- .gitignore
- .vscode/README.md
- .vscode/extensions.json
- .vscode/settings.json
- =0.6.0
- LICENSE
- README.ja.md
- README.md
- dev-requirements.txt
- examples/config.example.toml
- examples/monitoring-group-example.toml
- issue-notes/11.md
- issue-notes/13.md
- issue-notes/15.md
- issue-notes/16-refactoring-summary.md
- issue-notes/16.md
- issue-notes/19-refactoring-summary.md
- issue-notes/19.md
- issue-notes/21.md
- issue-notes/23.md
- issue-notes/24.md
- issue-notes/26.md
- issue-notes/27.md
- issue-notes/30.md
- issue-notes/32.md
- issue-notes/33.md
- issue-notes/35.md
- issue-notes/37.md
- issue-notes/39.md
- issue-notes/41.md
- issue-notes/43.md
- issue-notes/45.md
- issue-notes/46.md
- issue-notes/48.md
- issue-notes/50.md
- issue-notes/52.md
- issue-notes/54.md
- issue-notes/56.md
- issue-notes/57.md
- issue-notes/58.md
- issue-notes/62.md
- issue-notes/63.md
- issue-notes/65.md
- issue-notes/67.md
- issue-notes/69.md
- issue-notes/71.md
- issue-notes/72.md
- issue-notes/74.md
- issue-notes/76.md
- issue-notes/78.md
- issue-notes/9.md
- pytest.ini
- requirements.txt
- ruff.toml
- src/__init__.py
- src/__main__.py
- src/cat_file_watcher.py
- src/command_executor.py
- src/config_loader.py
- src/error_logger.py
- src/interval_parser.py
- src/process_detector.py
- src/time_period_checker.py
- src/timestamp_printer.py
- tests/test_basics.py
- tests/test_cat_file_watcher.py
- tests/test_colorama.py
- tests/test_command_logging.py
- tests/test_command_suppression.py
- tests/test_commands_and_processes_sections.py
- tests/test_config_reload.py
- tests/test_cwd.py
- tests/test_directory_monitoring.py
- tests/test_empty_filename.py
- tests/test_error_logging.py
- tests/test_external_files.py
- tests/test_interval_parser.py
- tests/test_intervals.py
- tests/test_main_loop_interval.py
- tests/test_multiple_empty_filenames.py
- tests/test_new_interval_format.py
- tests/test_process_detection.py
- tests/test_suppression_logging.py
- tests/test_terminate_if_process.py
- tests/test_time_periods.py
- tests/test_timestamp.py

## 現在のオープンIssues
## [Issue #71](../issue-notes/71.md): agentによるPRに対して、自動でRuffの実行がされず、毎回「GitHub Actionsの実行を承認する」ボタンをuserが押す必要があり、不便
[issue-notes/71.md](https://github.com/cat2151/cat-file-watcher/blob/main/issue-notes/71.md)

...
ラベル: 
--- issue-notes/71.md の内容 ---

```markdown
# issue agentによるPRに対して、自動でRuffの実行がされず、毎回「GitHub Actionsの実行を承認する」ボタンをuserが押す必要があり、不便 #71
[issues #71](https://github.com/cat2151/cat-file-watcher/issues/71)

# 対策
- Claudeに現在のworkflow ymlを投げた
- 改善版を生成させた
- testする


```

## ドキュメントで言及されているファイルの内容
### issue-notes/71.md
```md
# issue agentによるPRに対して、自動でRuffの実行がされず、毎回「GitHub Actionsの実行を承認する」ボタンをuserが押す必要があり、不便 #71
[issues #71](https://github.com/cat2151/cat-file-watcher/issues/71)

# 対策
- Claudeに現在のworkflow ymlを投げた
- 改善版を生成させた
- testする


```

## 最近の変更（過去7日間）
### コミット履歴:
c245125 fixed #78
3f2006f Add issue note for #78 [auto]
c8a5f89 Merge pull request #77 from cat2151/copilot/add-commands-and-processes-sections
938e542 Auto-format code with Ruff [skip ci]
5ff45cf Update issue notes and fix linter issues
f51ac95 Add [[commands]] and [[processes]] sections support
0b9998d Initial plan
c3f973f Add issue note for #76 [auto]
278bdce Merge pull request #73 from cat2151/copilot/update-toml-files-section
eca307b Merge branch 'main' of github.com:cat2151/cat-file-watcher into main

### 変更されたファイル:
.github/workflows/ruff-check.yml
=0.6.0
README.md
examples/config.example.toml
examples/monitoring-group-example.toml
issue-notes/72.md
issue-notes/76.md
issue-notes/78.md
src/cat_file_watcher.py
src/config_loader.py
tests/test_basics.py
tests/test_cat_file_watcher.py
tests/test_colorama.py
tests/test_command_logging.py
tests/test_command_suppression.py
tests/test_commands_and_processes_sections.py
tests/test_config_reload.py
tests/test_cwd.py
tests/test_directory_monitoring.py
tests/test_empty_filename.py
tests/test_error_logging.py
tests/test_external_files.py
tests/test_interval_parser.py
tests/test_intervals.py
tests/test_main_loop_interval.py
tests/test_multiple_empty_filenames.py
tests/test_new_interval_format.py
tests/test_process_detection.py
tests/test_suppression_logging.py
tests/test_terminate_if_process.py
tests/test_time_periods.py
tests/test_timestamp.py


---
Generated at: 2025-10-13 07:01:43 JST

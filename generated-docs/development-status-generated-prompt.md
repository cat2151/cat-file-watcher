Last updated: 2026-03-04

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
- .github/actions-tmp/.github/workflows/call-check-large-files.yml
- .github/actions-tmp/.github/workflows/call-daily-project-summary.yml
- .github/actions-tmp/.github/workflows/call-issue-note.yml
- .github/actions-tmp/.github/workflows/call-rust-windows-check.yml
- .github/actions-tmp/.github/workflows/call-translate-readme.yml
- .github/actions-tmp/.github/workflows/callgraph.yml
- .github/actions-tmp/.github/workflows/check-large-files.yml
- .github/actions-tmp/.github/workflows/check-recent-human-commit.yml
- .github/actions-tmp/.github/workflows/daily-project-summary.yml
- .github/actions-tmp/.github/workflows/issue-note.yml
- .github/actions-tmp/.github/workflows/rust-windows-check.yml
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
- .github/actions-tmp/.github_automation/check-large-files/README.md
- .github/actions-tmp/.github_automation/check-large-files/check-large-files.toml.default
- .github/actions-tmp/.github_automation/check-large-files/scripts/check_large_files.py
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
- .github/actions-tmp/_config.yml
- .github/actions-tmp/generated-docs/callgraph.html
- .github/actions-tmp/generated-docs/callgraph.js
- .github/actions-tmp/generated-docs/development-status-generated-prompt.md
- .github/actions-tmp/generated-docs/development-status.md
- .github/actions-tmp/generated-docs/project-overview-generated-prompt.md
- .github/actions-tmp/generated-docs/project-overview.md
- .github/actions-tmp/generated-docs/style.css
- .github/actions-tmp/googled947dc864c270e07.html
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
- .github/actions-tmp/issue-notes/29.md
- .github/actions-tmp/issue-notes/3.md
- .github/actions-tmp/issue-notes/30.md
- .github/actions-tmp/issue-notes/35.md
- .github/actions-tmp/issue-notes/38.md
- .github/actions-tmp/issue-notes/4.md
- .github/actions-tmp/issue-notes/40.md
- .github/actions-tmp/issue-notes/44.md
- .github/actions-tmp/issue-notes/52.md
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
- .gitignore
- .pre-commit-config.yaml
- .vscode/README.md
- .vscode/extensions.json
- .vscode/settings.json
- LICENSE
- README.ja.md
- README.md
- _config.yml
- dev-requirements.txt
- examples/config.example.toml
- examples/monitoring-group-example.toml
- generated-docs/project-overview-generated-prompt.md
- googled947dc864c270e07.html
- issue-notes/139.md
- issue-notes/141.md
- issue-notes/62.md
- issue-notes/71.md
- issue-notes/78.md
- pytest.ini
- requirements.txt
- ruff.toml
- src/__init__.py
- src/__main__.py
- src/cat_file_watcher.py
- src/color_scheme.py
- src/command_executor.py
- src/config_loader.py
- src/config_validator.py
- src/error_logger.py
- src/external_config_merger.py
- src/file_monitor.py
- src/interval_parser.py
- src/process_detector.py
- src/repo_updater.py
- src/time_period_checker.py
- src/timestamp_printer.py
- tests/test_basics.py
- tests/test_cat_file_watcher.py
- tests/test_color_scheme_config.py
- tests/test_colorama.py
- tests/test_command_logging.py
- tests/test_command_suppression.py
- tests/test_commands_and_processes_sections.py
- tests/test_config_reload.py
- tests/test_cwd.py
- tests/test_directory_monitoring.py
- tests/test_empty_filename.py
- tests/test_empty_filename_messages.py
- tests/test_error_log_clarity.py
- tests/test_error_logging.py
- tests/test_external_files.py
- tests/test_external_files_reload.py
- tests/test_interval_parser.py
- tests/test_intervals.py
- tests/test_issue_129.py
- tests/test_main_loop_interval.py
- tests/test_multiple_empty_filenames.py
- tests/test_new_interval_format.py
- tests/test_no_focus.py
- tests/test_no_focus_validation.py
- tests/test_print_color_specification.py
- tests/test_process_detection.py
- tests/test_repo_updater.py
- tests/test_suppression_logging.py
- tests/test_terminate_if_process.py
- tests/test_terminate_if_window_title.py
- tests/test_terminate_message_color.py
- tests/test_time_periods.py
- tests/test_timestamp.py
- tests/test_timestamp_reset_on_reload.py

## 現在のオープンIssues
## [Issue #142](../issue-notes/142.md): docs: document [auto_update] TOML configuration in README.ja.md
- [x] Investigate `auto_update` TOML configuration format (result: `[auto_update]` table with `enabled` and `interval` fields)
- [x] Add `auto_update` documentation to `README.ja.md` (新セクション「自動アップデート設定」+ prerequisite notes)
- [x] Add equivalent `auto_update` section to `README.md` to keep docs in sy...
ラベル: 
--- issue-notes/142.md の内容 ---

```markdown

```

## [Issue #141](../issue-notes/141.md): issue 139の検証方法が不明確
[issue-notes/141.md](https://github.com/cat2151/cat-file-watcher/blob/main/issue-notes/141.md)

...
ラベル: 
--- issue-notes/141.md の内容 ---

```markdown
# issue issue 139の検証方法が不明確 #141
[issues #141](https://github.com/cat2151/cat-file-watcher/issues/141)



```

## ドキュメントで言及されているファイルの内容
### .github/actions-tmp/.github_automation/check-large-files/README.md
```md
{% raw %}
# Check Large Files Workflow

This reusable workflow checks for source files that exceed a configured line count threshold and automatically creates GitHub issues when large files are detected.

## Purpose

- Automatically detect files that are becoming too large
- Create or update GitHub issues with detailed information about large files
- Help maintain code quality by identifying files that may need refactoring

## Usage

### 1. (Optional) Create Configuration File

If your repository needs custom settings, create `.github/check-large-files.toml`:

Test files are included in the scan; avoid excluding them unless there's a specific reason.

```toml
[settings]
max_lines = 500
issue_labels = ["refactoring", "code-quality", "automated"]
issue_title = "大きなファイルの検出: {count}個のファイルが{max_lines}行を超えています"

[scan]
include_patterns = ["**/*"]
exclude_patterns = [
    "**/node_modules/**",
    "**/dist/**",
    "**/*.md",
    # Add more patterns as needed
    # Note: The workflow automatically excludes .github/actions-tmp/**
]
exclude_files = []
```

If no `.github/check-large-files.toml` is found in your repository, the workflow falls back to the default configuration bundled with this reusable workflow at `.github_automation/check-large-files/check-large-files.toml.default`. See that file in this repository for a complete example with common patterns.

### 2. Create Caller Workflow

Create `.github/workflows/call-check-large-files.yml` in your repository:

```yaml
name: Call Check Large Files

on:
  schedule:
    # Run daily at 3:00 AM JST (18:00 UTC)
    - cron: '0 18 * * *'
  workflow_dispatch:

permissions:
  contents: read
  issues: write

jobs:
  call-check-large-files:
    uses: cat2151/github-actions/.github/workflows/check-large-files.yml@main
```

## Configuration Options

### `settings` section

- `max_lines`: Line count threshold (files exceeding this will be reported)
- `issue_labels`: Array of labels to apply to created issues
- `issue_title`: Template for issue title (supports `{count}` and `{max_lines}` placeholders)

### `scan` section

- `include_patterns`: Glob patterns for files to check (default: `["**/*"]`)
- `exclude_patterns`: Glob patterns for files/directories to exclude
  - Common lockfiles (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `npm-shrinkwrap.json`) are excluded by default; set `scan.auto_exclude_lockfiles = false` to include them
- `exclude_files`: Specific file paths to exclude

## How It Works

1. The workflow checks out your repository
2. Checks out this shared repository to access the Python script (into `.github/actions-tmp/`, automatically excluded from scanning)
3. Runs the `check_large_files.py` script to scan for large files
4. If large files are found:
   - Checks if a similar issue already exists (by title pattern)
   - If exists: Adds a comment with updated information
   - If not: Creates a new issue with file details and recommendations

**Note**: The workflow automatically excludes the `.github/actions-tmp/**` directory where it checks out the shared repository, so you don't need to add this exclusion manually.

## Issue Format

Created issues include:

- Table of detected files with line counts and excess lines
- Recommendations for refactoring
- Automatic labels for tracking
- A warning at the top when large files exist but no test files are found, prompting you to add tests first

## Example

For a project with TypeScript files, you might want to:

```toml
[settings]
max_lines = 300  # Stricter limit for TypeScript

[scan]
include_patterns = ["src/**/*.ts", "src/**/*.tsx"]
exclude_patterns = [
    "**/*.d.ts"
]
```

## Requirements

- Python 3.11 or later
- GitHub Actions permissions: `contents: read`, `issues: write`

## Related Files

- Workflow: `.github/workflows/check-large-files.yml`
- Script: `.github_automation/check-large-files/scripts/check_large_files.py`
- Example config: `.github_automation/check-large-files/check-large-files.toml.default`

{% endraw %}
```

### .github/actions-tmp/README.md
```md
{% raw %}
# GitHub Actions Shared Workflow Collection

This repository is a **collection of GitHub Actions shared workflows reusable across multiple projects.**

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
</p>

# Summary in 3 Points
- 🚀 Simplify GitHub Actions management for individual projects.
- 🔗 With standardized workflows, just call them from any project.
- ✅ Unified maintenance allows you to focus on project development.

## Quick Links
| Item | Link |
|------|--------|
| 📖 Project Overview | [generated-docs/project-overview.md](generated-docs/project-overview.md) |
| 📖 Call Graph | [generated-docs/callgraph.html](https://cat2151.github.io/github-actions/generated-docs/callgraph.html) |
| 📊 Development Status | [generated-docs/development-status.md](generated-docs/development-status.md) |

# notes
- Still in the process of standardizing workflows.
- Still improving workflow content.

Note: README.md is automatically generated by GitHub Actions based on README.ja.md and translated by Gemini.
{% endraw %}
```

### .vscode/README.md
```md
{% raw %}
# VSCode Configuration for cat-file-watcher

This directory contains VSCode settings for the cat-file-watcher project.

## Required Extensions

Please install the following extensions for the best development experience:

1. **Python** (ms-python.python)
   - Official Python extension
   - Provides IntelliSense, linting, debugging, and more

2. **Pylance** (ms-python.vscode-pylance)
   - Fast language server for Python
   - Provides advanced type checking and auto-completion

3. **Ruff** (charliermarsh.ruff)
   - Modern, fast Python linter and formatter
   - Replaces flake8, black, and isort

4. **EditorConfig for VS Code** (editorconfig.editorconfig)
   - Applies EditorConfig settings

## Installation

Install all extensions at once using the command palette (Ctrl+Shift+P or Cmd+Shift+P):

```
Extensions: Show Recommended Extensions
```

Or install them individually from the Extensions marketplace.

## Development Dependencies

Install development dependencies:

```bash
pip install -r dev-requirements.txt
```

This will install:
- ruff: Linter and formatter
- mypy: Optional type checker
- types-toml: Type stubs for toml

## Features

### Auto-formatting on Save

Python files are automatically formatted when you save them using Ruff formatter.

### Linting

Code is continuously linted with Ruff. Issues appear in the Problems panel.

### Test Discovery

Tests are automatically discovered and can be run from the Test Explorer.

### Import Organization

Imports are automatically sorted and organized on save.

## Settings Overview

- **Line Length**: 120 characters
- **Indent**: 4 spaces for Python
- **Line Ending**: LF (Unix style)
- **Trailing Whitespace**: Automatically removed
- **Final Newline**: Automatically added

## Manual Commands

### Check code:
```bash
ruff check src/ tests/
```

### Fix issues automatically:
```bash
ruff check --fix src/ tests/
```

### Format code:
```bash
ruff format src/ tests/
```

### Run tests:
```bash
pytest tests/
```

## Troubleshooting

### Extensions not working?

1. Reload VSCode window (Ctrl+Shift+P → "Developer: Reload Window")
2. Check that Python interpreter is selected (bottom-left corner)
3. Verify extensions are installed and enabled

### Linting not showing errors?

1. Open Output panel (View → Output)
2. Select "Python" or "Ruff" from the dropdown
3. Check for error messages

## Learn More

- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [VSCode Python Documentation](https://code.visualstudio.com/docs/python/python-tutorial)
- [EditorConfig Documentation](https://editorconfig.org/)

{% endraw %}
```

### README.md
```md
{% raw %}
# cat-file-watcher - Cat is watching your file -

**File Change Monitoring Tool - Detects file changes and executes commands**

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
  <a href="https://deepwiki.com/cat2151/cat-file-watcher"><img src="https://deepwiki.com/badge.svg" alt="Ask DeepWiki"></a>
</p>

*Note: This document is largely AI-generated. It was generated by submitting issues to an agent. Some parts (concept, differentiation, test) are human-written.*

## Quick Links
| Item | Link |
|------|--------|
| 📊 Development Status | [generated-docs/development-status](generated-docs/development-status.md) |

## Overview

A file monitoring tool that observes file timestamp changes and executes commands when a file is updated.

## Features

- Monitors multiple files simultaneously
- Executes custom commands upon file changes
- Configurable via TOML configuration file
- Lightweight and easy to use
- On Windows, can execute commands without stealing focus (or by immediately regaining it).

## Installation

1. Clone this repository:
```bash
git clone https://github.com/cat2151/cat-file-watcher.git
cd cat-file-watcher
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

Get started immediately with minimal configuration! It works with **just one line in a TOML file**:

1. Create a configuration file (`config.toml`):
```toml
files = [{path = "test.txt", command = "echo File has been changed"}]
```

2. Create the file to be monitored:
```bash
touch test.txt
```

3. Start the file watcher:
```bash
python -m src --config-filename config.toml
```

That's it! This will monitor changes to `test.txt` and execute the command when a change is detected.

Try editing the file:
```bash
echo "Test" >> test.txt
```

You will see "File has been changed" displayed in the console.

**Note**: The single-line format above is a formal TOML notation using inline array representation. A more readable multi-line format is also available (see the [Configuration](#configuration) section for details).

## Usage

Run the file watcher by specifying a configuration file:

```bash
python -m src --config-filename config.toml
```

Arguments:
- `--config-filename`: Path to the TOML configuration file (required)

## Configuration

Create a TOML configuration file to define the files to watch and the commands to execute:

```toml
# Default monitoring interval
# Time format: "1s" (1 second), "2m" (2 minutes), "3h" (3 hours), "0.5s" (0.5 seconds)
default_interval = "1s"

# Interval for checking changes to the configuration file itself
config_check_interval = "1s"

# File path for command execution logs (optional)
log_file = "command_execution.log"

# File path for error logs (optional)
# error_log_file = "error.log"

# File path for command suppression logs (optional)
# suppression_log_file = "suppression.log"

# Time period definitions (optional)
[time_periods]
business_hours = { start = "09:00", end = "17:00" }
night_shift = { start = "23:00", end = "01:00" }

[files]
"myfile.txt" = { command = "echo 'File changed!'" }
"script.py" = { command = "python -m pytest tests/", interval = "2s" }
"src/main.py" = { command = "make build", suppress_if_process = "vim|emacs|code" }
"batch.csv" = { command = "./process.sh", time_period = "night_shift" }
"important.txt" = { command = "backup.sh", enable_log = true }
"lib/module.c" = { command = "gcc -c module.c -o module.o", cwd = "./lib" }
```

### Configuration Format

The configuration file requires a `[files]` section, where each entry maps a filename to a command:

- **Key**: Path to the file or directory to monitor (relative or absolute path)
  - For files: Executes the command when the file's modification timestamp changes.
  - For directories: Executes the command when the directory's modification timestamp changes (e.g., adding or deleting files).
- **Value**: An object containing a `command` field for the shell command to execute (normal mode), or an `argv` field (no_focus mode).
  - `command` (required in normal mode): The shell command to execute when the file or directory changes. **Note**: Cannot be used if `no_focus=true`.
  - `argv` (required in no_focus mode): A required array field when `no_focus=true`. Specifies the executable name and arguments as an array. Example: `argv = ["notepad.exe", "file.txt"]`
  - `interval` (optional): The monitoring interval for this file or directory. Specified in time format ("1s", "2m", "3h", "0.5s"). Decimal values are allowed (e.g., "0.5s" for 0.5 seconds). If omitted, `default_interval` will be used.
  - `suppress_if_process` (optional): A regular expression pattern to match against running process names. If a matching process is found, command execution is skipped. This is useful for preventing actions from being triggered when specific programs like editors are running.
  - `time_period` (optional): The name of the time period during which the file or directory should be monitored. Specify a time period name defined in the `[time_periods]` section. Monitoring will only occur within the specified time period.
  - `enable_log` (optional): If set to `true`, detailed command execution information will be logged to the log file (default: `false`). The `log_file` setting in the global configuration is required.
  - `cwd` (optional): Changes the working directory to the specified path before executing the command. This ensures that relative paths in the command are resolved from the specified directory.
  - `no_focus` (optional): If set to `true`, the command will be executed without stealing focus (default: `false`). **Windows-specific** - The command is launched asynchronously (the tool does not wait for completion), and the window is displayed but not activated, preventing focus from being stolen. Uses `shell=False`. On non-Windows platforms, a warning will be displayed, and execution will fall back to normal mode. **Important**: When `no_focus=true`, the `command` field cannot be used; instead, the `argv` array field is required. Example: `argv = ["notepad.exe", "file.txt"]`

### Global Settings

- `default_interval` (optional): The default monitoring interval for all files and directories. Specified in time format ("1s", "2m", "3h", "0.5s"). Decimal values are allowed (e.g., "0.5s" for 0.5 seconds). If omitted, "1s" (1 second) will be used.
- `config_check_interval` (optional): The interval for checking changes to the configuration file itself. Specified in time format ("1s", "2m", "3h", "0.5s"). If the configuration file changes, it will be automatically reloaded. If omitted, "1s" (1 second) will be used.
- `log_file` (optional): The path to the log file for recording detailed command execution information. If set, command execution details (timestamp, path, TOML configuration content) for files or directories with `enable_log = true` will be recorded in this file.
- `error_log_file` (optional): The path to the error log file for recording detailed command execution errors. If set, detailed information such as error messages upon command failure, the executed command, standard error output, and stack traces will be recorded in this file.
- `suppression_log_file` (optional): The path to the log file for recording details of command execution suppression. If set, information (timestamp, file path, process pattern, matched process) when command execution is skipped due to `suppress_if_process` will be recorded in this file.
- `color_scheme` (optional): The color scheme for terminal output. Can be `monokai` (default) or `classic`. To use custom colors, specify `green`, `yellow`, and `red` in the `[color_scheme]` table using `#RRGGBB`, `R,G,B`, `R;G;B`, `38;2;R;G;B`, or ANSI escape sequence format (e.g., `\x1b[38;2;255;60;80m`).

### Time Period Configuration

You can define time periods in the `[time_periods]` section (optional):

- Each time period is defined with a name.
- `start`: Start time (HH:MM format, e.g., "09:00")
- `end`: End time (HH:MM format, e.g., "17:00")
- Time periods spanning across midnight are also supported (e.g., `start = "23:00", end = "01:00"`).
- By specifying a time period name using the `time_period` parameter for each file, that file or directory will only be monitored within that designated time period.

Example:
```toml
[time_periods]
business_hours = { start = "09:00", end = "17:00" }  # Regular business hours
night_shift = { start = "23:00", end = "01:00" }     # Time period spanning across midnight
```

### Configuration Example

Refer to `examples/config.example.toml` for a complete example with various use cases.

```toml
# Set default monitoring interval to 1 second
default_interval = "1s"

# Set configuration file change check interval to 1 second
config_check_interval = "1s"

# Log file for detailed command execution (optional)
log_file = "command_execution.log"

# Error log file (optional)
# error_log_file = "error.log"

# Command suppression log file (optional)
# suppression_log_file = "suppression.log"

# Time period definitions
[time_periods]
business_hours = { start = "09:00", end = "17:00" }
after_hours = { start = "18:00", end = "08:00" }  # Spans across midnight

[files]
# Use default interval (checks every 1 second)
"document.txt" = { command = "cp document.txt document.txt.bak" }

# Specify custom interval (checks every 0.5 seconds)
"app.log" = { command = "notify-send 'Log Updated' 'New entries in app.log'", interval = "0.5s" }

# Specify custom interval (checks every 5 seconds)
"config.ini" = { command = "systemctl reload myapp", interval = "5s" }

# Monitor only during business hours
"report.txt" = { command = "python generate_report.py", time_period = "business_hours" }

# Monitor only outside business hours (e.g., for batch processing)
"batch.csv" = { command = "./process_batch.sh", time_period = "after_hours" }

# Enable logging for important files (records timestamp, file path, configuration content)
"important.txt" = { command = "backup.sh", enable_log = true }
```

## How It Works

1. The tool reads the TOML configuration file.
2. It monitors the modification timestamps of all specified files.
3. When a file's timestamp changes, it executes the associated command.
4. It also monitors the configuration file itself and automatically reloads it if changes occur.
5. This process continuously repeats until stopped by Ctrl+C.

### Command Execution Handling

**Important**: Commands are executed **sequentially**.

- When a file change is detected and a command is executed, the next file check will not occur until that command completes (or times out after 30 seconds for foreground execution).
- For example, if a command for a particular file takes 25 seconds, monitoring of other files will be paused for those 25 seconds.
- Even if other files are updated during this time, they will not be detected until the currently running command completes (they will be detected in the next main loop after the command finishes).
- The current implementation does not support parallel monitoring and execution for multiple files.

For commands that require long execution times, it's necessary to either run them in the background within the command itself or launch them as a separate process.

**Methods for Non-Blocking Execution**:
- **Linux/macOS**: Append `&` to the end of the command (e.g., `command = "long_task.sh &"`).
- **Windows**: Prepend `start ` to the command (e.g., `command = "start long_task.bat"`).

### Command Execution Output

The standard output and standard error of executed commands are displayed in the console **in real-time**:

- **Output Display**: The standard output and standard error of commands are sequentially displayed in the console during execution. You can check the progress of even long-running commands in real-time.
- **On Failure**: If a command fails (exit code other than 0), a message like `Error: Command failed for '<file_path>' with exit code <code_number>` will be displayed.
- **Error Log File**: If `error_log_file` is configured, error messages and executed commands upon command failure will be recorded in the log file.

Commands executed in the foreground have a 30-second timeout; exceeding this will result in a timeout error. For commands requiring longer execution, please use background execution (using `&`). Commands executed in the background are not subject to the timeout limit because `subprocess.run()` completes immediately.

## Concept

Prioritizes simple and maintainable TOML descriptions.

## Use Cases

Use cat-file-watcher when you want to easily monitor file updates and operate with minimal effort.

Use cat-file-watcher when you need to quickly toggle update monitoring on/off for scattered files.

Use cat-file-watcher if you want to leverage its unique features.

For more advanced features, consider other applications.

For TypeScript application development, etc., a standard task runner is recommended.

## Development

### Environment Setup

To set up the development environment:

```bash
# Install dependencies (for runtime environment)
pip install -r requirements.txt

# Install development dependencies (including Ruff)
pip install -r dev-requirements.txt
```

### Code Quality Checks

This project uses [Ruff](https://docs.astral.sh/ruff/) to maintain code quality.

#### Running Ruff

```bash
# Run linter checks
ruff check src/

# Fix automatically fixable issues
ruff check --fix src/

# Check code formatting
ruff format --check src/

# Apply code formatting
ruff format src/
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v
```

- Linux
  - All tests are designed for Linux.
  - GitHub Copilot Coding Agent generated the test code and performed TDD on GitHub Actions (Linux Runner).

- Windows
  - Running tests in a Windows environment without WSL2 will frequently result in failed tests. This is because the tests are designed for Linux.
  - To run tests in a Windows environment, use WSL2.
  - Specifically, install WSL2, then prepare by running `wsl pip install -r dev-requirements.txt`, and finally `wsl pytest`.
  - Some tests might still fail on WSL2, but this is acceptable. The criterion is that if TDD resulted in passing tests when an issue was submitted to the agent, it was considered okay.

## License

MIT License - See the LICENSE file for details

*Note: The English README.md is automatically generated from README.ja.md via Gemini translation using GitHub Actions.*

*Big Brother watched your files. Now the cat does. 🐱*
{% endraw %}
```

### .github/actions-tmp/README.ja.md
```md
{% raw %}
# GitHub Actions 共通ワークフロー集

このリポジトリは、**複数プロジェクトで使い回せるGitHub Actions共通ワークフロー集**です

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
</p>

# 3行で説明
- 🚀 プロジェクトごとのGitHub Actions管理をもっと楽に
- 🔗 共通化されたワークフローで、どのプロジェクトからも呼ぶだけでOK
- ✅ メンテは一括、プロジェクト開発に集中できます

## Quick Links
| 項目 | リンク |
|------|--------|
| 📖 プロジェクト概要 | [generated-docs/project-overview.md](generated-docs/project-overview.md) |
| 📖 コールグラフ | [generated-docs/callgraph.html](https://cat2151.github.io/github-actions/generated-docs/callgraph.html) |
| 📊 開発状況 | [generated-docs/development-status.md](generated-docs/development-status.md) |

# notes
- まだ共通化の作業中です
- まだワークフロー内容を改善中です

※README.md は README.ja.md を元にGeminiの翻訳でGitHub Actionsで自動生成しています

{% endraw %}
```

### README.ja.md
```md
{% raw %}
# cat-file-watcher - Cat is watching your file -

**ファイル変更監視ツール - ファイルの変更を検知してコマンドを実行**

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
  <a href="https://deepwiki.com/cat2151/cat-file-watcher"><img src="https://deepwiki.com/badge.svg" alt="Ask DeepWiki"></a>
</p>

※このドキュメントは大部分がAI生成です。issueをagentに投げて生成させました。一部（コンセプト、使い分け、test）は人力で書いています

## Quick Links
| 項目 | リンク |
|------|--------|
| 📊 開発状況 | [generated-docs/development-status](generated-docs/development-status.md) |

## 概要

ファイルのタイムスタンプの変更を監視し、ファイルが更新されたときにコマンドを実行するファイル監視ツールです。

## 特徴

- 複数のファイルを同時に監視
- ファイル変更時にカスタムコマンドを実行
- TOML設定ファイルで設定可能
- 軽量で使いやすい
- Windowsで、起動したアプリにフォーカスを奪われない（厳密にはすぐ奪い返す）設定可

## インストール

1. このリポジトリをクローン:
```bash
git clone https://github.com/cat2151/cat-file-watcher.git
cd cat-file-watcher
```

2. 依存パッケージをインストール:
```bash
pip install -r requirements.txt
```

## クイックスタート

最小限の設定で今すぐ始めましょう！**たった1行のTOMLファイル**で動作します:

1. 設定ファイルを作成（`config.toml`）:
```toml
files = [{path = "test.txt", command = "echo ファイルが変更されました"}]
```

2. 監視対象のファイルを作成:
```bash
touch test.txt
```

3. ファイルウォッチャーを起動:
```bash
python -m src --config-filename config.toml
```

これだけで、`test.txt` の変更を監視し、変更があればコマンドを実行します！

ファイルを編集してみてください:
```bash
echo "テスト" >> test.txt
```

コンソールに「ファイルが変更されました」と表示されます。

**ポイント**: 上記の1行形式は、インライン配列表記を使ったTOMLの正式な記法です。より読みやすい複数行形式も使えます（詳細は[設定](#設定)セクションを参照）。

## 使い方

設定ファイルを指定してファイルウォッチャーを実行:

```bash
python -m src --config-filename config.toml
```

引数:
- `--config-filename`: TOML設定ファイルのパス（必須）

## 設定

監視するファイルと実行するコマンドを定義するTOML設定ファイルを作成します:

```toml
# デフォルトの監視間隔
# 時間フォーマット: "1s"（1秒）、"2m"（2分）、"3h"（3時間）、"0.5s"（0.5秒）
default_interval = "1s"

# 設定ファイル自体の変更チェック間隔
config_check_interval = "1s"

# コマンド実行ログのファイルパス（省略可）
log_file = "command_execution.log"

# エラーログのファイルパス（省略可）
# error_log_file = "error.log"

# コマンド実行抑制ログのファイルパス（省略可）
# suppression_log_file = "suppression.log"

# 時間帯の定義（省略可）
[time_periods]
business_hours = { start = "09:00", end = "17:00" }
night_shift = { start = "23:00", end = "01:00" }

[files]
"myfile.txt" = { command = "echo 'File changed!'" }
"script.py" = { command = "python -m pytest tests/", interval = "2s" }
"src/main.py" = { command = "make build", suppress_if_process = "vim|emacs|code" }
"batch.csv" = { command = "./process.sh", time_period = "night_shift" }
"important.txt" = { command = "backup.sh", enable_log = true }
"lib/module.c" = { command = "gcc -c module.c -o module.o", cwd = "./lib" }
```

### 設定フォーマット

設定ファイルには、各エントリがファイル名とコマンドをマッピングする `[files]` セクションが必要です:

- **キー**: 監視するファイルまたはディレクトリのパス（相対パスまたは絶対パス）
  - ファイルの場合: ファイルの変更時刻が変わったときにコマンドを実行
  - ディレクトリの場合: ディレクトリの変更時刻が変わったとき（ファイルの追加・削除など）にコマンドを実行
- **値**: 実行するシェルコマンドを含む `command` フィールドを持つオブジェクト（通常モード）、または `argv` フィールドを持つオブジェクト（no_focusモード）
  - `command` (通常モードで必須): ファイルまたはディレクトリ変更時に実行するシェルコマンド。**注意**: `no_focus=true` の場合は使用できません
  - `argv` (no_focusモードで必須): `no_focus=true` の場合に必須の配列フィールド。実行ファイル名と引数を配列として指定します。例: `argv = ["notepad.exe", "file.txt"]`
  - `interval` (省略可): このファイルまたはディレクトリの監視間隔。時間フォーマット（"1s", "2m", "3h", "0.5s"）で指定します。小数点も使用可能です（例: "0.5s"は0.5秒）。省略した場合は `default_interval` が使用されます
  - `suppress_if_process` (省略可): 実行中のプロセス名にマッチする正規表現パターン。マッチするプロセスが見つかった場合、コマンド実行をスキップします。エディタなどの特定のプログラムが実行中の場合にアクションをトリガーしないようにする場合に便利です
  - `time_period` (省略可): ファイルまたはディレクトリを監視する時間帯の名前。`[time_periods]` セクションで定義された時間帯名を指定します。指定した時間帯内でのみ監視します
  - `enable_log` (省略可): `true` に設定すると、コマンド実行の詳細をログファイルに記録します（デフォルト: `false`）。グローバル設定で `log_file` の設定が必要です
  - `cwd` (省略可): コマンドを実行する前に指定されたパスに作業ディレクトリを変更します。これにより、コマンド内の相対パスが指定されたディレクトリから解決されます
  - `no_focus` (省略可): `true` に設定すると、フォーカスを奪わずにコマンドを実行します（デフォルト: `false`）。**Windows専用** - コマンドは非同期で起動され（ツールは完了を待機しません）、ウィンドウは表示されますがアクティブ化されないため、フォーカスの奪取を防ぎます。`shell=False` を使用します。Windows以外のプラットフォームでは、警告を表示して通常実行にフォールバックします。**重要**: `no_focus=true` の場合、`command` フィールドは使用できず、代わりに `argv` 配列フィールドが必須です。例: `argv = ["notepad.exe", "file.txt"]`

### グローバル設定

- `default_interval` (省略可): すべてのファイルおよびディレクトリのデフォルト監視間隔。時間フォーマット（"1s", "2m", "3h", "0.5s"）で指定します。小数点も使用可能です（例: "0.5s"は0.5秒）。省略した場合は"1s"（1秒）が使用されます
- `config_check_interval` (省略可): 設定ファイル自体の変更チェック間隔。時間フォーマット（"1s", "2m", "3h", "0.5s"）で指定します。設定ファイルが変更されると自動的に再読み込みされます。省略した場合は"1s"（1秒）が使用されます
- `log_file` (省略可): コマンド実行の詳細を記録するログファイルのパス。設定すると、`enable_log = true` が指定されたファイルまたはディレクトリのコマンド実行情報（タイムスタンプ、パス、TOML設定内容）がこのファイルに記録されます
- `error_log_file` (省略可): コマンド実行エラーの詳細を記録するエラーログファイルのパス。設定すると、コマンド失敗時のエラーメッセージ、実行コマンド、標準エラー出力、スタックトレースなどの詳細情報がこのファイルに記録されます
- `suppression_log_file` (省略可): コマンド実行抑制の詳細を記録するログファイルのパス。設定すると、`suppress_if_process` によりコマンド実行がスキップされた際の情報（タイムスタンプ、ファイルパス、プロセスパターン、マッチしたプロセス）がこのファイルに記録されます
- `color_scheme` (省略可): ターミナル出力の配色。`monokai`（デフォルト）または`classic`を指定できます。カスタム色を使う場合は `[color_scheme]` テーブルで `green`、`yellow`、`red` を `#RRGGBB`、`R,G,B`、`R;G;B`、`38;2;R;G;B`、または ANSI エスケープシーケンス（例: `\x1b[38;2;255;60;80m`）形式で指定してください。


### 時間帯設定

`[time_periods]` セクション（省略可）で時間帯を定義できます:

- 各時間帯は名前を付けて定義します
- `start`: 開始時刻（HH:MM形式、例: "09:00"）
- `end`: 終了時刻（HH:MM形式、例: "17:00"）
- 日をまたぐ時間帯もサポート（例: `start = "23:00", end = "01:00"`）
- ファイルごとに `time_period` パラメータで時間帯名を指定すると、その時間帯内でのみそのファイルまたはディレクトリを監視します

例:
```toml
[time_periods]
business_hours = { start = "09:00", end = "17:00" }  # 通常の時間帯
night_shift = { start = "23:00", end = "01:00" }     # 日をまたぐ時間帯
```

### 設定例

様々なユースケースの完全な例は `examples/config.example.toml` を参照してください。

```toml
# デフォルトの監視間隔を1秒に設定
default_interval = "1s"

# 設定ファイル自体の変更チェック間隔を1秒に設定
config_check_interval = "1s"

# コマンド実行の詳細を記録するログファイル（省略可）
log_file = "command_execution.log"

# エラーログファイル（省略可）
# error_log_file = "error.log"

# コマンド実行抑制ログファイル（省略可）
# suppression_log_file = "suppression.log"

# 時間帯の定義
[time_periods]
business_hours = { start = "09:00", end = "17:00" }
after_hours = { start = "18:00", end = "08:00" }  # 日をまたぐ

[files]
# デフォルト間隔を使用（1秒ごとにチェック）
"document.txt" = { command = "cp document.txt document.txt.bak" }

# カスタム間隔を指定（0.5秒ごとにチェック）
"app.log" = { command = "notify-send 'Log Updated' 'New entries in app.log'", interval = "0.5s" }

# カスタム間隔を指定（5秒ごとにチェック）
"config.ini" = { command = "systemctl reload myapp", interval = "5s" }

# 営業時間のみ監視
"report.txt" = { command = "python generate_report.py", time_period = "business_hours" }

# 営業時間外のみ監視（バッチ処理など）
"batch.csv" = { command = "./process_batch.sh", time_period = "after_hours" }

# 重要なファイルのログを有効化（タイムスタンプ、ファイルパス、設定内容を記録）
"important.txt" = { command = "backup.sh", enable_log = true }
```

## 動作の仕組み

1. ツールがTOML設定ファイルを読み込みます
2. 指定されたすべてのファイルの更新タイムスタンプを監視します
3. ファイルのタイムスタンプが変更されると、関連するコマンドを実行します
4. 設定ファイル自体も監視し、変更があれば自動的に再読み込みします
5. このプロセスはCtrl+Cで停止するまで継続的に繰り返されます

### コマンド実行の処理方式

**重要**: コマンドは**順次実行（シーケンシャル）**されます。

- ファイルの変更を検知してコマンドを実行する際、そのコマンドが完了（またはフォアグラウンド実行の場合は30秒のタイムアウト）するまで、次のファイルのチェックは行われません
- 例えば、あるファイルのコマンドが25秒かかる場合、その25秒間は他のファイルの監視は一時停止します
- この間に他のファイルが更新されても、実行中のコマンドが完了するまで検知されません（コマンド完了後、次のメインループで検知されます）
- 現在の実装では、複数ファイルの監視・実行を並列化する機能はサポートされていません

長時間実行が必要なコマンドの場合は、コマンド内でバックグラウンド実行するか、別プロセスで起動する工夫が必要です。

**ノンブロッキング実行の方法**:
- **Linux/macOS**: コマンドの末尾に `&` を付ける（例: `command = "long_task.sh &"`）
- **Windows**: コマンドの先頭に `start ` を付ける（例: `command = "start long_task.bat"`）

### コマンド実行時の出力

実行されたコマンドの標準出力および標準エラー出力は、**リアルタイムで**コンソールに表示されます:

- **出力表示**: コマンドの標準出力と標準エラー出力は、実行中に逐次コンソールに表示されます。長時間実行されるコマンドでも、途中経過をリアルタイムで確認できます
- **失敗時**: コマンドが失敗した場合（終了コード 0以外）、`Error: Command failed for '<ファイルパス>' with exit code <コード>` というメッセージが表示されます
- **エラーログファイル**: `error_log_file` を設定している場合、コマンド失敗時のエラーメッセージと実行コマンドがログファイルに記録されます

フォアグラウンドで実行されるコマンドのタイムアウトは30秒に設定されており、それを超えるとタイムアウトエラーが発生します。長時間実行が必要なコマンドの場合は、バックグラウンド実行（`&` を使用）してください。バックグラウンド実行されたコマンドは、subprocess.run()が即座に完了するため、タイムアウトの制限を受けません。

## コンセプト

toml記述内容がシンプルでメンテしやすいことを優先します

## 使い分け

手軽にファイル更新監視したい場合、楽に運用したい場合は、cat-file-watcher

散在するファイルを手早く更新監視on/offしたい場合は、cat-file-watcher

これにしかない各種機能を利用したい場合は、cat-file-watcher

もっと高度な機能を使いたい場合は、ほかのアプリ

TypeScriptアプリ開発等には、スタンダードにタスクランナー

## 開発

### 環境構築

開発環境のセットアップ:

```bash
# 依存パッケージのインストール（実行環境用）
pip install -r requirements.txt

# 開発用依存パッケージのインストール（Ruffを含む）
pip install -r dev-requirements.txt
```

### コード品質チェック

このプロジェクトでは、コード品質を保つために[Ruff](https://docs.astral.sh/ruff/)を使用しています。

#### Ruffの実行

```bash
# リンターチェック
ruff check src/

# 自動修正可能な問題を修正
ruff check --fix src/

# コードフォーマットのチェック
ruff format --check src/

# コードフォーマットを適用
ruff format src/
```

### テストの実行

```bash
# 全テストの実行
pytest

# 詳細出力付きでテストを実行
pytest -v
```

- Linux
  - テストはすべてLinux用です。
  - GitHub Copilot Coding Agentが、
GitHub Actions（Linux Runner）上でテストコードを生成し
TDDしたものです。

- Windows
  - Windows環境でWSL2を使わずテストをするとtest redが多発します。これはテストがLinux用であるためです。
  - Windows環境でテストするには、WSL2を使います。
  - 具体的には、WSL2をinstallして、`wsl pip install -r dev-requirements.txt` で準備してから、
`wsl pytest` します。
  - WSL2だといくつかtest redになることがありますが許容しています。issueをagentに投げたときTDDしてtest greenであればOK、を基準としています。

## ライセンス

MIT License - 詳細はLICENSEファイルを参照してください

※英語版README.mdは、README.ja.mdを元にGeminiの翻訳でGitHub Actionsにより自動生成しています

*Big Brother watched your files. Now the cat does. 🐱*

{% endraw %}
```

### .github/actions-tmp/issue-notes/2.md
```md
{% raw %}
# issue GitHub Actions「関数コールグラフhtmlビジュアライズ生成」を共通ワークフロー化する #2
[issues #2](https://github.com/cat2151/github-actions/issues/2)


# prompt
```
あなたはGitHub Actionsと共通ワークフローのスペシャリストです。
このymlファイルを、以下の2つのファイルに分割してください。
1. 共通ワークフロー       cat2151/github-actions/.github/workflows/callgraph_enhanced.yml
2. 呼び出し元ワークフロー cat2151/github-actions/.github/workflows/call-callgraph_enhanced.yml
まずplanしてください
```

# 結果
- indent
    - linter？がindentのエラーを出しているがyml内容は見た感じOK
    - テキストエディタとagentの相性問題と判断する
    - 別のテキストエディタでsaveしなおし、テキストエディタをreload
    - indentのエラーは解消した
- LLMレビュー
    - agent以外の複数のLLMにレビューさせる
    - prompt
```
あなたはGitHub Actionsと共通ワークフローのスペシャリストです。
以下の2つのファイルをレビューしてください。最優先で、エラーが発生するかどうかだけレビューしてください。エラー以外の改善事項のチェックをするかわりに、エラー発生有無チェックに最大限注力してください。

--- 共通ワークフロー

# GitHub Actions Reusable Workflow for Call Graph Generation
name: Generate Call Graph

# TODO Windowsネイティブでのtestをしていた名残が残っているので、今後整理していく。今はWSL act でtestしており、Windowsネイティブ環境依存問題が解決した
#  ChatGPTにレビューさせるとそこそこ有用そうな提案が得られたので、今後それをやる予定
#  agentに自己チェックさせる手も、セカンドオピニオンとして選択肢に入れておく

on:
  workflow_call:

jobs:
  check-commits:
    runs-on: ubuntu-latest
    outputs:
      should-run: ${{ steps.check.outputs.should-run }}
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 50 # 過去のコミットを取得

      - name: Check for user commits in last 24 hours
        id: check
        run: |
          node .github/scripts/callgraph_enhanced/check-commits.cjs

  generate-callgraph:
    needs: check-commits
    if: needs.check-commits.outputs.should-run == 'true'
    runs-on: ubuntu-latest
    permissions:
      contents: write
      security-events: write
      actions: read

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set Git identity
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"

      - name: Remove old CodeQL packages cache
        run: rm -rf ~/.codeql/packages

      - name: Check Node.js version
        run: |
          node .github/scripts/callgraph_enhanced/check-node-version.cjs

      - name: Install CodeQL CLI
        run: |
          wget https://github.com/github/codeql-cli-binaries/releases/download/v2.22.1/codeql-linux64.zip
          unzip codeql-linux64.zip
          sudo mv codeql /opt/codeql
          echo "/opt/codeql" >> $GITHUB_PATH

      - name: Install CodeQL query packs
        run: |
          /opt/codeql/codeql pack install .github/codeql-queries

      - name: Check CodeQL exists
        run: |
          node .github/scripts/callgraph_enhanced/check-codeql-exists.cjs

      - name: Verify CodeQL Configuration
        run: |
          node .github/scripts/callgraph_enhanced/analyze-codeql.cjs verify-config

      - name: Remove existing CodeQL DB (if any)
        run: |
          rm -rf codeql-db

      - name: Perform CodeQL Analysis
        run: |
          node .github/scripts/callgraph_enhanced/analyze-codeql.cjs analyze

      - name: Check CodeQL Analysis Results
        run: |
          node .github/scripts/callgraph_enhanced/analyze-codeql.cjs check-results

      - name: Debug CodeQL execution
        run: |
          node .github/scripts/callgraph_enhanced/analyze-codeql.cjs debug

      - name: Wait for CodeQL results
        run: |
          node -e "setTimeout(()=>{}, 10000)"

      - name: Find and process CodeQL results
        run: |
          node .github/scripts/callgraph_enhanced/find-process-results.cjs

      - name: Generate HTML graph
        run: |
          node .github/scripts/callgraph_enhanced/generate-html-graph.cjs

      - name: Copy files to generated-docs and commit results
        run: |
          node .github/scripts/callgraph_enhanced/copy-commit-results.cjs

--- 呼び出し元
# 呼び出し元ワークフロー: call-callgraph_enhanced.yml
name: Call Call Graph Enhanced

on:
  schedule:
    # 毎日午前5時(JST) = UTC 20:00前日
    - cron: '0 20 * * *'
  workflow_dispatch:

jobs:
  call-callgraph-enhanced:
    # uses: cat2151/github-actions/.github/workflows/callgraph_enhanced.yml
    uses: ./.github/workflows/callgraph_enhanced.yml # ローカルでのテスト用
```

# レビュー結果OKと判断する
- レビュー結果を人力でレビューした形になった

# test
- #4 同様にローカル WSL + act でtestする
- エラー。userのtest設計ミス。
  - scriptの挙動 : src/ がある前提
  - 今回の共通ワークフローのリポジトリ : src/ がない
  - 今回testで実現したいこと
    - 仮のソースでよいので、関数コールグラフを生成させる
  - 対策
    - src/ にダミーを配置する
- test green
  - ただしcommit pushはしてないので、html内容が0件NG、といったケースの検知はできない
  - もしそうなったら別issueとしよう

# test green

# commit用に、yml 呼び出し元 uses をlocal用から本番用に書き換える

# closeとする
- もしhtml内容が0件NG、などになったら、別issueとするつもり

{% endraw %}
```

### issue-notes/141.md
```md
{% raw %}
# issue issue 139の検証方法が不明確 #141
[issues #141](https://github.com/cat2151/cat-file-watcher/issues/141)



{% endraw %}
```

## 最近の変更（過去7日間）
### コミット履歴:
ca33ac7 Add issue note for #141 [auto]
f1130c4 Merge pull request #140 from cat2151/copilot/check-repo-updates-hourly
52fbf78 Address review feedback: immediate check, OSError in restart, finally block for stop
1857846 Add auto-update feature: background thread checks repo every 1h (issue #139)
f62c38f Initial plan
3b6b6f7 Update project summaries (overview & development status) [auto]
dd98612 Merge pull request #138 from cat2151/copilot/fix-no-command-warning
e7fffda Enhance issue notes for automatic updates feature
58270e3 Add issue note for #139 [auto]
3bb394a Fix: no_focus=true with argv causes false 'No command specified' warning

### 変更されたファイル:
generated-docs/development-status-generated-prompt.md
generated-docs/development-status.md
generated-docs/project-overview-generated-prompt.md
generated-docs/project-overview.md
issue-notes/117.md
issue-notes/119.md
issue-notes/121.md
issue-notes/123.md
issue-notes/125.md
issue-notes/127.md
issue-notes/129.md
issue-notes/131.md
issue-notes/133.md
issue-notes/135.md
issue-notes/139.md
issue-notes/141.md
src/cat_file_watcher.py
src/file_monitor.py
src/repo_updater.py
tests/test_no_focus_validation.py
tests/test_repo_updater.py


---
Generated at: 2026-03-04 07:03:34 JST

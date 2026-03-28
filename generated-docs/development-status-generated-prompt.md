Last updated: 2026-03-29

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
- .github/actions-tmp/.github/workflows/call-rust-fmt-commit.yml
- .github/actions-tmp/.github/workflows/call-rust-windows-cargo-check.yml
- .github/actions-tmp/.github/workflows/call-rust-windows-check.yml
- .github/actions-tmp/.github/workflows/call-translate-readme.yml
- .github/actions-tmp/.github/workflows/callgraph.yml
- .github/actions-tmp/.github/workflows/check-large-files.yml
- .github/actions-tmp/.github/workflows/check-recent-human-commit.yml
- .github/actions-tmp/.github/workflows/daily-project-summary.yml
- .github/actions-tmp/.github/workflows/issue-note.yml
- .github/actions-tmp/.github/workflows/rust-fmt-commit.yml
- .github/actions-tmp/.github/workflows/rust-windows-cargo-check.yml
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
- .github/actions-tmp/AGENTS.md
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
- .github/actions-tmp/issue-notes/57.md
- .github/actions-tmp/issue-notes/67.md
- .github/actions-tmp/issue-notes/7.md
- .github/actions-tmp/issue-notes/8.md
- .github/actions-tmp/issue-notes/9.md
- .github/actions-tmp/package-lock.json
- .github/actions-tmp/package.json
- .github/actions-tmp/src/main.js
- .github/copilot-instructions.md
- .github/workflows/call-check-large-files.yml
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
- issue-notes/145.md
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
## [Issue #147](../issue-notes/147.md): 大きなファイルの検出: 1個のファイルが500行を超えています
以下のファイルが500行を超えています。リファクタリングを検討してください。

## 検出されたファイル

| ファイル | 行数 | 超過行数 |
|---------|------|----------|
| `tests/test_terminate_if_process.py` | 544 | +44 |

## テスト実施のお願い

- リファクタリング前後にテストを実行し、それぞれのテスト失敗件数を報告してください
- リファクタリング前後のどちらかでテストがredの場合、まず別issueでtest greenにしてからリファクタリングしてください

## 推奨事項

1. 単一責...
ラベル: refactoring, code-quality, automated
--- issue-notes/147.md の内容 ---

```markdown

```

## ドキュメントで言及されているファイルの内容
### .github/actions-tmp/issue-notes/7.md
```md
{% raw %}
# issue issue note生成できるかのtest用 #7
[issues #7](https://github.com/cat2151/github-actions/issues/7)

- 生成できた
- closeとする

{% endraw %}
```

### tests/test_terminate_if_process.py
```py
{% raw %}
#!/usr/bin/env python3
"""
Test cases for terminate_if_process functionality
"""

import os
import shutil
import subprocess
import sys
import tempfile
import time

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from cat_file_watcher import FileWatcher
from process_detector import ProcessDetector


class TestTerminateIfProcess:
    """Test cases for terminate_if_process functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, "test_config.toml")
        self.error_log_file = os.path.join(self.test_dir, "error.log")

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_terminate_single_process(self):
        """Test that a single matching process is terminated."""
        # Start a long-running test process
        test_script = os.path.join(self.test_dir, "test_process.py")
        with open(test_script, "w") as f:
            f.write("import time\nwhile True:\n    time.sleep(0.1)\n")

        # Start the process
        proc = subprocess.Popen([sys.executable, test_script])
        time.sleep(0.2)  # Give it time to start

        try:
            # Verify process is running
            assert proc.poll() is None, "Test process should be running"

            # Create config with terminate_if_process
            config_content = f"""default_interval = "0.05s"
error_log_file = "{self.error_log_file}"

[[files]]
path = ""
terminate_if_process = "test_process\\\\.py"
"""
            with open(self.config_file, "w") as f:
                f.write(config_content)

            watcher = FileWatcher(self.config_file)

            # Execute check - should terminate the process
            watcher._check_files()

            # Wait a bit for termination to complete
            time.sleep(0.5)

            # Verify process was terminated
            assert proc.poll() is not None, "Process should have been terminated"
        finally:
            # Cleanup: ensure process is killed if still running
            if proc.poll() is None:
                proc.kill()
                proc.wait()

    def test_terminate_no_matching_process(self):
        """Test that no action is taken when no process matches."""
        # Create config with terminate_if_process for non-existent process
        config_content = f"""default_interval = "0.05s"
error_log_file = "{self.error_log_file}"

[[files]]
path = ""
terminate_if_process = "nonexistent_process_xyz123"
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # Execute check - should do nothing (no error)
        watcher._check_files()

        # No assertion needed - just verify it doesn't crash

    def test_terminate_multiple_processes_with_single_pattern(self):
        """Test that warning is issued and no termination occurs when multiple processes match a single pattern."""
        # Start multiple test processes
        test_script = os.path.join(self.test_dir, "test_multi.py")
        with open(test_script, "w") as f:
            f.write("import time\nwhile True:\n    time.sleep(0.1)\n")

        # Start two processes
        proc1 = subprocess.Popen([sys.executable, test_script])
        proc2 = subprocess.Popen([sys.executable, test_script])
        time.sleep(0.2)  # Give them time to start

        try:
            # Create config with terminate_if_process
            config_content = f"""default_interval = "0.05s"
error_log_file = "{self.error_log_file}"

[[files]]
path = ""
terminate_if_process = "test_multi\\\\.py"
"""
            with open(self.config_file, "w") as f:
                f.write(config_content)

            watcher = FileWatcher(self.config_file)

            # Execute check - should issue warning but not terminate
            watcher._check_files()

            # Wait a bit
            time.sleep(0.5)

            # Verify both processes are still running (safety check worked)
            assert proc1.poll() is None, "First process should still be running (not terminated)"
            assert proc2.poll() is None, "Second process should still be running (not terminated)"

            # Verify warning was logged
            assert os.path.exists(self.error_log_file), "Error log should exist"
            with open(self.error_log_file, "r") as f:
                log_content = f.read()
            assert "Found 2 processes" in log_content, "Warning about multiple processes should be logged"
        finally:
            # Cleanup: ensure processes are killed
            for proc in [proc1, proc2]:
                if proc.poll() is None:
                    proc.kill()
                    proc.wait()

    def test_terminate_with_filename_error(self):
        """Test that error is raised when terminate_if_process is used with non-empty filename."""
        test_file = os.path.join(self.test_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("test content\n")

        # Create config with terminate_if_process on non-empty filename
        config_content = f"""default_interval = "0.05s"
error_log_file = "{self.error_log_file}"

[[files]]
path = "{test_file}"
terminate_if_process = "python"

"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # Execute check - should log fatal error and continue
        watcher._check_files()

        # Verify error was logged
        assert os.path.exists(self.error_log_file), "Error log should exist"
        with open(self.error_log_file, "r") as f:
            log_content = f.read()
        assert "Fatal configuration error" in log_content, "Fatal error should be logged"
        assert "empty filename" in log_content, "Error should mention empty filename requirement"

    def test_terminate_with_command_error(self):
        """Test that error is raised when terminate_if_process is used with command field."""
        # Create config with both terminate_if_process and command
        config_content = f"""default_interval = "0.05s"
error_log_file = "{self.error_log_file}"

[[files]]
path = ""
command = "echo 'test'"
terminate_if_process = "python"
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # Execute check - should log fatal error and continue
        watcher._check_files()

        # Verify error was logged
        assert os.path.exists(self.error_log_file), "Error log should exist"
        with open(self.error_log_file, "r") as f:
            log_content = f.read()
        assert "Fatal configuration error" in log_content, "Fatal error should be logged"
        assert "command must be empty" in log_content, "Error should mention command must be empty"

    def test_terminate_respects_interval(self):
        """Test that terminate_if_process respects interval timing."""
        # Start a test process
        test_script = os.path.join(self.test_dir, "test_interval.py")
        with open(test_script, "w") as f:
            f.write("import time\nwhile True:\n    time.sleep(0.1)\n")

        proc = subprocess.Popen([sys.executable, test_script])
        time.sleep(0.2)

        try:
            # Create config with custom interval
            config_content = f"""default_interval = "10s"
error_log_file = "{self.error_log_file}"

[[files]]
path = ""
terminate_if_process = "test_interval\\\\.py"
interval = "10s"
"""
            with open(self.config_file, "w") as f:
                f.write(config_content)

            watcher = FileWatcher(self.config_file)

            # First check - should terminate
            watcher._check_files()
            time.sleep(0.3)

            # Verify process was terminated
            assert proc.poll() is not None, "Process should be terminated after first check"

            # Start another process
            proc2 = subprocess.Popen([sys.executable, test_script])
            time.sleep(0.2)

            # Second check immediately - should NOT check yet (interval not met)
            watcher._check_files()
            time.sleep(0.1)

            # Process should still be running (interval not met - we set it to 10s)
            assert proc2.poll() is None, "Process should still be running (interval not met)"

            # Cleanup the second process
            if proc2.poll() is None:
                proc2.kill()
                proc2.wait()
        finally:
            # Cleanup
            if proc.poll() is None:
                proc.kill()
                proc.wait()
            if "proc2" in locals() and proc2.poll() is None:
                proc2.kill()
                proc2.wait()

    def test_terminate_multiple_process_patterns_array(self):
        """Test that terminate_if_process can accept an array of patterns, with safety check per pattern."""
        # Start multiple different test processes
        test_script1 = os.path.join(self.test_dir, "test_proc_a.py")
        with open(test_script1, "w") as f:
            f.write("import time\nwhile True:\n    time.sleep(0.1)\n")

        test_script2 = os.path.join(self.test_dir, "test_proc_b.py")
        with open(test_script2, "w") as f:
            f.write("import time\nwhile True:\n    time.sleep(0.1)\n")

        # Start both processes
        proc1 = subprocess.Popen([sys.executable, test_script1])
        proc2 = subprocess.Popen([sys.executable, test_script2])
        time.sleep(0.2)  # Give them time to start

        try:
            # Verify both processes are running
            assert proc1.poll() is None, "First test process should be running"
            assert proc2.poll() is None, "Second test process should be running"

            # Create config with array of terminate_if_process patterns
            config_content = f"""default_interval = "0.05s"
error_log_file = "{self.error_log_file}"

[[files]]
path = ""
terminate_if_process = ["test_proc_a\\\\.py", "test_proc_b\\\\.py"]
"""
            with open(self.config_file, "w") as f:
                f.write(config_content)

            watcher = FileWatcher(self.config_file)

            # Execute check - should terminate both processes (each pattern matches exactly 1)
            watcher._check_files()

            # Wait a bit for termination to complete
            time.sleep(0.5)

            # Verify both processes were terminated
            assert proc1.poll() is not None, "First process should have been terminated"
            assert proc2.poll() is not None, "Second process should have been terminated"

            # Successful terminations should not be logged to error log
            # Error log should not exist for successful operations
            if os.path.exists(self.error_log_file):
                with open(self.error_log_file, "r") as f:
                    log_content = f.read()
                # If the file exists, it should only contain actual errors, not success messages
                assert "Successfully sent terminate signal" not in log_content, (
                    "Success messages should not be in error log"
                )
        finally:
            # Cleanup: ensure processes are killed if still running
            for proc in [proc1, proc2]:
                if proc.poll() is None:
                    proc.kill()
                    proc.wait()

    def test_terminate_multiple_instances_same_pattern_in_array(self):
        """Test that when a pattern in an array matches multiple processes, safety check prevents termination."""
        # Start multiple instances of the same script
        test_script = os.path.join(self.test_dir, "test_multi_same.py")
        with open(test_script, "w") as f:
            f.write("import time\nwhile True:\n    time.sleep(0.1)\n")

        # Start three processes with the same script
        proc1 = subprocess.Popen([sys.executable, test_script])
        proc2 = subprocess.Popen([sys.executable, test_script])
        proc3 = subprocess.Popen([sys.executable, test_script])
        time.sleep(0.2)

        try:
            # Verify all processes are running
            assert proc1.poll() is None, "First process should be running"
            assert proc2.poll() is None, "Second process should be running"
            assert proc3.poll() is None, "Third process should be running"

            # Create config with array containing pattern that matches all three
            config_content = f"""default_interval = "0.05s"
error_log_file = "{self.error_log_file}"

[[files]]
path = ""
terminate_if_process = ["test_multi_same\\\\.py"]
"""
            with open(self.config_file, "w") as f:
                f.write(config_content)

            watcher = FileWatcher(self.config_file)

            # Execute check - should warn but NOT terminate (safety check)
            watcher._check_files()

            # Wait a bit
            time.sleep(0.5)

            # Verify all processes are still running (safety check prevented termination)
            assert proc1.poll() is None, "First process should still be running (not terminated)"
            assert proc2.poll() is None, "Second process should still be running (not terminated)"
            assert proc3.poll() is None, "Third process should still be running (not terminated)"

            # Verify warning was logged
            assert os.path.exists(self.error_log_file), "Error log should exist"
            with open(self.error_log_file, "r") as f:
                log_content = f.read()
            assert "Found 3 processes" in log_content, "Warning about multiple processes should be logged"
        finally:
            # Cleanup
            for proc in [proc1, proc2, proc3]:
                if proc.poll() is None:
                    proc.kill()
                    proc.wait()

    def test_terminate_array_with_no_matches(self):
        """Test that array of patterns with no matches doesn't cause errors."""
        config_content = f"""default_interval = "0.05s"
error_log_file = "{self.error_log_file}"

[[files]]
path = ""
terminate_if_process = ["nonexistent_abc", "nonexistent_xyz"]
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # Execute check - should do nothing (no error)
        watcher._check_files()

        # No assertion needed - just verify it doesn't crash

    def test_terminate_array_with_partial_matches(self):
        """Test that array of patterns terminates only matching processes."""
        # Start only one of two expected processes
        test_script = os.path.join(self.test_dir, "test_partial.py")
        with open(test_script, "w") as f:
            f.write("import time\nwhile True:\n    time.sleep(0.1)\n")

        proc = subprocess.Popen([sys.executable, test_script])
        time.sleep(0.2)

        try:
            # Verify process is running
            assert proc.poll() is None, "Test process should be running"

            # Create config with array where only one pattern matches
            config_content = f"""default_interval = "0.05s"
error_log_file = "{self.error_log_file}"

[[files]]
path = ""
terminate_if_process = ["test_partial\\\\.py", "nonexistent_xyz"]
"""
            with open(self.config_file, "w") as f:
                f.write(config_content)

            watcher = FileWatcher(self.config_file)

            # Execute check - should terminate only the matching process
            watcher._check_files()

            # Wait a bit for termination to complete
            time.sleep(0.5)

            # Verify process was terminated
            assert proc.poll() is not None, "Process should have been terminated"

            # Successful terminations should not be logged to error log
            # Error log should not exist for successful operations
            if os.path.exists(self.error_log_file):
                with open(self.error_log_file, "r") as f:
                    log_content = f.read()
                # If the file exists, it should only contain actual errors, not success messages
                assert "Successfully sent terminate signal" not in log_content, (
                    "Success messages should not be in error log"
                )
        finally:
            # Cleanup
            if proc.poll() is None:
                proc.kill()
                proc.wait()

    def test_terminate_array_mixed_single_and_multiple_matches(self):
        """Test array where one pattern matches 1 process and another matches multiple processes.

        The pattern matching 1 process should terminate it.
        The pattern matching multiple processes should warn and NOT terminate (safety check).
        """
        # Start one process for pattern A
        test_script_a = os.path.join(self.test_dir, "test_single.py")
        with open(test_script_a, "w") as f:
            f.write("import time\nwhile True:\n    time.sleep(0.1)\n")

        # Start two processes for pattern B
        test_script_b = os.path.join(self.test_dir, "test_multi.py")
        with open(test_script_b, "w") as f:
            f.write("import time\nwhile True:\n    time.sleep(0.1)\n")

        proc_a = subprocess.Popen([sys.executable, test_script_a])
        proc_b1 = subprocess.Popen([sys.executable, test_script_b])
        proc_b2 = subprocess.Popen([sys.executable, test_script_b])
        time.sleep(0.2)

        try:
            # Verify all processes are running
            assert proc_a.poll() is None, "Process A should be running"
            assert proc_b1.poll() is None, "Process B1 should be running"
            assert proc_b2.poll() is None, "Process B2 should be running"

            # Create config with array: pattern A matches 1, pattern B matches 2
            config_content = f"""default_interval = "0.05s"
error_log_file = "{self.error_log_file}"

[[files]]
path = ""
terminate_if_process = ["test_single\\\\.py", "test_multi\\\\.py"]
"""
            with open(self.config_file, "w") as f:
                f.write(config_content)

            watcher = FileWatcher(self.config_file)

            # Execute check
            watcher._check_files()

            # Wait a bit
            time.sleep(0.5)

            # Process A should be terminated (matched exactly 1)
            assert proc_a.poll() is not None, "Process A should have been terminated (single match)"

            # Processes B1 and B2 should still be running (safety check for multiple matches)
            assert proc_b1.poll() is None, "Process B1 should still be running (multiple match safety)"
            assert proc_b2.poll() is None, "Process B2 should still be running (multiple match safety)"

            # Verify log contains warning for B (multiple matches)
            # Successful termination of A should NOT be in error log
            assert os.path.exists(self.error_log_file), "Error log should exist"
            with open(self.error_log_file, "r") as f:
                log_content = f.read()
            assert "test_single" not in log_content, "Successful termination should not be in error log"
            assert "Found 2 processes" in log_content, "Should log warning about multiple-match pattern"
            assert "test_multi" in log_content, "Should mention the multi-match pattern"
        finally:
            # Cleanup
            for proc in [proc_a, proc_b1, proc_b2]:
                if proc.poll() is None:
                    proc.kill()
                    proc.wait()


class TestProcessDetectorEnhancements:
    """Test cases for ProcessDetector enhancements."""

    def test_get_all_matching_processes(self):
        """Test getting all matching processes with PIDs."""
        # Get all python processes (should be at least one - this test itself)
        matches = ProcessDetector.get_all_matching_processes(r"python")

        assert isinstance(matches, list), "Should return a list"
        assert len(matches) > 0, "Should find at least one python process"

        # Verify structure
        for pid, name in matches:
            assert isinstance(pid, int), "PID should be an integer"
            assert isinstance(name, str), "Name should be a string"
            assert pid > 0, "PID should be positive"

    def test_get_all_matching_processes_no_match(self):
        """Test getting all matching processes when none exist."""
        matches = ProcessDetector.get_all_matching_processes(r"nonexistent_xyz123")

        assert isinstance(matches, list), "Should return a list"
        assert len(matches) == 0, "Should return empty list for no matches"

    def test_get_all_matching_processes_invalid_regex(self):
        """Test that invalid regex is handled gracefully."""
        matches = ProcessDetector.get_all_matching_processes(r"[invalid(regex")

        assert isinstance(matches, list), "Should return a list"
        assert len(matches) == 0, "Should return empty list for invalid regex"

    def test_terminate_process_invalid_pid(self):
        """Test that terminating invalid PID is handled gracefully."""
        # Use a very high PID that doesn't exist
        result = ProcessDetector.terminate_process(999999)

        assert result is False, "Should return False for non-existent process"

{% endraw %}
```

## 最近の変更（過去7日間）
### コミット履歴:
11a6eab CI

### 変更されたファイル:
.github/copilot-instructions.md
.github/workflows/call-check-large-files.yml
README.md
issue-notes/141.md
issue-notes/145.md
src/color_scheme.py
src/command_executor.py


---
Generated at: 2026-03-29 07:03:31 JST

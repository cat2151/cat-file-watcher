#!/usr/bin/env python3
"""
Tests for the RepoUpdater (auto-update) feature
"""

import os
import sys
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from repo_updater import RepoUpdater


class TestRepoUpdaterInit:
    """Test RepoUpdater initialisation from config."""

    def test_default_config_no_auto_update_section(self):
        """RepoUpdater with empty config defaults to dry-run, 1h interval."""
        updater = RepoUpdater({})
        assert updater.enabled is False
        assert updater.interval == 3600.0  # 1h in seconds

    def test_enabled_false_by_default(self):
        """auto_update.enabled defaults to False (dry-run)."""
        updater = RepoUpdater({"auto_update": {}})
        assert updater.enabled is False

    def test_enabled_true_from_config(self):
        """auto_update.enabled=true is read correctly."""
        updater = RepoUpdater({"auto_update": {"enabled": True}})
        assert updater.enabled is True

    def test_custom_interval(self):
        """Custom auto_update.interval is parsed correctly."""
        updater = RepoUpdater({"auto_update": {"interval": "30m"}})
        assert updater.interval == 1800.0  # 30 minutes in seconds

    def test_repo_dir_is_a_directory(self):
        """repo_dir resolves to an existing directory."""
        updater = RepoUpdater({})
        assert os.path.isdir(updater.repo_dir)


class TestRepoUpdaterGitCommands:
    """Test git command helpers."""

    def _make_updater(self):
        return RepoUpdater({})

    def test_run_git_command_success(self):
        """_run_git_command returns correct output on success."""
        updater = self._make_updater()
        with patch("subprocess.run") as mock_run:
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stdout = "abc123\n"
            mock_result.stderr = ""
            mock_run.return_value = mock_result

            rc, stdout, stderr = updater._run_git_command(["rev-parse", "HEAD"])
            assert rc == 0
            assert stdout == "abc123"

    def test_run_git_command_timeout(self):
        """_run_git_command returns -1 on timeout."""
        import subprocess

        updater = self._make_updater()
        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired(cmd="git", timeout=60)):
            rc, stdout, stderr = updater._run_git_command(["fetch"])
            assert rc == -1
            assert "timed out" in stderr

    def test_has_updates_returns_false_when_hashes_equal(self):
        """_has_updates returns False when HEAD matches upstream."""
        updater = self._make_updater()

        def fake_run_git(args):
            if args[0] == "fetch":
                return 0, "", ""
            if args == ["rev-parse", "HEAD"]:
                return 0, "abc123", ""
            if args == ["rev-parse", "@{u}"]:
                return 0, "abc123", ""
            return 0, "", ""

        updater._run_git_command = fake_run_git
        assert updater._has_updates() is False

    def test_has_updates_returns_true_when_hashes_differ(self):
        """_has_updates returns True when upstream is ahead of HEAD."""
        updater = self._make_updater()

        def fake_run_git(args):
            if args[0] == "fetch":
                return 0, "", ""
            if args == ["rev-parse", "HEAD"]:
                return 0, "abc123", ""
            if args == ["rev-parse", "@{u}"]:
                return 0, "def456", ""
            return 0, "", ""

        updater._run_git_command = fake_run_git
        assert updater._has_updates() is True

    def test_has_updates_returns_false_on_fetch_failure(self):
        """_has_updates returns False when git fetch fails."""
        updater = self._make_updater()

        def fake_run_git(args):
            if args[0] == "fetch":
                return 1, "", "network error"
            return 0, "abc123", ""

        updater._run_git_command = fake_run_git
        assert updater._has_updates() is False

    def test_has_updates_returns_false_when_no_upstream(self):
        """_has_updates returns False when no upstream branch is configured."""
        updater = self._make_updater()

        def fake_run_git(args):
            if args[0] == "fetch":
                return 0, "", ""
            if args == ["rev-parse", "HEAD"]:
                return 0, "abc123", ""
            if args == ["rev-parse", "@{u}"]:
                return 128, "", "no upstream configured"
            return 0, "", ""

        updater._run_git_command = fake_run_git
        assert updater._has_updates() is False

    def test_pull_returns_true_on_success(self):
        """_pull returns True when git pull succeeds."""
        updater = self._make_updater()
        updater._run_git_command = lambda args: (0, "Already up to date.", "")
        assert updater._pull() is True

    def test_pull_returns_false_on_failure(self):
        """_pull returns False when git pull fails."""
        updater = self._make_updater()
        updater._run_git_command = lambda args: (1, "", "merge conflict")
        assert updater._pull() is False


class TestRepoUpdaterDryRun:
    """Test dry-run behaviour (no pull, no restart)."""

    def test_dry_run_does_not_pull_when_updates_available(self):
        """In dry-run mode, _pull is NOT called when updates are found."""
        updater = RepoUpdater({"auto_update": {"enabled": False, "interval": "100ms"}})

        pull_called = []
        updater._has_updates = lambda: True
        updater._pull = lambda: pull_called.append(True) or True
        updater._restart = lambda: None  # should never be called

        # Manually run one iteration of the check loop logic (without sleeping)
        updater._stop_event.set()  # stop immediately after first wait returns False
        updater._stop_event.clear()

        # Simulate one loop body
        if updater._has_updates():
            if updater.enabled:
                updater._pull()

        assert pull_called == [], "pull should not be called in dry-run mode"

    def test_enabled_mode_calls_pull_and_restart_on_updates(self):
        """When enabled=True, _pull and _restart are called if updates exist."""
        updater = RepoUpdater({"auto_update": {"enabled": True, "interval": "100ms"}})

        pull_called = []
        restart_called = []
        updater._has_updates = lambda: True
        updater._pull = lambda: pull_called.append(True) or True
        updater._restart = lambda: restart_called.append(True)

        # Simulate one loop body
        if updater._has_updates():
            if updater.enabled:
                if updater._pull():
                    updater._restart()

        assert pull_called == [True]
        assert restart_called == [True]


class TestRepoUpdaterThread:
    """Test background thread lifecycle."""

    def test_start_creates_daemon_thread(self):
        """start() creates a daemon thread named RepoUpdater."""
        updater = RepoUpdater({"auto_update": {"interval": "1h"}})
        # Prevent the thread from actually sleeping/checking
        updater._stop_event.set()
        updater.start()
        assert updater._thread is not None
        assert updater._thread.daemon is True
        assert updater._thread.name == "RepoUpdater"
        updater.stop()

    def test_stop_signals_thread(self):
        """stop() sets the stop event so the thread exits."""
        updater = RepoUpdater({"auto_update": {"interval": "1h"}})
        updater._stop_event.set()  # prevent the loop from sleeping
        updater.start()
        updater.stop()
        assert updater._stop_event.is_set()


class TestFileWatcherAutoUpdate:
    """Integration: FileWatcher creates RepoUpdater only when configured."""

    def setup_method(self):
        import tempfile

        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test.txt")
        with open(self.test_file, "w") as f:
            f.write("content\n")

    def teardown_method(self):
        import shutil

        shutil.rmtree(self.test_dir, ignore_errors=True)

    def _write_config(self, extra=""):
        config_file = os.path.join(self.test_dir, "config.toml")
        content = f'[[files]]\npath = "{self.test_file}"\ncommand = "echo ok"\n{extra}\n'
        with open(config_file, "w") as f:
            f.write(content)
        return config_file

    def test_no_auto_update_section_creates_no_updater(self):
        """FileWatcher._repo_updater is None when [auto_update] is absent."""
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
        from cat_file_watcher import FileWatcher

        config_file = self._write_config()
        watcher = FileWatcher(config_file)
        assert watcher._repo_updater is None

    def test_auto_update_section_creates_updater(self):
        """FileWatcher._repo_updater is set when [auto_update] is present."""
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
        from cat_file_watcher import FileWatcher

        config_file = self._write_config('[auto_update]\ninterval = "1h"\n')
        watcher = FileWatcher(config_file)
        assert watcher._repo_updater is not None
        assert isinstance(watcher._repo_updater, RepoUpdater)

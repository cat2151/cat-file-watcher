#!/usr/bin/env python3
"""
Repository auto-updater for File Watcher

Checks for git repository updates in a background thread and optionally
pulls changes and restarts the process.
"""

import os
import subprocess
import sys
import threading

from colorama import Fore

# Support both relative and absolute imports
try:
    from .interval_parser import IntervalParser
    from .timestamp_printer import TimestampPrinter
except ImportError:
    from interval_parser import IntervalParser
    from timestamp_printer import TimestampPrinter


class RepoUpdater:
    """Checks for git repository updates in a background thread.

    By default runs in dry-run mode: detects updates and reports them
    without pulling or restarting.  Set ``auto_update.enabled = true``
    in the TOML config to enable automatic pull and restart.
    """

    DEFAULT_INTERVAL = "1h"

    def __init__(self, config):
        """Initialize the repo updater from configuration.

        Args:
            config: Global configuration dictionary.  Reads the
                    ``[auto_update]`` sub-table for settings.
        """
        auto_update_config = config.get("auto_update", {})
        self.enabled = auto_update_config.get("enabled", False)
        interval_str = auto_update_config.get("interval", self.DEFAULT_INTERVAL)
        self.interval = IntervalParser.parse_interval(interval_str)

        # The repository directory is two levels up from this file
        # (src/repo_updater.py -> src/ -> repo root)
        self.repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self._stop_event = threading.Event()
        self._thread = None

    def _run_git_command(self, args):
        """Run a git command inside the repository directory.

        Args:
            args: List of arguments to pass after ``git``

        Returns:
            tuple: (returncode, stdout, stderr)
        """
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=self.repo_dir,
                capture_output=True,
                text=True,
                timeout=60,
            )
            return result.returncode, result.stdout.strip(), result.stderr.strip()
        except subprocess.TimeoutExpired:
            return -1, "", "git command timed out"
        except Exception as e:
            return -1, "", str(e)

    def _has_updates(self):
        """Fetch from origin and check whether the local branch is behind.

        Returns:
            bool: True if upstream has commits not yet in HEAD
        """
        returncode, _, stderr = self._run_git_command(["fetch"])
        if returncode != 0:
            TimestampPrinter.print(f"Warning: git fetch failed: {stderr}", Fore.YELLOW)
            return False

        returncode, local_hash, _ = self._run_git_command(["rev-parse", "HEAD"])
        if returncode != 0:
            return False

        returncode, upstream_hash, _ = self._run_git_command(["rev-parse", "@{u}"])
        if returncode != 0:
            # No upstream tracking branch configured — nothing to compare
            return False

        return local_hash != upstream_hash

    def _pull(self):
        """Pull the latest changes from the upstream branch.

        Returns:
            bool: True if pull succeeded
        """
        returncode, stdout, stderr = self._run_git_command(["pull"])
        if returncode != 0:
            TimestampPrinter.print(f"Warning: git pull failed: {stderr}", Fore.YELLOW)
            return False
        TimestampPrinter.print(f"Repository updated: {stdout}", Fore.GREEN)
        return True

    def _restart(self):
        """Replace the current process with a fresh instance (self-restart)."""
        TimestampPrinter.print("Restarting...", Fore.GREEN)
        os.execv(sys.executable, [sys.executable] + sys.argv)

    def _check_loop(self):
        """Background thread: sleep for *interval*, then check for updates."""
        while not self._stop_event.wait(self.interval):
            try:
                TimestampPrinter.print("Checking for repository updates...", Fore.GREEN)
                if self._has_updates():
                    if self.enabled:
                        TimestampPrinter.print("Repository updates found. Pulling and restarting...", Fore.GREEN)
                        if self._pull():
                            self._restart()
                    else:
                        TimestampPrinter.print(
                            "Repository updates available. "
                            "(dry-run: set auto_update.enabled = true to pull and restart automatically)",
                            Fore.YELLOW,
                        )
                else:
                    TimestampPrinter.print("No repository updates found.", Fore.GREEN)
            except Exception as e:
                TimestampPrinter.print(f"Warning: Error during repository update check: {e}", Fore.YELLOW)

    def start(self):
        """Start the background update-check thread (daemon thread)."""
        self._thread = threading.Thread(target=self._check_loop, daemon=True, name="RepoUpdater")
        self._thread.start()
        mode = "enabled" if self.enabled else "dry-run"
        TimestampPrinter.print(f"Auto-update check started (interval: {self.interval}s, mode: {mode})", Fore.GREEN)

    def stop(self):
        """Signal the background thread to stop and wait for it to finish."""
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join(timeout=5)

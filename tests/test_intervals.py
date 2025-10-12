#!/usr/bin/env python3
"""
Interval-related tests for cat_file_watcher
"""

import os
import shutil
import sys
import tempfile
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from cat_file_watcher import FileWatcher


class TestFileWatcherIntervals:
    """Test cases for interval-related functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, "test_config.toml")
        self.test_file = os.path.join(self.test_dir, "test.txt")
        with open(self.test_file, "w") as f:
            f.write("Initial content\n")

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_default_interval(self):
        """Test that default interval is used when not specified."""
        config_content = f'''[files]
[[files]]
path = "{self.test_file}"
command = "echo 'File changed'"

'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)
        interval = watcher._get_interval_for_file({})
        assert interval == 1.0

    def test_custom_default_interval(self):
        """Test that custom default interval is respected."""
        config_content = f'''default_interval = "0.5s"

[[files]]
path = "{self.test_file}"
command = "echo 'File changed'"

'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)
        interval = watcher._get_interval_for_file({})
        assert interval == 0.5

    def test_per_file_interval(self):
        """Test that per-file interval overrides default."""
        config_content = f'''default_interval = "1s"

[[files]]
path = "{self.test_file}"
command = "echo 'File changed'"
interval = "0.25s"

'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)
        settings = watcher.config["files"][self.test_file]
        interval = watcher._get_interval_for_file(settings)
        assert interval == 0.25

    def test_interval_throttling(self):
        """Test that files are not checked more frequently than their interval."""
        config_content = f'''default_interval = "0.5s"

[[files]]
path = "{self.test_file}"
command = "echo 'File changed'"

'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)
        watcher._check_files()
        first_check_time = watcher.file_last_check[self.test_file]

        time.sleep(0.05)
        watcher._check_files()
        assert watcher.file_last_check[self.test_file] == first_check_time

        time.sleep(0.5)
        watcher._check_files()
        assert watcher.file_last_check[self.test_file] > first_check_time

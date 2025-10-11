#!/usr/bin/env python3
"""
Test cases for main loop interval calculation
"""

import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from cat_file_watcher import FileWatcher


class TestMainLoopInterval:
    """Test cases for main loop interval calculation."""

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

    def test_main_loop_interval_uses_default_interval(self):
        """Test that main loop interval uses default_interval when it's the smallest."""
        config_content = f'''default_interval = "1s"
config_check_interval = "2s"

[files]
"{self.test_file}" = {{ command = "echo 'File changed'" }}
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)
        interval = watcher._calculate_main_loop_interval()
        assert interval == 1.0

    def test_main_loop_interval_uses_config_check_interval(self):
        """Test that main loop interval uses config_check_interval when it's the smallest."""
        config_content = f'''default_interval = "2s"
config_check_interval = "0.5s"

[files]
"{self.test_file}" = {{ command = "echo 'File changed'" }}
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)
        interval = watcher._calculate_main_loop_interval()
        assert interval == 0.5

    def test_main_loop_interval_uses_per_file_interval(self):
        """Test that main loop interval uses per-file interval when it's the smallest."""
        config_content = f'''default_interval = "2s"
config_check_interval = "2s"

[files]
"{self.test_file}" = {{ command = "echo 'File changed'", interval = "0.25s" }}
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)
        interval = watcher._calculate_main_loop_interval()
        assert interval == 0.25

    def test_main_loop_interval_with_multiple_files(self):
        """Test that main loop interval uses minimum across multiple files."""
        test_file2 = os.path.join(self.test_dir, "test2.txt")
        with open(test_file2, "w") as f:
            f.write("Content\n")

        config_content = f'''default_interval = "2s"
config_check_interval = "2s"

[files]
"{self.test_file}" = {{ command = "echo 'File changed'", interval = "0.5s" }}
"{test_file2}" = {{ command = "echo 'File2 changed'", interval = "0.1s" }}
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)
        interval = watcher._calculate_main_loop_interval()
        assert interval == 0.1

    def test_main_loop_interval_defaults(self):
        """Test that main loop interval works with default values."""
        config_content = f'''[files]
"{self.test_file}" = {{ command = "echo 'File changed'" }}
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)
        interval = watcher._calculate_main_loop_interval()
        # Both default_interval and config_check_interval default to "1s"
        assert interval == 1.0

    def test_main_loop_interval_with_only_config_check_interval(self):
        """Test main loop interval when only config_check_interval is specified."""
        config_content = f'''config_check_interval = "3s"

[files]
"{self.test_file}" = {{ command = "echo 'File changed'" }}
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)
        interval = watcher._calculate_main_loop_interval()
        # default_interval defaults to "1s", config_check_interval is "3s"
        assert interval == 1.0

    def test_main_loop_interval_very_small(self):
        """Test main loop interval with very small value."""
        config_content = f'''default_interval = "5s"
config_check_interval = "5s"

[files]
"{self.test_file}" = {{ command = "echo 'File changed'", interval = "0.05s" }}
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)
        interval = watcher._calculate_main_loop_interval()
        assert interval == 0.05

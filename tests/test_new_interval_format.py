#!/usr/bin/env python3
"""
Tests for new interval format (time strings like "1s", "2m", "3h")
"""

import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from cat_file_watcher import FileWatcher


class TestNewIntervalFormat:
    """Test cases for new interval format with time strings."""

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

    def test_default_interval_seconds(self):
        """Test default interval with seconds format."""
        config_content = f'''default_interval = "2s"

[[files]]
path = "{self.test_file}"
command = "echo 'File changed'"

'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)
        interval = watcher._get_interval_for_file({})
        assert interval == 2.0

    def test_default_interval_minutes(self):
        """Test default interval with minutes format."""
        config_content = f'''default_interval = "2m"

[[files]]
path = "{self.test_file}"
command = "echo 'File changed'"

'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)
        interval = watcher._get_interval_for_file({})
        assert interval == 120.0

    def test_default_interval_hours(self):
        """Test default interval with hours format."""
        config_content = f'''default_interval = "1h"

[[files]]
path = "{self.test_file}"
command = "echo 'File changed'"

'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)
        interval = watcher._get_interval_for_file({})
        assert interval == 3600.0

    def test_default_interval_decimal_seconds(self):
        """Test default interval with decimal seconds format."""
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

    def test_per_file_interval_seconds(self):
        """Test per-file interval with seconds format."""
        config_content = f'''default_interval = "1s"

[[files]]
path = "{self.test_file}"
command = "echo 'File changed'"
interval = "3s"

'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)
        settings = watcher.config["files"][self.test_file]
        interval = watcher._get_interval_for_file(settings)
        assert interval == 3.0

    def test_per_file_interval_minutes(self):
        """Test per-file interval with minutes format."""
        config_content = f'''default_interval = "1s"

[[files]]
path = "{self.test_file}"
command = "echo 'File changed'"
interval = "5m"

'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)
        settings = watcher.config["files"][self.test_file]
        interval = watcher._get_interval_for_file(settings)
        assert interval == 300.0

    def test_per_file_interval_decimal(self):
        """Test per-file interval with decimal format."""
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

    def test_config_check_interval_new_format(self):
        """Test config_check_interval with new format."""
        config_content = f'''default_interval = "1s"
config_check_interval = "5s"

[[files]]
path = "{self.test_file}"
command = "echo 'File changed'"

'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)
        # Calculate the main loop interval - should be the minimum of all intervals
        main_interval = watcher._calculate_main_loop_interval()
        assert main_interval == 1.0  # default_interval is the minimum

    def test_main_loop_interval_with_new_format(self):
        """Test that main loop interval calculation works with new format."""
        config_content = f'''default_interval = "2s"
config_check_interval = "5s"

[[files]]
path = "{self.test_file}"
command = "echo 'File changed'"
interval = "1s"

'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)
        main_interval = watcher._calculate_main_loop_interval()
        # Should be the minimum: 1s
        assert main_interval == 1.0

    def test_various_decimal_formats(self):
        """Test various decimal formats for intervals."""
        test_cases = [
            ("0.1s", 0.1),
            (".5s", 0.5),
            ("1.5s", 1.5),
            ("2.5m", 150.0),
            ("0.25h", 900.0),
        ]

        for interval_str, expected_seconds in test_cases:
            config_content = f'''default_interval = "{interval_str}"

[[files]]
path = "{self.test_file}"
command = "echo 'File changed'"

'''
            with open(self.config_file, "w") as f:
                f.write(config_content)

            watcher = FileWatcher(self.config_file)
            interval = watcher._get_interval_for_file({})
            assert interval == expected_seconds, f"Failed for {interval_str}: expected {expected_seconds}, got {interval}"

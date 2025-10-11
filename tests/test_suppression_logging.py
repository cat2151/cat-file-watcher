#!/usr/bin/env python3
"""
Tests for command suppression logging functionality
"""

import os
import shutil
import sys
import tempfile
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from cat_file_watcher import FileWatcher


class TestSuppressionLogging:
    """Test cases for suppression logging."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, "test_config.toml")
        self.test_file = os.path.join(self.test_dir, "test.txt")
        self.suppression_log_file = os.path.join(self.test_dir, "suppression.log")

        with open(self.test_file, "w") as f:
            f.write("Initial content\n")

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_suppression_logging_enabled(self):
        """Test that suppression logging works when enabled."""
        # Create config with suppression_log_file
        config_content = f'''default_interval = 50
suppression_log_file = "{self.suppression_log_file}"

[files]
"{self.test_file}" = {{ command = "echo 'test'", suppress_if_process = "python" }}
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # Initialize timestamp tracking
        watcher._check_files()

        # Modify the test file to trigger command execution (which should be suppressed)
        time.sleep(0.1)
        with open(self.test_file, "a") as f:
            f.write("Modified content\n")

        # Check for file changes
        watcher._check_files()

        # Suppression log file should be created
        assert os.path.exists(self.suppression_log_file)

        # Check log content
        with open(self.suppression_log_file, "r") as f:
            log_content = f.read()

        # Log should contain timestamp, process pattern, and matched process
        assert "File:" in log_content
        assert "Process pattern: python" in log_content
        assert "Matched process:" in log_content
        # Should contain "python" somewhere in the matched process line
        assert "python" in log_content.lower()

    def test_suppression_logging_disabled(self):
        """Test that suppression logging is not created when not configured."""
        # Create config without suppression_log_file
        config_content = f'''default_interval = 50

[files]
"{self.test_file}" = {{ command = "echo 'test'", suppress_if_process = "python" }}
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # Initialize timestamp tracking
        watcher._check_files()

        # Modify the test file to trigger command execution (which should be suppressed)
        time.sleep(0.1)
        with open(self.test_file, "a") as f:
            f.write("Modified content\n")

        # Check for file changes
        watcher._check_files()

        # Suppression log file should not be created
        assert not os.path.exists(self.suppression_log_file)

    def test_suppression_logging_no_suppression(self):
        """Test that no log is written when command is not suppressed."""
        # Create config with suppression_log_file but process that won't match
        config_content = f'''default_interval = 50
suppression_log_file = "{self.suppression_log_file}"

[files]
"{self.test_file}" = {{ command = "echo 'test'", suppress_if_process = "nonexistent_process_xyz123" }}
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # Initialize timestamp tracking
        watcher._check_files()

        # Modify the test file to trigger command execution (should not be suppressed)
        time.sleep(0.1)
        with open(self.test_file, "a") as f:
            f.write("Modified content\n")

        # Check for file changes
        watcher._check_files()

        # Suppression log file should not be created
        assert not os.path.exists(self.suppression_log_file)

    def test_suppression_logging_multiple_suppressions(self):
        """Test that multiple suppressions are logged correctly."""
        # Create config with suppression_log_file
        config_content = f'''default_interval = 50
suppression_log_file = "{self.suppression_log_file}"

[files]
"{self.test_file}" = {{ command = "echo 'test'", suppress_if_process = "python" }}
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # Initialize timestamp tracking
        watcher._check_files()

        # Modify the test file multiple times
        for i in range(3):
            time.sleep(0.1)
            with open(self.test_file, "a") as f:
                f.write(f"Modified content {i}\n")
            watcher._check_files()

        # Suppression log file should be created
        assert os.path.exists(self.suppression_log_file)

        # Check log content - should have 3 entries
        with open(self.suppression_log_file, "r") as f:
            log_content = f.read()

        # Count the number of log entries (each has a File: line)
        entry_count = log_content.count("File:")
        assert entry_count == 3

    def test_suppression_logging_timestamp_format(self):
        """Test that log entries include properly formatted timestamps."""
        # Create config with suppression_log_file
        config_content = f'''default_interval = 50
suppression_log_file = "{self.suppression_log_file}"

[files]
"{self.test_file}" = {{ command = "echo 'test'", suppress_if_process = "python" }}
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # Initialize timestamp tracking
        watcher._check_files()

        # Modify the test file
        time.sleep(0.1)
        with open(self.test_file, "a") as f:
            f.write("Modified content\n")

        # Check for file changes
        watcher._check_files()

        # Check log content
        with open(self.suppression_log_file, "r") as f:
            log_content = f.read()

        # Should have timestamp in format [YYYY-MM-DD HH:MM:SS]
        import re

        timestamp_pattern = r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]"
        assert re.search(timestamp_pattern, log_content)

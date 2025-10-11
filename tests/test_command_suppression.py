#!/usr/bin/env python3
"""
Command suppression tests for cat_file_watcher
"""

import os
import shutil
import sys
import tempfile
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from cat_file_watcher import FileWatcher


class TestCommandSuppression:
    """Test cases for command suppression based on running processes."""

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

    def test_command_suppression_when_process_exists(self):
        """Test that command execution is suppressed when specified process exists."""
        test_output = os.path.join(self.test_dir, "output.txt")
        config_content = f'''default_interval = "0.05s"

[files]
"{self.test_file}" = {{ command = "echo 'executed' > {test_output}", suppress_if_process = "python" }}
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)
        watcher._check_files()

        time.sleep(0.1)
        with open(self.test_file, "a") as f:
            f.write("Modified content\n")

        watcher._check_files()
        assert not os.path.exists(test_output)

    def test_command_execution_when_process_not_exists(self):
        """Test that command executes normally when specified process doesn't exist."""
        test_output = os.path.join(self.test_dir, "output.txt")
        config_content = f'''default_interval = "0.05s"

[files]
"{self.test_file}" = {{ command = "echo 'executed' > {test_output}", suppress_if_process = "nonexistent_process_xyz123" }}
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)
        watcher._check_files()

        time.sleep(0.1)
        with open(self.test_file, "a") as f:
            f.write("Modified content\n")

        watcher._check_files()
        assert os.path.exists(test_output)

    def test_command_execution_without_suppress_if_process(self):
        """Test that commands execute normally when suppress_if_process is not specified."""
        test_output = os.path.join(self.test_dir, "output.txt")
        config_content = f'''default_interval = "0.05s"

[files]
"{self.test_file}" = {{ command = "echo 'executed' > {test_output}" }}
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)
        watcher._check_files()

        time.sleep(0.1)
        with open(self.test_file, "a") as f:
            f.write("Modified content\n")

        watcher._check_files()
        assert os.path.exists(test_output)

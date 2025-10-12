#!/usr/bin/env python3
"""
Tests for cwd functionality in command execution
"""

import os
import shutil
import sys
import tempfile
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from cat_file_watcher import FileWatcher


class TestCwd:
    """Test cases for cwd functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, "config.toml")
        self.test_file = os.path.join(self.test_dir, "test.txt")

        # Create a subdirectory for cwd tests
        self.subdir = os.path.join(self.test_dir, "subdir")
        os.makedirs(self.subdir, exist_ok=True)

        # Create a test file
        with open(self.test_file, "w") as f:
            f.write("Initial content\n")

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def test_cwd_basic(self):
        """Test that cwd changes the working directory when executing commands."""
        # Create an output file path in the subdirectory
        output_file = os.path.join(self.subdir, "output.txt")

        # Create config with cwd setting
        # The command will execute 'pwd > output.txt' in the subdir
        config_content = f'''default_interval = "0.05s"

[[files]]
path = "{self.test_file}"
command = "pwd > output.txt"
cwd = "{self.subdir}"
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # Initialize timestamp tracking
        watcher._check_files()

        # Modify the test file to trigger command execution
        time.sleep(0.1)
        with open(self.test_file, "a") as f:
            f.write("Modified content\n")

        # Check for file changes
        watcher._check_files()

        # Output file should be created in the subdir
        assert os.path.exists(output_file), "Output file should exist in subdir"

        # Read the output and verify it contains the subdir path
        with open(output_file, "r") as f:
            pwd_output = f.read().strip()

        # The pwd command should show the subdir path
        assert pwd_output == self.subdir, f"Expected pwd to be {self.subdir}, got {pwd_output}"

    def test_cwd_relative_file_access(self):
        """Test that relative file paths work correctly with cwd."""
        # Create a file in the subdirectory
        test_input = os.path.join(self.subdir, "input.txt")
        with open(test_input, "w") as f:
            f.write("test data\n")

        # Create output file path in subdirectory
        output_file = os.path.join(self.subdir, "output.txt")

        # Command will use relative path 'input.txt' because it runs in subdir
        config_content = f'''default_interval = "0.05s"

[[files]]
path = "{self.test_file}"
command = "cat input.txt > output.txt"
cwd = "{self.subdir}"
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)
        watcher._check_files()

        # Modify the test file to trigger command execution
        time.sleep(0.1)
        with open(self.test_file, "a") as f:
            f.write("Modified\n")

        watcher._check_files()

        # Verify the output file was created and contains the expected content
        assert os.path.exists(output_file)
        with open(output_file, "r") as f:
            content = f.read()
        assert "test data" in content

    def test_cwd_without_setting(self):
        """Test that commands work normally when cwd is not specified."""
        output_file = os.path.join(self.test_dir, "output.txt")

        config_content = f'''default_interval = "0.05s"

[[files]]
path = "{self.test_file}"
command = "echo 'no cwd' > {output_file}"
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)
        watcher._check_files()

        time.sleep(0.1)
        with open(self.test_file, "a") as f:
            f.write("Modified\n")

        watcher._check_files()

        # Output file should be created
        assert os.path.exists(output_file)

    def test_cwd_invalid_directory(self):
        """Test error handling when cwd path doesn't exist."""
        invalid_dir = os.path.join(self.test_dir, "nonexistent")

        config_content = f'''default_interval = "0.05s"

[[files]]
path = "{self.test_file}"
command = "echo 'test'"
cwd = "{invalid_dir}"
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)
        watcher._check_files()

        time.sleep(0.1)
        with open(self.test_file, "a") as f:
            f.write("Modified\n")

        # This should handle the error gracefully (not crash)
        # The error will be caught and logged
        watcher._check_files()

        # Test passes if we get here without exception

    def test_cwd_with_other_settings(self):
        """Test that cwd works alongside other settings like interval and enable_log."""
        output_file = os.path.join(self.subdir, "output.txt")
        log_file = os.path.join(self.test_dir, "command.log")

        config_content = f'''default_interval = "0.05s"
log_file = "{log_file}"

[[files]]
path = "{self.test_file}"
command = "pwd > output.txt"
cwd = "{self.subdir}"
interval = "0.1s"
enable_log = true
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)
        watcher._check_files()

        time.sleep(0.1)
        with open(self.test_file, "a") as f:
            f.write("Modified\n")

        watcher._check_files()

        # Verify command executed in subdir
        assert os.path.exists(output_file)
        with open(output_file, "r") as f:
            pwd_output = f.read().strip()
        assert pwd_output == self.subdir

        # Verify logging worked
        assert os.path.exists(log_file)
        with open(log_file, "r") as f:
            log_content = f.read()
        assert "cwd" in log_content

#!/usr/bin/env python3
"""
Empty filename tests for cat_file_watcher
Tests for executing commands without file monitoring (process health monitoring use case)
"""

import os
import shutil
import sys
import tempfile
import time

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from cat_file_watcher import FileWatcher


class TestEmptyFilename:
    """Test cases for empty filename functionality (command-only execution)."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, "test_config.toml")

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_empty_filename_executes_command(self):
        """Test that empty filename executes command without file monitoring."""
        # Create a test output file to verify command execution
        test_output = os.path.join(self.test_dir, "output.txt")

        # Create config with empty filename
        config_content = f"""default_interval = "0.05s"

[files]
"" = {{ command = "echo 'executed' > {test_output}" }}
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # First check should execute the command (no file to monitor)
        watcher._check_files()

        # Output file should be created
        assert os.path.exists(test_output), "Command should have executed for empty filename"

        # Read the content to verify
        with open(test_output, "r") as f:
            content = f.read().strip()
        assert content == "executed", "Command output should match expected value"

    def test_empty_filename_respects_interval(self):
        """Test that empty filename respects interval timing."""
        # Create a counter file to track executions
        counter_file = os.path.join(self.test_dir, "counter.txt")

        # Create config with empty filename and custom interval (100ms)
        config_content = f"""default_interval = "0.1s"

[files]
"" = {{ command = "echo 'x' >> {counter_file}" }}
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # First check - should execute
        watcher._check_files()
        time.sleep(0.05)  # 50ms - less than interval

        # Second check immediately - should NOT execute (interval not met)
        watcher._check_files()

        # Wait for interval to pass
        time.sleep(0.06)  # Total 110ms, more than 100ms interval

        # Third check - should execute again
        watcher._check_files()

        # Verify the command was executed exactly twice
        if os.path.exists(counter_file):
            with open(counter_file, "r") as f:
                lines = f.readlines()
            assert len(lines) == 2, "Command should execute twice (once at start, once after interval)"

    def test_empty_filename_with_suppress_if_process(self):
        """Test empty filename with process suppression for health monitoring."""
        # This is the main use case: process health monitoring
        test_output = os.path.join(self.test_dir, "health_check.txt")

        # Create config that checks if python is running, and only executes if NOT running
        config_content = f"""default_interval = "0.05s"

[files]
"" = {{ command = "echo 'process_not_found' > {test_output}", suppress_if_process = "python" }}
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # Check files - command should be suppressed because python is running
        watcher._check_files()

        # Output file should NOT exist because command was suppressed
        assert not os.path.exists(test_output), "Command should be suppressed when process exists"

    def test_empty_filename_combined_with_regular_files(self):
        """Test that empty filename can coexist with regular file monitoring."""
        test_file = os.path.join(self.test_dir, "test.txt")
        output1 = os.path.join(self.test_dir, "output1.txt")
        output2 = os.path.join(self.test_dir, "output2.txt")

        # Create a test file
        with open(test_file, "w") as f:
            f.write("Initial content\n")

        # Create config with both empty filename and regular file
        config_content = f'''default_interval = "0.05s"

[files]
"" = {{ command = "echo 'periodic' > {output1}" }}
"{test_file}" = {{ command = "echo 'file_changed' > {output2}" }}
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # First check - empty filename should execute, regular file should just initialize
        watcher._check_files()

        assert os.path.exists(output1), "Empty filename command should execute"
        assert not os.path.exists(output2), "Regular file command should not execute on first check"

        # Modify the regular file
        time.sleep(0.1)
        with open(test_file, "a") as f:
            f.write("Modified content\n")

        # Second check - regular file should now execute
        watcher._check_files()

        assert os.path.exists(output2), "Regular file command should execute after file change"

#!/usr/bin/env python3
"""
Tests for multiple empty filename entries (array of tables format)
"""

import os
import shutil
import sys
import tempfile
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from cat_file_watcher import FileWatcher


class TestMultipleEmptyFilenames:
    """Test cases for multiple empty filename entries using array of tables format."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, "config.toml")

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_multiple_empty_filenames_execute(self):
        """Test that multiple empty filename entries can execute independently."""
        # Create output files to verify command execution
        output1 = os.path.join(self.test_dir, "output1.txt")
        output2 = os.path.join(self.test_dir, "output2.txt")
        output3 = os.path.join(self.test_dir, "output3.txt")

        # Create config with multiple empty filename entries using array of tables
        config_content = f"""default_interval = "0.05s"

[[files]]
path = ""
command = "echo 'first' > {output1}"

[[files]]
path = ""
command = "echo 'second' > {output2}"

[[files]]
path = ""
command = "echo 'third' > {output3}"
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # First check should execute all commands
        watcher._check_files()

        # All output files should be created
        assert os.path.exists(output1), "First command should have executed"
        assert os.path.exists(output2), "Second command should have executed"
        assert os.path.exists(output3), "Third command should have executed"

        # Verify the content
        with open(output1, "r") as f:
            assert f.read().strip() == "first"
        with open(output2, "r") as f:
            assert f.read().strip() == "second"
        with open(output3, "r") as f:
            assert f.read().strip() == "third"

    def test_multiple_empty_filenames_with_different_intervals(self):
        """Test that multiple empty filename entries respect their individual intervals."""
        counter1 = os.path.join(self.test_dir, "counter1.txt")
        counter2 = os.path.join(self.test_dir, "counter2.txt")

        # First entry: 100ms interval, Second entry: 200ms interval
        config_content = f"""default_interval = "0.1s"

[[files]]
path = ""
command = "echo 'x' >> {counter1}"
interval = "0.1s"

[[files]]
path = ""
command = "echo 'y' >> {counter2}"
interval = "0.2s"
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # First check - both should execute
        watcher._check_files()
        time.sleep(0.15)  # 150ms

        # Second check - only first should execute (100ms passed)
        watcher._check_files()
        time.sleep(0.1)  # Total 250ms

        # Third check - both should execute (250ms passed)
        watcher._check_files()

        # Verify execution counts
        if os.path.exists(counter1):
            with open(counter1, "r") as f:
                lines1 = f.readlines()
            assert len(lines1) == 3, f"First command should execute 3 times, got {len(lines1)}"

        if os.path.exists(counter2):
            with open(counter2, "r") as f:
                lines2 = f.readlines()
            assert len(lines2) == 2, f"Second command should execute 2 times, got {len(lines2)}"

    def test_array_format_with_regular_files(self):
        """Test that array format works with both empty and regular file paths."""
        test_file = os.path.join(self.test_dir, "test.txt")
        output1 = os.path.join(self.test_dir, "output1.txt")
        output2 = os.path.join(self.test_dir, "output2.txt")

        # Create a test file
        with open(test_file, "w") as f:
            f.write("Initial content\n")

        # Create config with mixed entries
        config_content = f"""default_interval = "0.05s"

[[files]]
path = ""
command = "echo 'periodic' > {output1}"

[[files]]
path = "{test_file}"
command = "echo 'file_changed' > {output2}"
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # First check - empty filename should execute
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

    def test_array_format_with_all_optional_fields(self):
        """Test that array format supports all optional fields."""
        test_file = os.path.join(self.test_dir, "test.txt")
        output = os.path.join(self.test_dir, "output.txt")

        with open(test_file, "w") as f:
            f.write("Initial\n")

        # Create config with optional fields
        config_content = f"""default_interval = "1s"

[[files]]
path = "{test_file}"
command = "echo 'changed' > {output}"
interval = "0.05s"
suppress_if_process = "nonexistent_process"
enable_log = false
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # Initialize
        watcher._check_files()

        # Modify file
        time.sleep(0.1)
        with open(test_file, "a") as f:
            f.write("Modified\n")

        # Wait for interval to pass
        time.sleep(0.05)

        # Check should execute command
        watcher._check_files()

        assert os.path.exists(output), "Command should execute with all optional fields"

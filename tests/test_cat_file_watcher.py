#!/usr/bin/env python3
"""
Basic tests for cat_file_watcher
"""

import os
import shutil
import sys
import tempfile
import time

# Add src directory to path to import the module
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from cat_file_watcher import FileWatcher


class TestFileWatcher:
    """Test cases for FileWatcher class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, "test_config.toml")
        self.test_file = os.path.join(self.test_dir, "test.txt")

        # Create a test file
        with open(self.test_file, "w") as f:
            f.write("Initial content\n")

        # Create a test config
        config_content = f'''[[files]]
path = "{self.test_file}"
command = "echo 'File changed'"

'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_load_config(self):
        """Test that configuration is loaded correctly."""
        watcher = FileWatcher(self.config_file)
        assert "files" in watcher.config
        # Check that the test file path is in the files list (as array of tables)
        assert any(entry.get("path") == self.test_file for entry in watcher.config["files"])

    def test_get_file_timestamp(self):
        """Test that file timestamps are retrieved correctly."""
        watcher = FileWatcher(self.config_file)
        timestamp = watcher._get_file_timestamp(self.test_file)
        assert timestamp is not None
        assert isinstance(timestamp, float)

    def test_get_nonexistent_file_timestamp(self):
        """Test that nonexistent files return None for timestamp."""
        watcher = FileWatcher(self.config_file)
        timestamp = watcher._get_file_timestamp("/nonexistent/file.txt")
        assert timestamp is None

    def test_check_files_initializes_timestamps(self):
        """Test that checking files initializes timestamp tracking."""
        watcher = FileWatcher(self.config_file)
        assert len(watcher.file_timestamps) == 0
        watcher._check_files()
        assert len(watcher.file_timestamps) == 1
        # With array format, we use index-based keys
        assert "#0" in watcher.file_timestamps

    def test_detect_file_change(self):
        """Test that file changes are detected."""
        watcher = FileWatcher(self.config_file)

        # Initialize tracking
        watcher._check_files()
        initial_timestamp = watcher.file_timestamps["#0"]

        # Wait a bit and modify the file
        time.sleep(0.1)
        with open(self.test_file, "a") as f:
            f.write("Modified content\n")

        # Check again - timestamp should be different
        new_timestamp = watcher._get_file_timestamp(self.test_file)
        assert initial_timestamp != new_timestamp

    def test_default_interval(self):
        """Test that default interval is used when not specified."""
        watcher = FileWatcher(self.config_file)
        settings = {}
        interval = watcher._get_interval_for_file(settings)
        # Default is "1s" = 1 second
        assert interval == 1.0

    def test_custom_default_interval(self):
        """Test that custom default interval is respected."""
        # Create config with custom default interval
        config_content = f'''default_interval = "0.5s"

[[files]]
path = "{self.test_file}"

'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)
        settings = {}
        interval = watcher._get_interval_for_file(settings)
        # Custom default is "0.5s" = 0.5 second
        assert interval == 0.5

    def test_per_file_interval(self):
        """Test that per-file interval overrides default."""
        # Create config with per-file interval
        config_content = f'''default_interval = "1s"

[[files]]
path = "{self.test_file}"
command = "echo 'File changed'"
interval = "0.25s"

'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)
        settings = watcher.config["files"][0]
        interval = watcher._get_interval_for_file(settings)
        # Per-file interval is "0.25s" = 0.25 second
        assert interval == 0.25

    def test_interval_throttling(self):
        """Test that files are not checked more frequently than their interval."""
        # Create config with a longer interval
        config_content = f'''default_interval = "0.5s"

[[files]]
path = "{self.test_file}"
command = "echo 'File changed'"

'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # First check should process the file
        watcher._check_files()
        assert "#0" in watcher.file_last_check
        first_check_time = watcher.file_last_check["#0"]

        # Immediate second check should skip the file (not enough time passed)
        time.sleep(0.05)  # Much less than 0.5s
        watcher._check_files()
        # Check time should not have changed
        assert watcher.file_last_check["#0"] == first_check_time

        # After waiting for the interval, file should be checked again
        time.sleep(0.5)  # Wait for 0.5s interval
        watcher._check_files()
        # Check time should have been updated
        assert watcher.file_last_check["#0"] > first_check_time

    def test_process_detection(self):
        """Test that process detection works correctly."""
        watcher = FileWatcher(self.config_file)

        # Test that current python process is detected
        # The process name should be "python" or "python3"
        result = watcher._is_process_running(r"python")
        assert result, "Should detect running python process"

        # Test with a non-existent process
        result = watcher._is_process_running(r"nonexistent_process_xyz123")
        assert not result, "Should not detect non-existent process"

    def test_process_detection_with_regex(self):
        """Test that process detection works with regex patterns."""
        watcher = FileWatcher(self.config_file)

        # Test regex pattern matching
        result = watcher._is_process_running(r"python[23]?")
        assert result, "Should detect python process with regex"

        # Test case-insensitive matching (just ensure it doesn't crash)
        result = watcher._is_process_running(r"(?i)PYTHON")
        # Result may vary based on process name case, but should not crash
        assert isinstance(result, bool)

    def test_process_detection_invalid_regex(self):
        """Test that invalid regex patterns are handled gracefully."""
        watcher = FileWatcher(self.config_file)

        # Invalid regex pattern
        result = watcher._is_process_running(r"[invalid(regex")
        assert not result, "Should return False for invalid regex"

    def test_command_suppression_when_process_exists(self):
        """Test that command execution is suppressed when specified process exists."""
        # Create a test file that will be modified
        test_output = os.path.join(self.test_dir, "output.txt")

        # Create config with suppress_if_process for a running process (python)
        # Use short interval to speed up test
        config_content = f'''default_interval = "0.05s"

[[files]]
path = "{self.test_file}"
command = "echo 'executed' > {test_output}"
suppress_if_process = "python"

'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # Initialize tracking
        watcher._check_files()

        # Modify the file
        time.sleep(0.1)
        with open(self.test_file, "a") as f:
            f.write("Modified content\n")

        # Check files - command should be suppressed
        watcher._check_files()

        # Output file should NOT be created because command was suppressed
        assert not os.path.exists(test_output), "Command should have been suppressed, output file should not exist"

    def test_command_execution_when_process_not_exists(self):
        """Test that command executes normally when specified process doesn't exist."""
        # Create a test file that will be modified
        test_output = os.path.join(self.test_dir, "output.txt")

        # Create config with suppress_if_process for a non-existent process
        # Use short interval to speed up test
        config_content = f'''default_interval = "0.05s"

[[files]]
path = "{self.test_file}"
command = "echo 'executed' > {test_output}"
suppress_if_process = "nonexistent_process_xyz123"

'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # Initialize tracking
        watcher._check_files()

        # Modify the file
        time.sleep(0.1)
        with open(self.test_file, "a") as f:
            f.write("Modified content\n")

        # Check files - command should execute
        watcher._check_files()

        # Output file should be created because process doesn't exist
        assert os.path.exists(test_output), "Command should have executed, output file should exist"

    def test_command_execution_without_suppress_if_process(self):
        """Test that commands execute normally when suppress_if_process is not specified."""
        # Create a test file that will be modified
        test_output = os.path.join(self.test_dir, "output.txt")

        # Create config without suppress_if_process
        # Use short interval to speed up test
        config_content = f'''default_interval = "0.05s"

[[files]]
path = "{self.test_file}"
command = "echo 'executed' > {test_output}"

'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # Initialize tracking
        watcher._check_files()

        # Modify the file
        time.sleep(0.1)
        with open(self.test_file, "a") as f:
            f.write("Modified content\n")

        # Check files - command should execute
        watcher._check_files()

        # Output file should be created
        assert os.path.exists(test_output), "Command should have executed, output file should exist"

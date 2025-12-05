#!/usr/bin/env python3
"""
Test cases for terminate_if_window_title functionality
"""

import os
import shutil
import sys
import tempfile

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from cat_file_watcher import FileWatcher
from process_detector import ProcessDetector


class TestTerminateIfWindowTitle:
    """Test cases for terminate_if_window_title functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, "test_config.toml")
        self.error_log_file = os.path.join(self.test_dir, "error.log")

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_get_all_windows_by_title_on_non_windows(self):
        """Test that get_all_windows_by_title returns empty list on non-Windows platforms."""
        if sys.platform == "win32":
            # Skip this test on Windows since behavior is different
            return

        # On non-Windows platforms, should return empty list and print warning
        result = ProcessDetector.get_all_windows_by_title(".*")
        assert result == [], "Should return empty list on non-Windows platforms"

    def test_get_all_windows_by_title_invalid_regex(self):
        """Test that invalid regex is handled gracefully."""
        result = ProcessDetector.get_all_windows_by_title(r"[invalid(regex")
        assert isinstance(result, list), "Should return a list"
        assert len(result) == 0, "Should return empty list for invalid regex"

    def test_terminate_if_window_title_with_nonempty_filename_error(self):
        """Test that error is raised when terminate_if_window_title is used with non-empty filename."""
        test_file = os.path.join(self.test_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("test content\n")

        # Create config with terminate_if_window_title on non-empty filename
        config_content = f"""default_interval = "0.05s"
error_log_file = "{self.error_log_file}"

[[files]]
path = "{test_file}"
terminate_if_window_title = "Test Window"

"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # Execute check - should log fatal error and continue
        watcher._check_files()

        # Verify error was logged
        assert os.path.exists(self.error_log_file), "Error log should exist"
        with open(self.error_log_file, "r") as f:
            log_content = f.read()
        assert "Fatal configuration error" in log_content, "Fatal error should be logged"
        assert "empty filename" in log_content, "Error should mention empty filename requirement"

    def test_terminate_if_window_title_with_command_error(self):
        """Test that error is raised when terminate_if_window_title is used with command field."""
        # Create config with both terminate_if_window_title and command
        config_content = f"""default_interval = "0.05s"
error_log_file = "{self.error_log_file}"

[[files]]
path = ""
command = "echo 'test'"
terminate_if_window_title = "Test Window"
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # Execute check - should log fatal error and continue
        watcher._check_files()

        # Verify error was logged
        assert os.path.exists(self.error_log_file), "Error log should exist"
        with open(self.error_log_file, "r") as f:
            log_content = f.read()
        assert "Fatal configuration error" in log_content, "Fatal error should be logged"
        assert "command must be empty" in log_content, "Error should mention command must be empty"

    def test_terminate_if_window_title_with_no_matches(self):
        """Test that no action is taken when no window matches."""
        # Create config with terminate_if_window_title for non-existent window
        config_content = f"""default_interval = "0.05s"
error_log_file = "{self.error_log_file}"

[[files]]
path = ""
terminate_if_window_title = "nonexistent_window_xyz123"
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # Execute check - should do nothing (no error)
        watcher._check_files()

        # No assertion needed - just verify it doesn't crash

    def test_terminate_if_window_title_array_with_no_matches(self):
        """Test that array of patterns with no matches doesn't cause errors."""
        config_content = f"""default_interval = "0.05s"
error_log_file = "{self.error_log_file}"

[[files]]
path = ""
terminate_if_window_title = ["nonexistent_abc", "nonexistent_xyz"]
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # Execute check - should do nothing (no error)
        watcher._check_files()

        # No assertion needed - just verify it doesn't crash


class TestProcessDetectorWindowEnhancements:
    """Test cases for ProcessDetector window-related enhancements."""

    def test_get_all_windows_by_title_returns_list(self):
        """Test that get_all_windows_by_title returns a list."""
        result = ProcessDetector.get_all_windows_by_title(r".*")
        assert isinstance(result, list), "Should return a list"

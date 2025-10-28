#!/usr/bin/env python3
"""
Tests for console messages when using empty filename entries
Verifies that meaningful information is displayed instead of empty strings
"""

import io
import os
import shutil
import sys
import tempfile
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from cat_file_watcher import FileWatcher


class TestEmptyFilenameMessages:
    """Test cases for console messages with empty filename."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, "config.toml")

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_suppress_message_shows_command_for_empty_filename(self):
        """Test that suppression message shows command when filename is empty."""
        test_command = "echo 'health check'"

        # Create config with empty filename and suppress_if_process
        config_content = f"""default_interval = "0.05s"

[[files]]
path = ""
command = "{test_command}"
suppress_if_process = "python"
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # Capture stdout to verify message
        captured_output = io.StringIO()
        with patch("sys.stdout", captured_output):
            watcher._check_files()

        output = captured_output.getvalue()

        # The message should contain the command, not empty filename
        assert "Skipping command" in output or "Skipping" in output
        # Should show the command text
        assert test_command in output or "echo" in output
        # Should NOT show empty quotes prominently at the start
        # (We're checking the message is informative)

    def test_execute_message_shows_command_for_empty_filename(self):
        """Test that execution message shows command when filename is empty."""
        test_output = os.path.join(self.test_dir, "output.txt")
        test_command = f"echo 'executed' > {test_output}"

        # Create config with empty filename
        config_content = f"""default_interval = "0.05s"

[[files]]
path = ""
command = "{test_command}"
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # Capture stdout to verify message
        captured_output = io.StringIO()
        with patch("sys.stdout", captured_output):
            watcher._check_files()

        output = captured_output.getvalue()

        # The message should contain the command being executed
        assert "Executing" in output
        # Should show the command text
        assert "echo" in output

    def test_suppress_message_shows_process_for_terminate_if_process(self):
        """Test that messages show process pattern for terminate_if_process."""
        process_pattern = "nonexistent_process_12345"

        # Create config with terminate_if_process
        config_content = f"""default_interval = "0.05s"

[[files]]
path = ""
terminate_if_process = "{process_pattern}"
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # Capture stdout to verify message (should be no output for non-existent process)
        captured_output = io.StringIO()
        with patch("sys.stdout", captured_output):
            watcher._check_files()

        # No message should appear when process doesn't exist
        # (This test just ensures no crash occurs)
        # The pattern name would appear if there were matches

#!/usr/bin/env python3
"""
Basic functionality tests for cat_file_watcher
"""

import os
import shutil
import sys
import tempfile
import time

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from cat_file_watcher import FileWatcher


class TestFileWatcherBasics:
    """Test cases for basic FileWatcher functionality."""

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
        assert isinstance(watcher.config["files"], list)
        assert len(watcher.config["files"]) == 1
        assert watcher.config["files"][0]["path"] == self.test_file

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

    def test_one_line_toml_format(self):
        """Test that one-line inline TOML format works correctly."""
        # Create a one-line config using inline table syntax
        one_line_config = os.path.join(self.test_dir, "one_line.toml")
        config_content = f'files = [{{path = "{self.test_file}", command = "echo changed"}}]'
        with open(one_line_config, "w") as f:
            f.write(config_content)

        # Verify the config loads correctly
        watcher = FileWatcher(one_line_config)
        assert "files" in watcher.config
        assert isinstance(watcher.config["files"], list)
        assert len(watcher.config["files"]) == 1
        assert watcher.config["files"][0]["path"] == self.test_file
        assert watcher.config["files"][0]["command"] == "echo changed"

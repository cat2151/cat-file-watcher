#!/usr/bin/env python3
"""
Test directory monitoring functionality
"""

import os
import sys
import tempfile
import time

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from cat_file_watcher import FileWatcher


class TestDirectoryMonitoring:
    """Test cases for directory monitoring functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, "test_config.toml")
        self.monitor_dir = os.path.join(self.test_dir, "monitored_dir")
        os.makedirs(self.monitor_dir)

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_directory_monitoring_basic(self):
        """Test that directories can be monitored like files."""
        config_content = f'''default_interval = 100

[files]
"{self.monitor_dir}" = {{ command = "echo 'Directory changed!'" }}
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # Initial check - should register the directory
        watcher._check_files()
        assert self.monitor_dir in watcher.file_timestamps, "Directory should be registered for monitoring"

    def test_directory_change_detection(self):
        """Test that directory changes are detected when files are added."""
        config_content = f'''default_interval = 100

[files]
"{self.monitor_dir}" = {{ command = "echo 'Directory changed!'" }}
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # Initial check
        watcher._check_files()
        old_timestamp = watcher.file_timestamps.get(self.monitor_dir)
        assert old_timestamp is not None, "Directory should have an initial timestamp"

        # Wait and modify the directory by adding a file
        time.sleep(0.1)
        test_file = os.path.join(self.monitor_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("test")

        # Wait to ensure mtime changes
        time.sleep(0.1)

        # Check again - should detect the change
        watcher._check_files()
        new_timestamp = watcher.file_timestamps.get(self.monitor_dir)
        
        assert new_timestamp is not None, "Directory should still have a timestamp"
        assert new_timestamp != old_timestamp, "Directory timestamp should have changed after file addition"

    def test_directory_with_custom_interval(self):
        """Test that custom intervals work for directories."""
        config_content = f'''default_interval = 1000

[files]
"{self.monitor_dir}" = {{ command = "echo 'Directory changed!'", interval = 500 }}
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)
        
        # Verify the interval is set correctly (500ms = 0.5 seconds)
        settings = watcher.config["files"][self.monitor_dir]
        interval = watcher._get_interval_for_file(settings)
        assert interval == 0.5, f"Expected interval of 0.5 seconds, got {interval}"

    def test_directory_with_suppress_if_process(self):
        """Test that process suppression works for directories."""
        config_content = f'''default_interval = 100

[files]
"{self.monitor_dir}" = {{ command = "echo 'Directory changed!'", suppress_if_process = "nonexistent_process_12345" }}
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)
        
        # Directory should be monitored normally since the process doesn't exist
        watcher._check_files()
        assert self.monitor_dir in watcher.file_timestamps, "Directory should be monitored"

    def test_mixed_files_and_directories(self):
        """Test monitoring both files and directories simultaneously."""
        test_file = os.path.join(self.test_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("initial")

        config_content = f'''default_interval = 100

[files]
"{test_file}" = {{ command = "echo 'File changed!'" }}
"{self.monitor_dir}" = {{ command = "echo 'Directory changed!'" }}
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # Initial check - both should be registered
        watcher._check_files()
        assert test_file in watcher.file_timestamps, "File should be monitored"
        assert self.monitor_dir in watcher.file_timestamps, "Directory should be monitored"

        # Modify both
        time.sleep(0.1)
        with open(test_file, "a") as f:
            f.write("modified")
        
        new_file = os.path.join(self.monitor_dir, "new.txt")
        with open(new_file, "w") as f:
            f.write("new")

        time.sleep(0.1)

        # Both changes should be detected
        file_old_ts = watcher.file_timestamps[test_file]
        dir_old_ts = watcher.file_timestamps[self.monitor_dir]
        
        watcher._check_files()
        
        assert watcher.file_timestamps[test_file] != file_old_ts, "File change should be detected"
        assert watcher.file_timestamps[self.monitor_dir] != dir_old_ts, "Directory change should be detected"

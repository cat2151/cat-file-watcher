#!/usr/bin/env python3
"""
Test that timestamp reset on config reload prevents false triggers.
This test verifies the fix for issue #129.
"""

import os
import shutil
import sys
import tempfile
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from cat_file_watcher import FileWatcher


class TestTimestampResetOnReload:
    """Test that timestamps are reset on config reload to prevent false triggers."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, "config.toml")
        self.test_file1 = os.path.join(self.test_dir, "file1.txt")
        self.test_file2 = os.path.join(self.test_dir, "file2.txt")
        self.test_file3 = os.path.join(self.test_dir, "file3.txt")
        self.output_file = os.path.join(self.test_dir, "output.txt")

        # Create test files
        with open(self.test_file1, "w") as f:
            f.write("file1 content\n")
        with open(self.test_file2, "w") as f:
            f.write("file2 content\n")
        with open(self.test_file3, "w") as f:
            f.write("file3 content\n")

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def test_timestamp_reset_prevents_false_triggers(self):
        """
        Test that timestamp reset on config reload prevents false command triggers.

        Scenario:
        1. Monitor file2 and file3 (file1 commented)
        2. file2 at index #0, file3 at index #1
        3. Check files to initialize timestamps
        4. Uncomment file1 in config (hot reload)
        5. file1 now at index #0, file2 at #1, file3 at #2
        6. After reload, timestamps should be reset to current state
        7. Checking files should NOT trigger commands (no false positives)
        """
        # Initial config with file1 commented
        initial_config = f'''default_interval = "1s"
config_check_interval = "0.1s"

# [[files]]
# path = "{self.test_file1}"
# command = "echo 'file1 changed' >> {self.output_file}"

[[files]]
path = "{self.test_file2}"
command = "echo 'file2 changed' >> {self.output_file}"

[[files]]
path = "{self.test_file3}"
command = "echo 'file3 changed' >> {self.output_file}"
'''
        with open(self.config_file, "w") as f:
            f.write(initial_config)

        watcher = FileWatcher(self.config_file)

        # Check files once to initialize timestamps
        watcher._check_files()

        # Verify initial state
        assert "#0" in watcher.file_timestamps  # file2
        assert "#1" in watcher.file_timestamps  # file3
        assert len(watcher.file_timestamps) == 2

        # Uncomment file1 in config
        time.sleep(0.2)
        new_config = f'''default_interval = "1s"
config_check_interval = "0.1s"

[[files]]
path = "{self.test_file1}"
command = "echo 'file1 changed' >> {self.output_file}"

[[files]]
path = "{self.test_file2}"
command = "echo 'file2 changed' >> {self.output_file}"

[[files]]
path = "{self.test_file3}"
command = "echo 'file3 changed' >> {self.output_file}"
'''
        with open(self.config_file, "w") as f:
            f.write(new_config)

        # Trigger config reload
        time.sleep(0.15)
        watcher._check_config_file()

        # After reload, timestamps should be reset
        # All three files should now have current timestamps
        assert "#0" in watcher.file_timestamps  # file1
        assert "#1" in watcher.file_timestamps  # file2
        assert "#2" in watcher.file_timestamps  # file3
        assert len(watcher.file_timestamps) == 3

        # Get current file timestamps
        file1_ts = watcher._get_file_timestamp(self.test_file1)
        file2_ts = watcher._get_file_timestamp(self.test_file2)
        file3_ts = watcher._get_file_timestamp(self.test_file3)

        # Timestamps should match current file state
        assert watcher.file_timestamps["#0"] == file1_ts
        assert watcher.file_timestamps["#1"] == file2_ts
        assert watcher.file_timestamps["#2"] == file3_ts

        # Check files - should NOT trigger any commands
        # because timestamps match current state
        watcher._check_files()

        # Output file should not exist (no commands executed)
        assert not os.path.exists(self.output_file)

    def test_timestamp_reset_clears_check_times(self):
        """Test that file_last_check is also cleared on reload."""
        config = f'''default_interval = "1s"
config_check_interval = "0.1s"

[[files]]
path = "{self.test_file1}"
command = "echo 'test'"
'''
        with open(self.config_file, "w") as f:
            f.write(config)

        watcher = FileWatcher(self.config_file)
        watcher._check_files()

        # Set some check times
        watcher.file_last_check["#0"] = time.time()
        assert len(watcher.file_last_check) > 0

        # Modify config to trigger reload
        time.sleep(0.2)
        new_config = f'''default_interval = "2s"
config_check_interval = "0.1s"

[[files]]
path = "{self.test_file1}"
command = "echo 'test'"
'''
        with open(self.config_file, "w") as f:
            f.write(new_config)

        time.sleep(0.15)
        watcher._check_config_file()

        # file_last_check should be cleared
        assert len(watcher.file_last_check) == 0

    def test_timestamp_reset_handles_no_files_section(self):
        """Test that timestamp reset handles config without files section."""
        config = """default_interval = "1s"
config_check_interval = "0.1s"
"""
        with open(self.config_file, "w") as f:
            f.write(config)

        watcher = FileWatcher(self.config_file)

        # Modify config to trigger reload
        time.sleep(0.2)
        new_config = """default_interval = "2s"
config_check_interval = "0.1s"
"""
        with open(self.config_file, "w") as f:
            f.write(new_config)

        time.sleep(0.15)
        # Should not crash
        watcher._check_config_file()

        # Timestamps should be empty
        assert len(watcher.file_timestamps) == 0
        assert len(watcher.file_last_check) == 0

    def test_timestamp_reset_handles_empty_paths(self):
        """Test that timestamp reset correctly handles empty path entries."""
        config = f'''default_interval = "1s"
config_check_interval = "0.1s"

[[files]]
path = ""
command = "echo 'periodic task'"

[[files]]
path = "{self.test_file1}"
command = "echo 'file1 changed'"
'''
        with open(self.config_file, "w") as f:
            f.write(config)

        watcher = FileWatcher(self.config_file)
        watcher._check_files()

        # Modify config to trigger reload
        time.sleep(0.2)
        with open(self.config_file, "w") as f:
            f.write(config)  # Same config to trigger reload

        time.sleep(0.15)
        watcher._check_config_file()

        # Only file1 should have timestamp (empty path should not)
        assert "#1" in watcher.file_timestamps  # file1
        assert "#0" not in watcher.file_timestamps  # empty path entry
        assert len(watcher.file_timestamps) == 1

#!/usr/bin/env python3
"""
Test case to demonstrate issue #129:
When TOML lines are uncommented (adding elements), unintended command launches can occur
because of numeric index-based tracking.
"""

import os
import shutil
import sys
import tempfile
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from cat_file_watcher import FileWatcher


class TestIssue129:
    """Test cases for issue #129 - numeric index tracking problems."""

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

    def test_index_shift_on_uncomment(self):
        """
        Test that demonstrates the issue when uncommenting TOML entries.
        
        Scenario:
        1. Start with file2 and file3 monitored (file1 commented out)
        2. file2 is at index 0, file3 is at index 1
        3. Modify file2 to establish its timestamp
        4. Uncomment file1 in config (hot reload)
        5. Now file1 is at index 0, file2 is at index 1, file3 is at index 2
        6. The old timestamp for index 0 (file2) is now associated with file1
        7. This could cause unintended command execution
        """
        # Initial config with file1 commented out
        initial_config = f'''default_interval = "1s"
config_check_interval = "0.1s"

# Commented out initially
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
        
        # Verify initial state: file2 is at index 0, file3 is at index 1
        assert "#0" in watcher.file_timestamps  # file2
        assert "#1" in watcher.file_timestamps  # file3
        file2_initial_timestamp = watcher.file_timestamps["#0"]
        file3_initial_timestamp = watcher.file_timestamps["#1"]
        
        # Modify file2 to update its timestamp
        time.sleep(0.1)
        with open(self.test_file2, "w") as f:
            f.write("file2 modified\n")
        
        # Check and execute command for file2
        watcher._check_files()
        
        # Now uncomment file1 in the config (simulating hot reload)
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
        
        # After reload, indices have shifted:
        # - file1 is now at index 0 (was nothing)
        # - file2 is now at index 1 (was at index 0)
        # - file3 is now at index 2 (was at index 1)
        
        # Print state for debugging
        print(f"File timestamps after reload: {watcher.file_timestamps}")
        
        # The problem: old timestamp associations still exist
        # If we check files now, file1 at index 0 might have file2's old timestamp
        watcher._check_files()
        
        # This demonstrates the potential for unintended behavior
        # The timestamps dictionary should be properly updated or reset on config reload

    def test_hash_based_tracking_concept(self):
        """
        Test demonstrating a potential solution: hash-based tracking instead of index.
        
        This test shows how using file path as the key would solve the issue.
        """
        # This is a conceptual test showing what should happen
        # File tracking should be based on file path, not numeric index
        
        # Create a simple tracking dict using file path
        file_tracking = {}
        
        # Scenario 1: Initial state with file2 and file3
        file_tracking[self.test_file2] = os.path.getmtime(self.test_file2)
        file_tracking[self.test_file3] = os.path.getmtime(self.test_file3)
        
        # Modify file2
        time.sleep(0.1)
        with open(self.test_file2, "w") as f:
            f.write("modified\n")
        
        # Check file2 - timestamp changed
        new_timestamp = os.path.getmtime(self.test_file2)
        assert new_timestamp != file_tracking[self.test_file2]
        file_tracking[self.test_file2] = new_timestamp
        
        # Scenario 2: Add file1 to tracking (simulating uncomment)
        file_tracking[self.test_file1] = os.path.getmtime(self.test_file1)
        
        # The tracking for file2 and file3 remains correct
        # No index shift issues occur
        assert self.test_file2 in file_tracking
        assert self.test_file3 in file_tracking
        assert self.test_file1 in file_tracking

    def test_timestamp_reset_on_reload(self):
        """
        Test whether timestamps are reset on config reload.
        
        Expected behavior: When config is reloaded, all file timestamps should be
        updated to current values to prevent false triggers.
        """
        config = f'''default_interval = "1s"
config_check_interval = "0.1s"

[[files]]
path = "{self.test_file1}"
command = "echo 'file1 changed' >> {self.output_file}"
'''
        with open(self.config_file, "w") as f:
            f.write(config)

        watcher = FileWatcher(self.config_file)
        
        # Initialize by checking files
        watcher._check_files()
        assert "#0" in watcher.file_timestamps
        old_timestamp = watcher.file_timestamps["#0"]
        
        # Modify config (but keep same structure)
        time.sleep(0.2)
        new_config = f'''default_interval = "2s"
config_check_interval = "0.1s"

[[files]]
path = "{self.test_file1}"
command = "echo 'file1 changed' >> {self.output_file}"
'''
        with open(self.config_file, "w") as f:
            f.write(new_config)
        
        # Trigger reload
        time.sleep(0.15)
        watcher._check_config_file()
        
        # After reload, file timestamps should be updated to current state
        # to avoid triggering commands for unchanged files
        watcher._check_files()
        
        # The timestamp should be updated to prevent false triggers
        print(f"Old timestamp: {old_timestamp}")
        print(f"Current timestamps: {watcher.file_timestamps}")

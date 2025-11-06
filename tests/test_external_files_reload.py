#!/usr/bin/env python3
"""
Tests for external files reload functionality
"""

import os
import shutil
import sys
import tempfile
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from cat_file_watcher import FileWatcher


class TestExternalFilesReload:
    """Test cases for external files reload functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, "config.toml")
        self.external_file = os.path.join(self.test_dir, "external.toml")
        self.test_file = os.path.join(self.test_dir, "test.txt")

        # Create a test file
        with open(self.test_file, "w") as f:
            f.write("Initial content\n")

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def test_external_file_reload_on_change(self):
        """Test that config is reloaded when an external file changes."""
        # Create external file with a files entry
        external_content = f'''[[files]]
path = "{self.test_file}"
command = "echo 'original command'"
'''
        with open(self.external_file, "w") as f:
            f.write(external_content)

        # Create main config that references external file
        config_content = f'''default_interval = "1s"
config_check_interval = "0.1s"
external_files = ["{self.external_file}"]
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Create watcher and check initial state
        watcher = FileWatcher(self.config_file)
        assert len(watcher.config["files"]) == 1
        assert watcher.config["files"][0]["command"] == "echo 'original command'"

        # Verify external file is being tracked
        assert len(watcher.external_file_paths) == 1
        assert watcher.external_file_paths[0] == self.external_file
        assert self.external_file in watcher.external_file_timestamps

        # Wait a bit and modify the external file
        time.sleep(0.2)
        new_external_content = f'''[[files]]
path = "{self.test_file}"
command = "echo 'updated command'"
'''
        with open(self.external_file, "w") as f:
            f.write(new_external_content)

        # Check for config changes
        time.sleep(0.15)  # Wait for the config check interval
        watcher._check_config_file()

        # Verify config was reloaded with updated external file content
        assert len(watcher.config["files"]) == 1
        assert watcher.config["files"][0]["command"] == "echo 'updated command'"

    def test_external_file_timestamp_tracking(self):
        """Test that external file timestamps are properly tracked."""
        # Create external file
        external_content = f'''[[files]]
path = "{self.test_file}"
command = "echo 'test'"
'''
        with open(self.external_file, "w") as f:
            f.write(external_content)

        # Create main config
        config_content = f'''default_interval = "1s"
external_files = ["{self.external_file}"]
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Create watcher
        watcher = FileWatcher(self.config_file)

        # Verify timestamp is tracked
        assert self.external_file in watcher.external_file_timestamps
        initial_timestamp = watcher.external_file_timestamps[self.external_file]
        assert initial_timestamp is not None

    def test_multiple_external_files_reload(self):
        """Test that config is reloaded when any of multiple external files changes."""
        external_file2 = os.path.join(self.test_dir, "external2.toml")
        test_file2 = os.path.join(self.test_dir, "test2.txt")

        # Create first external file
        external1_content = f'''[[files]]
path = "{self.test_file}"
command = "echo 'file1 original'"
'''
        with open(self.external_file, "w") as f:
            f.write(external1_content)

        # Create second external file
        external2_content = f'''[[files]]
path = "{test_file2}"
command = "echo 'file2 original'"
'''
        with open(external_file2, "w") as f:
            f.write(external2_content)

        # Create main config that references both external files
        config_content = f'''default_interval = "1s"
config_check_interval = "0.1s"
external_files = ["{self.external_file}", "{external_file2}"]
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Create watcher and check initial state
        watcher = FileWatcher(self.config_file)
        assert len(watcher.config["files"]) == 2
        assert len(watcher.external_file_paths) == 2

        # Wait a bit and modify the second external file
        time.sleep(0.2)
        new_external2_content = f'''[[files]]
path = "{test_file2}"
command = "echo 'file2 updated'"
'''
        with open(external_file2, "w") as f:
            f.write(new_external2_content)

        # Check for config changes
        time.sleep(0.15)
        watcher._check_config_file()

        # Verify config was reloaded
        assert len(watcher.config["files"]) == 2
        # Find the updated entry
        file2_entries = [f for f in watcher.config["files"] if f["path"] == test_file2]
        assert len(file2_entries) == 1
        assert file2_entries[0]["command"] == "echo 'file2 updated'"

    def test_external_file_list_changes_on_reload(self):
        """Test that external file tracking is updated when the external_files list changes."""
        external_file2 = os.path.join(self.test_dir, "external2.toml")

        # Create first external file
        external1_content = f'''[[files]]
path = "{self.test_file}"
command = "echo 'file1'"
'''
        with open(self.external_file, "w") as f:
            f.write(external1_content)

        # Create second external file
        external2_content = f'''[[files]]
path = "{self.test_file}"
command = "echo 'file2'"
'''
        with open(external_file2, "w") as f:
            f.write(external2_content)

        # Create main config with only first external file
        config_content = f'''default_interval = "1s"
config_check_interval = "0.1s"
external_files = ["{self.external_file}"]
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Create watcher
        watcher = FileWatcher(self.config_file)
        assert len(watcher.external_file_paths) == 1
        assert watcher.external_file_paths[0] == self.external_file

        # Wait and modify main config to add second external file
        time.sleep(0.2)
        new_config_content = f'''default_interval = "1s"
config_check_interval = "0.1s"
external_files = ["{self.external_file}", "{external_file2}"]
'''
        with open(self.config_file, "w") as f:
            f.write(new_config_content)

        # Check for config changes
        time.sleep(0.15)
        watcher._check_config_file()

        # Verify external file tracking was updated
        assert len(watcher.external_file_paths) == 2
        assert self.external_file in watcher.external_file_paths
        assert external_file2 in watcher.external_file_paths
        assert external_file2 in watcher.external_file_timestamps

    def test_external_file_reload_preserves_state_on_error(self):
        """Test that external file reload errors don't break the watcher."""
        # Create external file
        external_content = f'''[[files]]
path = "{self.test_file}"
command = "echo 'original'"
'''
        with open(self.external_file, "w") as f:
            f.write(external_content)

        # Create main config
        config_content = f'''default_interval = "1s"
config_check_interval = "0.1s"
external_files = ["{self.external_file}"]
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Create watcher
        watcher = FileWatcher(self.config_file)
        original_config = watcher.config.copy()

        # Wait and write invalid TOML to external file
        time.sleep(0.2)
        with open(self.external_file, "w") as f:
            f.write("invalid toml [[[")

        # Check for config changes
        time.sleep(0.15)
        watcher._check_config_file()

        # Config should remain unchanged (previous config preserved)
        assert len(watcher.config["files"]) == len(original_config["files"])
        assert watcher.config["files"][0]["command"] == "echo 'original'"

    def test_relative_path_external_file_reload(self):
        """Test that external files with relative paths are properly monitored."""
        # Create subdirectory for external file
        subdir = os.path.join(self.test_dir, "configs")
        os.makedirs(subdir)
        external_file = os.path.join(subdir, "external.toml")

        # Create external file
        external_content = f'''[[files]]
path = "{self.test_file}"
command = "echo 'original'"
'''
        with open(external_file, "w") as f:
            f.write(external_content)

        # Create main config with relative path
        config_content = """default_interval = "1s"
config_check_interval = "0.1s"
external_files = ["configs/external.toml"]
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Create watcher
        watcher = FileWatcher(self.config_file)
        assert len(watcher.external_file_paths) == 1
        # Path should be resolved to absolute
        assert watcher.external_file_paths[0] == external_file

        # Wait and modify the external file
        time.sleep(0.2)
        new_external_content = f'''[[files]]
path = "{self.test_file}"
command = "echo 'updated'"
'''
        with open(external_file, "w") as f:
            f.write(new_external_content)

        # Check for config changes
        time.sleep(0.15)
        watcher._check_config_file()

        # Verify config was reloaded
        assert watcher.config["files"][0]["command"] == "echo 'updated'"

    def test_no_external_files_specified(self):
        """Test that watcher works correctly when no external files are specified."""
        # Create main config without external_files
        config_content = f'''default_interval = "1s"

[[files]]
path = "{self.test_file}"
command = "echo 'test'"
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Create watcher
        watcher = FileWatcher(self.config_file)

        # Verify no external files are tracked
        assert len(watcher.external_file_paths) == 0
        assert len(watcher.external_file_timestamps) == 0

        # Config check should still work
        watcher._check_config_file()

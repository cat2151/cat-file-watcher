#!/usr/bin/env python3
"""
Tests for external TOML files functionality
"""

import os
import shutil
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from cat_file_watcher import FileWatcher
from config_loader import ConfigLoader


class TestExternalFiles:
    """Test cases for external files functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, "config.toml")
        self.external_file1 = os.path.join(self.test_dir, "external1.toml")
        self.external_file2 = os.path.join(self.test_dir, "external2.toml")
        self.test_file = os.path.join(self.test_dir, "test.txt")

        # Create a test file
        with open(self.test_file, "w") as f:
            f.write("Initial content\n")

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_external_files_basic(self):
        """Test loading a basic external file with files section."""
        # Create external file with files section
        external_content = f'''[files]
"{self.test_file}" = {{ command = "echo 'external command'" }}
'''
        with open(self.external_file1, "w") as f:
            f.write(external_content)

        # Create main config that references external file
        config_content = f'''default_interval = "1s"
external_files = ["{self.external_file1}"]
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Load config and verify files are merged
        config = ConfigLoader.load_config(self.config_file)
        assert "files" in config
        assert self.test_file in config["files"]
        assert config["files"][self.test_file]["command"] == "echo 'external command'"

    def test_external_files_multiple(self):
        """Test loading multiple external files."""
        # Create first external file
        external1_content = f'''[files]
"{self.test_file}" = {{ command = "echo 'file1'" }}
'''
        with open(self.external_file1, "w") as f:
            f.write(external1_content)

        # Create second external file
        test_file2 = os.path.join(self.test_dir, "test2.txt")
        external2_content = f'''[files]
"{test_file2}" = {{ command = "echo 'file2'" }}
'''
        with open(self.external_file2, "w") as f:
            f.write(external2_content)

        # Create main config that references both external files
        config_content = f'''default_interval = "1s"
external_files = ["{self.external_file1}", "{self.external_file2}"]
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Load config and verify both files are merged
        config = ConfigLoader.load_config(self.config_file)
        assert "files" in config
        assert self.test_file in config["files"]
        assert test_file2 in config["files"]
        assert config["files"][self.test_file]["command"] == "echo 'file1'"
        assert config["files"][test_file2]["command"] == "echo 'file2'"

    def test_external_files_merge_with_main(self):
        """Test that external files are merged with main config files section."""
        # Create external file
        external_content = f'''[files]
"{self.test_file}" = {{ command = "echo 'external'" }}
'''
        with open(self.external_file1, "w") as f:
            f.write(external_content)

        # Create main config with its own files section
        test_file2 = os.path.join(self.test_dir, "test2.txt")
        config_content = f'''default_interval = "1s"
external_files = ["{self.external_file1}"]

[files]
"{test_file2}" = {{ command = "echo 'main'" }}
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Load config and verify both are present
        config = ConfigLoader.load_config(self.config_file)
        assert "files" in config
        assert self.test_file in config["files"]
        assert test_file2 in config["files"]
        assert config["files"][self.test_file]["command"] == "echo 'external'"
        assert config["files"][test_file2]["command"] == "echo 'main'"

    def test_external_files_relative_path(self):
        """Test that relative paths in external_files are resolved relative to main config."""
        # Create subdirectory for external file
        subdir = os.path.join(self.test_dir, "configs")
        os.makedirs(subdir)
        external_file = os.path.join(subdir, "external.toml")

        # Create external file
        external_content = f'''[files]
"{self.test_file}" = {{ command = "echo 'test'" }}
'''
        with open(external_file, "w") as f:
            f.write(external_content)

        # Create main config with relative path
        config_content = """default_interval = "1s"
external_files = ["configs/external.toml"]
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Load config and verify file is loaded
        config = ConfigLoader.load_config(self.config_file)
        assert "files" in config
        assert self.test_file in config["files"]

    def test_external_files_invalid_section_error(self):
        """Test that external files with invalid sections raise an error."""
        # Create external file with time_periods section (not allowed)
        external_content = f'''[time_periods]
business_hours = {{ start = "09:00", end = "17:00" }}

[files]
"{self.test_file}" = {{ command = "echo 'test'" }}
'''
        with open(self.external_file1, "w") as f:
            f.write(external_content)

        # Create main config
        config_content = f'''default_interval = "1s"
external_files = ["{self.external_file1}"]
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Loading config should fail with SystemExit
        with pytest.raises(SystemExit) as cm:
            ConfigLoader.load_config(self.config_file)
        assert cm.value.code == 1

    def test_external_files_only_files_section_allowed(self):
        """Test that external files can only contain files section."""
        # Create external file with default_interval (not allowed)
        external_content = f'''default_interval = 2000

[files]
"{self.test_file}" = {{ command = "echo 'test'" }}
'''
        with open(self.external_file1, "w") as f:
            f.write(external_content)

        # Create main config
        config_content = f'''default_interval = "1s"
external_files = ["{self.external_file1}"]
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Loading config should fail
        with pytest.raises(SystemExit) as cm:
            ConfigLoader.load_config(self.config_file)
        assert cm.value.code == 1

    def test_external_files_not_found_error(self):
        """Test that missing external file raises an error."""
        # Create main config with non-existent external file
        config_content = """default_interval = "1s"
external_files = ["/nonexistent/file.toml"]
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Loading config should fail
        with pytest.raises(SystemExit) as cm:
            ConfigLoader.load_config(self.config_file)
        assert cm.value.code == 1

    def test_external_files_invalid_toml_error(self):
        """Test that invalid TOML in external file raises an error."""
        # Create external file with invalid TOML
        with open(self.external_file1, "w") as f:
            f.write("this is not valid toml [[[")

        # Create main config
        config_content = f'''default_interval = "1s"
external_files = ["{self.external_file1}"]
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Loading config should fail
        with pytest.raises(SystemExit) as cm:
            ConfigLoader.load_config(self.config_file)
        assert cm.value.code == 1

    def test_external_files_empty_list(self):
        """Test that empty external_files list works correctly."""
        # Create main config with empty external_files list
        config_content = f'''default_interval = "1s"
external_files = []

[files]
"{self.test_file}" = {{ command = "echo 'test'" }}
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Load config and verify it works
        config = ConfigLoader.load_config(self.config_file)
        assert "files" in config
        assert self.test_file in config["files"]

    def test_external_files_not_list_error(self):
        """Test that external_files must be a list."""
        # Create main config with external_files as string instead of list
        config_content = f'''default_interval = "1s"
external_files = "{self.external_file1}"
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Loading config should fail
        with pytest.raises(SystemExit) as cm:
            ConfigLoader.load_config(self.config_file)
        assert cm.value.code == 1

    def test_external_files_with_watcher(self):
        """Test that FileWatcher works correctly with external files."""
        # Create external file
        external_content = f'''[files]
"{self.test_file}" = {{ command = "echo 'external watcher'" }}
'''
        with open(self.external_file1, "w") as f:
            f.write(external_content)

        # Create main config
        config_content = f'''default_interval = "0.1s"
external_files = ["{self.external_file1}"]
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Create watcher and verify it can be initialized
        watcher = FileWatcher(self.config_file)
        assert "files" in watcher.config
        assert self.test_file in watcher.config["files"]

    def test_external_files_empty_files_section(self):
        """Test external file with empty files section."""
        # Create external file with empty files section
        external_content = """[files]
"""
        with open(self.external_file1, "w") as f:
            f.write(external_content)

        # Create main config
        config_content = f'''default_interval = "1s"
external_files = ["{self.external_file1}"]

[files]
"{self.test_file}" = {{ command = "echo 'main'" }}
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Load config and verify main files section still works
        config = ConfigLoader.load_config(self.config_file)
        assert "files" in config
        assert self.test_file in config["files"]

    def test_external_files_overwrite_main(self):
        """Test that external file can overwrite entries from main config."""
        # Create external file
        external_content = f'''[files]
"{self.test_file}" = {{ command = "echo 'from external'" }}
'''
        with open(self.external_file1, "w") as f:
            f.write(external_content)

        # Create main config with same file
        # Note: external_files must be before [files] section to be at top level
        config_content = f'''default_interval = "1s"
external_files = ["{self.external_file1}"]

[files]
"{self.test_file}" = {{ command = "echo 'from main'" }}
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Load config and verify external overwrites main
        config = ConfigLoader.load_config(self.config_file)
        assert "files" in config
        assert self.test_file in config["files"]
        # External files are loaded after main config, so they should overwrite
        assert config["files"][self.test_file]["command"] == "echo 'from external'"

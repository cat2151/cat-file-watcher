#!/usr/bin/env python3
"""
Tests for [[commands]] and [[processes]] sections
"""

import os
import shutil
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from cat_file_watcher import FileWatcher
from config_loader import ConfigLoader


class TestCommandsSection:
    """Test cases for [[commands]] section."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, "config.toml")

    def teardown_method(self):
        """Clean up test fixtures."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_commands_section_basic(self):
        """Test that [[commands]] section works with basic command."""
        output_file = os.path.join(self.test_dir, "output.txt")

        config_content = f"""default_interval = "0.1s"

[[commands]]
command = "echo 'test' > {output_file}"
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        config = ConfigLoader.load_config(self.config_file)

        # Verify that commands section was merged into files with path=""
        assert "files" in config
        assert len(config["files"]) == 1
        assert config["files"][0]["path"] == ""
        assert config["files"][0]["command"] == f"echo 'test' > {output_file}"

    def test_commands_section_multiple_entries(self):
        """Test that [[commands]] section supports multiple entries."""
        config_content = """default_interval = "0.1s"

[[commands]]
command = "echo 'cmd1'"
interval = "1s"

[[commands]]
command = "echo 'cmd2'"
interval = "2s"
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        config = ConfigLoader.load_config(self.config_file)

        # Verify that all commands were merged
        assert "files" in config
        assert len(config["files"]) == 2
        assert config["files"][0]["path"] == ""
        assert config["files"][0]["command"] == "echo 'cmd1'"
        assert config["files"][0]["interval"] == "1s"
        assert config["files"][1]["path"] == ""
        assert config["files"][1]["command"] == "echo 'cmd2'"
        assert config["files"][1]["interval"] == "2s"

    def test_commands_section_with_path_forbidden(self):
        """Test that [[commands]] section forbids 'path' field."""
        config_content = """default_interval = "0.1s"

[[commands]]
path = "some_file.txt"
command = "echo 'test'"
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        with pytest.raises(SystemExit):
            ConfigLoader.load_config(self.config_file)

    def test_commands_section_with_suppress_if_process(self):
        """Test that [[commands]] section works with suppress_if_process."""
        config_content = """default_interval = "0.1s"

[[commands]]
command = "echo 'test'"
suppress_if_process = "vim|emacs"
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        config = ConfigLoader.load_config(self.config_file)

        assert "files" in config
        assert config["files"][0]["suppress_if_process"] == "vim|emacs"

    def test_commands_section_execution(self):
        """Test that commands from [[commands]] section execute correctly."""
        output_file = os.path.join(self.test_dir, "output.txt")

        config_content = f"""default_interval = "0.1s"

[[commands]]
command = "echo 'executed' > {output_file}"
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)
        watcher._check_files()

        # Command should execute immediately
        assert os.path.exists(output_file)
        with open(output_file, "r") as f:
            assert "executed" in f.read()


class TestProcessesSection:
    """Test cases for [[processes]] section."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, "config.toml")

    def teardown_method(self):
        """Clean up test fixtures."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_processes_section_basic(self):
        """Test that [[processes]] section works with terminate_if_process."""
        config_content = """default_interval = "0.1s"

[[processes]]
terminate_if_process = "test_process"
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        config = ConfigLoader.load_config(self.config_file)

        # Verify that processes section was merged into files with path=""
        assert "files" in config
        assert len(config["files"]) == 1
        assert config["files"][0]["path"] == ""
        assert config["files"][0]["terminate_if_process"] == "test_process"

    def test_processes_section_with_path_forbidden(self):
        """Test that [[processes]] section forbids 'path' field."""
        config_content = """default_interval = "0.1s"

[[processes]]
path = "some_file.txt"
terminate_if_process = "test_process"
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        with pytest.raises(SystemExit):
            ConfigLoader.load_config(self.config_file)

    def test_processes_section_with_command_forbidden(self):
        """Test that [[processes]] section forbids 'command' field."""
        config_content = """default_interval = "0.1s"

[[processes]]
command = "echo 'test'"
terminate_if_process = "test_process"
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        with pytest.raises(SystemExit):
            ConfigLoader.load_config(self.config_file)

    def test_processes_section_multiple_entries(self):
        """Test that [[processes]] section supports multiple entries."""
        config_content = """default_interval = "0.1s"

[[processes]]
terminate_if_process = "process1"
interval = "1s"

[[processes]]
terminate_if_process = "process2"
interval = "2s"
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        config = ConfigLoader.load_config(self.config_file)

        # Verify that all processes were merged
        assert "files" in config
        assert len(config["files"]) == 2
        assert config["files"][0]["path"] == ""
        assert config["files"][0]["terminate_if_process"] == "process1"
        assert config["files"][0]["interval"] == "1s"
        assert config["files"][1]["path"] == ""
        assert config["files"][1]["terminate_if_process"] == "process2"
        assert config["files"][1]["interval"] == "2s"


class TestMixedSections:
    """Test cases for mixing [[files]], [[commands]], and [[processes]] sections."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, "config.toml")

    def teardown_method(self):
        """Clean up test fixtures."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_all_three_sections_together(self):
        """Test that [[files]], [[commands]], and [[processes]] sections work together."""
        test_file = os.path.join(self.test_dir, "test.txt")

        config_content = f"""default_interval = "0.1s"

[[files]]
path = "{test_file}"
command = "echo 'file changed'"

[[commands]]
command = "echo 'command executed'"
interval = "1s"

[[processes]]
terminate_if_process = "test_process"
interval = "2s"
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        config = ConfigLoader.load_config(self.config_file)

        # Verify that all sections were merged into files
        assert "files" in config
        assert len(config["files"]) == 3

        # Check files entry
        assert config["files"][0]["path"] == test_file
        assert config["files"][0]["command"] == "echo 'file changed'"

        # Check commands entry (merged with path="")
        assert config["files"][1]["path"] == ""
        assert config["files"][1]["command"] == "echo 'command executed'"
        assert config["files"][1]["interval"] == "1s"

        # Check processes entry (merged with path="")
        assert config["files"][2]["path"] == ""
        assert config["files"][2]["terminate_if_process"] == "test_process"
        assert config["files"][2]["interval"] == "2s"

    def test_external_files_with_commands_section(self):
        """Test that external files can contain [[commands]] section."""
        external_file = os.path.join(self.test_dir, "external.toml")

        external_content = """[[commands]]
command = "echo 'external command'"
"""
        with open(external_file, "w") as f:
            f.write(external_content)

        config_content = f"""default_interval = "0.1s"

external_files = ["{external_file}"]

[[files]]
path = "main.txt"
command = "echo 'main'"
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        config = ConfigLoader.load_config(self.config_file)

        # Verify that external commands were loaded
        assert "files" in config
        assert len(config["files"]) == 2
        assert any(entry.get("command") == "echo 'external command'" for entry in config["files"])

    def test_external_files_with_processes_section(self):
        """Test that external files can contain [[processes]] section."""
        external_file = os.path.join(self.test_dir, "external.toml")

        external_content = """[[processes]]
terminate_if_process = "external_process"
"""
        with open(external_file, "w") as f:
            f.write(external_content)

        config_content = f"""default_interval = "0.1s"

external_files = ["{external_file}"]
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        config = ConfigLoader.load_config(self.config_file)

        # Verify that external processes were loaded
        assert "files" in config
        assert len(config["files"]) == 1
        assert config["files"][0]["terminate_if_process"] == "external_process"

    def test_validation_order(self):
        """Test that validation happens before merging."""
        # This ensures that validation catches errors in commands section
        # before they're merged into files section
        config_content = """default_interval = "0.1s"

[[commands]]
path = "forbidden.txt"
command = "echo 'test'"
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Should fail validation with clear error message about commands section
        with pytest.raises(SystemExit):
            ConfigLoader.load_config(self.config_file)


class TestArrayFormatValidation:
    """Test cases for array of tables format validation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, "config.toml")

    def teardown_method(self):
        """Clean up test fixtures."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_commands_section_must_be_array(self):
        """Test that [[commands]] section must use array format."""
        # This would be invalid: [commands] instead of [[commands]]
        # However, TOML will parse it differently, so we test the validation
        config_content = """default_interval = "0.1s"

[commands]
cmd1 = { command = "echo 'test'" }
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        with pytest.raises(SystemExit):
            ConfigLoader.load_config(self.config_file)

    def test_processes_section_must_be_array(self):
        """Test that [[processes]] section must use array format."""
        config_content = """default_interval = "0.1s"

[processes]
proc1 = { terminate_if_process = "test" }
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        with pytest.raises(SystemExit):
            ConfigLoader.load_config(self.config_file)

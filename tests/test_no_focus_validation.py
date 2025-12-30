#!/usr/bin/env python3
"""
Tests for no_focus command validation
"""

import os
import sys
import tempfile
import unittest


class TestNoFocusValidation(unittest.TestCase):
    """Test cases for no_focus command validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, "config.toml")

        # Add src directory to path for imports
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

    def tearDown(self):
        """Clean up test files."""
        import shutil

        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_no_focus_with_start_command_should_error(self):
        """Test that no_focus=true with 'start' command at beginning raises error."""
        # Create config with no_focus=true and command starting with "start"
        config_content = """
default_interval = "1s"

[[files]]
path = "test.txt"
command = "start notepad.exe"
no_focus = true
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Import ConfigLoader
        from config_loader import ConfigLoader

        # This should raise SystemExit
        with self.assertRaises(SystemExit):
            ConfigLoader.load_config(self.config_file)

    def test_no_focus_with_start_uppercase_command_should_error(self):
        """Test that no_focus=true with 'START' command (uppercase) raises error."""
        # Create config with no_focus=true and command starting with "START"
        config_content = """
default_interval = "1s"

[[files]]
path = "test.txt"
command = "START notepad.exe"
no_focus = true
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Import ConfigLoader
        from config_loader import ConfigLoader

        # This should raise SystemExit
        with self.assertRaises(SystemExit):
            ConfigLoader.load_config(self.config_file)

    def test_no_focus_with_start_mixed_case_command_should_error(self):
        """Test that no_focus=true with 'Start' command (mixed case) raises error."""
        # Create config with no_focus=true and command starting with "Start"
        config_content = """
default_interval = "1s"

[[files]]
path = "test.txt"
command = "Start notepad.exe"
no_focus = true
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Import ConfigLoader
        from config_loader import ConfigLoader

        # This should raise SystemExit
        with self.assertRaises(SystemExit):
            ConfigLoader.load_config(self.config_file)

    def test_no_focus_without_start_command_should_succeed(self):
        """Test that no_focus=true without 'start' command succeeds."""
        # Create config with no_focus=true and normal command
        config_content = """
default_interval = "1s"

[[files]]
path = "test.txt"
command = "python script.py"
no_focus = true
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Import ConfigLoader
        from config_loader import ConfigLoader

        # This should NOT raise an exception
        config = ConfigLoader.load_config(self.config_file)
        self.assertIsNotNone(config)
        self.assertTrue(config["files"][0]["no_focus"])

    def test_no_focus_false_with_start_command_should_succeed(self):
        """Test that no_focus=false with 'start' command succeeds."""
        # Create config with no_focus=false and command starting with "start"
        config_content = """
default_interval = "1s"

[[files]]
path = "test.txt"
command = "start notepad.exe"
no_focus = false
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Import ConfigLoader
        from config_loader import ConfigLoader

        # This should NOT raise an exception
        config = ConfigLoader.load_config(self.config_file)
        self.assertIsNotNone(config)
        self.assertFalse(config["files"][0]["no_focus"])

    def test_no_focus_not_specified_with_start_command_should_succeed(self):
        """Test that no_focus not specified (defaults to false) with 'start' command succeeds."""
        # Create config without no_focus and command starting with "start"
        config_content = """
default_interval = "1s"

[[files]]
path = "test.txt"
command = "start notepad.exe"
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Import ConfigLoader
        from config_loader import ConfigLoader

        # This should NOT raise an exception
        config = ConfigLoader.load_config(self.config_file)
        self.assertIsNotNone(config)
        self.assertNotIn("no_focus", config["files"][0])

    def test_no_focus_with_cmd_c_start_should_succeed(self):
        """Test that no_focus=true with 'cmd /c start' succeeds (start is not at beginning)."""
        # Create config with no_focus=true and command with "cmd /c start"
        config_content = """
default_interval = "1s"

[[files]]
path = "test.txt"
command = "cmd /c start notepad.exe"
no_focus = true
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Import ConfigLoader
        from config_loader import ConfigLoader

        # This should NOT raise an exception because "start" is not at the beginning
        config = ConfigLoader.load_config(self.config_file)
        self.assertIsNotNone(config)

    def test_no_focus_with_restart_command_should_succeed(self):
        """Test that no_focus=true with command containing 'restart' (not 'start ') succeeds."""
        # Create config with no_focus=true and command containing "restart"
        config_content = """
default_interval = "1s"

[[files]]
path = "test.txt"
command = "systemctl restart myservice"
no_focus = true
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Import ConfigLoader
        from config_loader import ConfigLoader

        # This should NOT raise an exception
        config = ConfigLoader.load_config(self.config_file)
        self.assertIsNotNone(config)
        self.assertTrue(config["files"][0]["no_focus"])

    def test_no_focus_with_start_at_end_should_succeed(self):
        """Test that no_focus=true with 'start' not at beginning succeeds."""
        # Create config with no_focus=true and command with "start" in the middle
        config_content = """
default_interval = "1s"

[[files]]
path = "test.txt"
command = "python --start-server"
no_focus = true
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Import ConfigLoader
        from config_loader import ConfigLoader

        # This should NOT raise an exception
        config = ConfigLoader.load_config(self.config_file)
        self.assertIsNotNone(config)
        self.assertTrue(config["files"][0]["no_focus"])

    def test_no_focus_with_start_only_should_error(self):
        """Test that no_focus=true with just 'start' command raises error."""
        # Create config with no_focus=true and command as just "start"
        config_content = """
default_interval = "1s"

[[files]]
path = "test.txt"
command = "start"
no_focus = true
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Import ConfigLoader
        from config_loader import ConfigLoader

        # This should raise SystemExit
        with self.assertRaises(SystemExit):
            ConfigLoader.load_config(self.config_file)


if __name__ == "__main__":
    unittest.main()

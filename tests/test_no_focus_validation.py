#!/usr/bin/env python3
"""
Tests for no_focus command validation
"""

import os
import sys
import tempfile
import unittest

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from config_loader import ConfigLoader


class TestNoFocusValidation(unittest.TestCase):
    """Test cases for no_focus command validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, "config.toml")

    def tearDown(self):
        """Clean up test files."""
        import shutil

        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_no_focus_with_command_should_error(self):
        """Test that no_focus=true with 'command' field raises error."""
        # Create config with no_focus=true and command field
        config_content = """
default_interval = "1s"

[[files]]
path = "test.txt"
command = "notepad.exe test.txt"
no_focus = true
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # This should raise SystemExit because command is not allowed with no_focus
        with self.assertRaises(SystemExit):
            ConfigLoader.load_config(self.config_file)

    def test_no_focus_without_argv_should_error(self):
        """Test that no_focus=true without 'argv' field raises error."""
        # Create config with no_focus=true but no argv field
        config_content = """
default_interval = "1s"

[[files]]
path = "test.txt"
no_focus = true
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # This should raise SystemExit because argv is required with no_focus
        with self.assertRaises(SystemExit):
            ConfigLoader.load_config(self.config_file)

    def test_no_focus_with_empty_argv_should_error(self):
        """Test that no_focus=true with empty argv array raises error."""
        # Create config with no_focus=true and empty argv
        config_content = """
default_interval = "1s"

[[files]]
path = "test.txt"
argv = []
no_focus = true
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # This should raise SystemExit because argv cannot be empty
        with self.assertRaises(SystemExit):
            ConfigLoader.load_config(self.config_file)

    def test_no_focus_with_non_array_argv_should_error(self):
        """Test that no_focus=true with argv as string raises error."""
        # Create config with no_focus=true and argv as string instead of array
        config_content = """
default_interval = "1s"

[[files]]
path = "test.txt"
argv = "notepad.exe test.txt"
no_focus = true
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # This should raise SystemExit because argv must be an array
        with self.assertRaises(SystemExit):
            ConfigLoader.load_config(self.config_file)

    def test_no_focus_with_valid_argv_should_succeed(self):
        """Test that no_focus=true with valid argv array succeeds."""
        # Create config with no_focus=true and valid argv array
        config_content = """
default_interval = "1s"

[[files]]
path = "test.txt"
argv = ["notepad.exe", "test.txt"]
no_focus = true
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # This should NOT raise an exception
        config = ConfigLoader.load_config(self.config_file)
        self.assertIsNotNone(config)
        self.assertTrue(config["files"][0]["no_focus"])
        self.assertEqual(config["files"][0]["argv"], ["notepad.exe", "test.txt"])

    def test_no_focus_with_single_element_argv_should_succeed(self):
        """Test that no_focus=true with single element argv array succeeds."""
        # Create config with no_focus=true and single element argv
        config_content = """
default_interval = "1s"

[[files]]
path = "test.txt"
argv = ["notepad.exe"]
no_focus = true
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # This should NOT raise an exception
        config = ConfigLoader.load_config(self.config_file)
        self.assertIsNotNone(config)
        self.assertTrue(config["files"][0]["no_focus"])
        self.assertEqual(config["files"][0]["argv"], ["notepad.exe"])

    def test_no_focus_false_with_command_should_succeed(self):
        """Test that no_focus=false with 'command' field succeeds."""
        # Create config with no_focus=false and command field
        config_content = """
default_interval = "1s"

[[files]]
path = "test.txt"
command = "start notepad.exe"
no_focus = false
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # This should NOT raise an exception
        config = ConfigLoader.load_config(self.config_file)
        self.assertIsNotNone(config)
        self.assertFalse(config["files"][0]["no_focus"])

    def test_no_focus_not_specified_with_command_should_succeed(self):
        """Test that no_focus not specified (defaults to false) with 'command' field succeeds."""
        # Create config without no_focus and command field
        config_content = """
default_interval = "1s"

[[files]]
path = "test.txt"
command = "start notepad.exe"
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # This should NOT raise an exception
        config = ConfigLoader.load_config(self.config_file)
        self.assertIsNotNone(config)
        self.assertNotIn("no_focus", config["files"][0])

    def test_no_focus_with_argv_containing_special_chars_should_succeed(self):
        """Test that no_focus=true with argv containing special characters succeeds."""
        # Create config with no_focus=true and argv with spaces and special chars
        config_content = """
default_interval = "1s"

[[files]]
path = "test.txt"
argv = ["python", "-c", "print('hello world')"]
no_focus = true
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # This should NOT raise an exception
        config = ConfigLoader.load_config(self.config_file)
        self.assertIsNotNone(config)
        self.assertTrue(config["files"][0]["no_focus"])
        self.assertEqual(config["files"][0]["argv"], ["python", "-c", "print('hello world')"])


if __name__ == "__main__":
    unittest.main()

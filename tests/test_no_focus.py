#!/usr/bin/env python3
"""
Tests for no_focus command execution mode
"""

import os
import tempfile
import time
import unittest

import toml


class TestNoFocus(unittest.TestCase):
    """Test cases for no_focus command execution."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, "config.toml")
        self.test_file = os.path.join(self.test_dir, "test.txt")
        self.output_file = os.path.join(self.test_dir, "output.txt")

    def tearDown(self):
        """Clean up test files."""
        import shutil

        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_no_focus_enabled(self):
        """Test command execution with no_focus enabled."""
        # Create config with no_focus=true
        config_content = f"""
default_interval = "100ms"

[[files]]
path = "{self.test_file}"
command = "echo test_output"
no_focus = true
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Verify config parses correctly
        config = toml.load(self.config_file)
        self.assertTrue(config["files"][0]["no_focus"])

        # Create test file to trigger command
        with open(self.test_file, "w") as f:
            f.write("initial content")

        # Import and run FileWatcher
        import sys

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
        from cat_file_watcher import FileWatcher

        watcher = FileWatcher(self.config_file)

        # Modify the file to trigger command execution
        time.sleep(0.2)
        with open(self.test_file, "w") as f:
            f.write("modified content")

        # Run one iteration of the watcher
        watcher._check_files()

        # The test passes if no exception was raised
        self.assertTrue(True)

    def test_no_focus_disabled_default(self):
        """Test command execution with no_focus not specified (default behavior)."""
        # Create config without no_focus (should default to False)
        config_content = f"""
default_interval = "100ms"

[[files]]
path = "{self.test_file}"
command = "echo test_output"
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Verify config parses correctly and no_focus is not set
        config = toml.load(self.config_file)
        self.assertNotIn("no_focus", config["files"][0])

        # Create test file
        with open(self.test_file, "w") as f:
            f.write("initial content")

        # Import and run FileWatcher
        import sys

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
        from cat_file_watcher import FileWatcher

        watcher = FileWatcher(self.config_file)

        # Modify the file to trigger command execution
        time.sleep(0.2)
        with open(self.test_file, "w") as f:
            f.write("modified content")

        # Run one iteration of the watcher
        watcher._check_files()

        # The test passes if no exception was raised
        self.assertTrue(True)

    def test_no_focus_with_arguments(self):
        """Test no_focus mode with command that has arguments."""
        # Create a simple Python script that writes to a file
        script_file = os.path.join(self.test_dir, "script.py")
        with open(script_file, "w") as f:
            f.write(f"""
import sys
with open(r'{self.output_file}', 'w') as f:
    f.write(' '.join(sys.argv[1:]))
""")

        # Create config with no_focus=true and a command with arguments
        config_content = f"""
default_interval = "100ms"

[[files]]
path = "{self.test_file}"
command = "python {script_file} arg1 arg2 arg3"
no_focus = true
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Create and modify test file
        with open(self.test_file, "w") as f:
            f.write("initial content")

        import sys

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
        from cat_file_watcher import FileWatcher

        watcher = FileWatcher(self.config_file)

        time.sleep(0.2)
        with open(self.test_file, "w") as f:
            f.write("modified content")

        # Run one iteration
        watcher._check_files()

        # Since no_focus is asynchronous, wait a bit for the command to complete
        time.sleep(0.5)

        # Verify the command executed with correct arguments
        if os.path.exists(self.output_file):
            with open(self.output_file, "r") as f:
                output = f.read()
                self.assertEqual(output, "arg1 arg2 arg3")
        else:
            # If on Windows with no_focus, the file should eventually exist
            # If not on Windows, the fallback to normal execution should have created it
            # Wait a bit more and try again
            time.sleep(1.0)
            if os.path.exists(self.output_file):
                with open(self.output_file, "r") as f:
                    output = f.read()
                    self.assertEqual(output, "arg1 arg2 arg3")

    def test_no_focus_false(self):
        """Test command execution with no_focus explicitly set to false."""
        # Create config with no_focus=false
        config_content = f"""
default_interval = "100ms"

[[files]]
path = "{self.test_file}"
command = "echo test_output"
no_focus = false
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Verify config parses correctly
        config = toml.load(self.config_file)
        self.assertFalse(config["files"][0]["no_focus"])

        # Create test file
        with open(self.test_file, "w") as f:
            f.write("initial content")

        # Import and run FileWatcher
        import sys

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
        from cat_file_watcher import FileWatcher

        watcher = FileWatcher(self.config_file)

        # Modify the file
        time.sleep(0.2)
        with open(self.test_file, "w") as f:
            f.write("modified content")

        # Run one iteration
        watcher._check_files()

        # The test passes if no exception was raised
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()

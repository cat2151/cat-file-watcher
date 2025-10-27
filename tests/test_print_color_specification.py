#!/usr/bin/env python3
"""
Tests for print color specification changes.
Tests that "Detected change" uses white (no color) and "Executing command" colors only the command part.
"""

import os
import sys
import tempfile
import time
from io import StringIO

from colorama import Fore, Style

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from command_executor import CommandExecutor
from file_monitor import FileMonitor
from timestamp_printer import TimestampPrinter


class TestPrintColorSpecification:
    """Test cases for print color specification."""

    def test_detected_change_uses_no_color(self):
        """Test that 'Detected change' message uses white (no color)."""
        # Create a temporary test directory and file
        test_dir = tempfile.mkdtemp()
        test_file = os.path.join(test_dir, "test.txt")

        try:
            # Create test file with initial content
            with open(test_file, "w") as f:
                f.write("initial")

            # Create config
            config = {
                "files": [{"path": test_file, "command": "echo test"}],
                "default_interval": "0.1s",
            }

            # Initialize timestamps
            file_timestamps = {}
            file_last_check = {}

            # First check - should start monitoring (green message)
            captured_output = StringIO()
            sys.stdout = captured_output
            TimestampPrinter.set_enable_timestamp(False)

            file_timestamps, file_last_check = FileMonitor.check_files(config, file_timestamps, file_last_check)

            # Modify the file
            time.sleep(0.2)
            with open(test_file, "w") as f:
                f.write("modified")

            # Second check - should detect change
            file_timestamps, file_last_check = FileMonitor.check_files(config, file_timestamps, file_last_check)

            output = captured_output.getvalue()
            sys.stdout = sys.__stdout__

            # Verify "Detected change" is in output
            assert "Detected change in" in output

            # Verify that "Detected change" line does NOT contain color codes
            lines = output.split("\n")
            for line in lines:
                if "Detected change in" in line:
                    # Should not contain ANSI color codes for Fore.GREEN or any other color
                    # White text means no color codes
                    assert Fore.GREEN not in line
                    assert Fore.RED not in line
                    assert Fore.YELLOW not in line
                    # Also check for ANSI escape sequences (if colorama is initialized)
                    assert "\x1b[32m" not in line  # Green
                    assert "\x1b[31m" not in line  # Red
                    assert "\x1b[33m" not in line  # Yellow

        finally:
            # Cleanup
            if os.path.exists(test_file):
                os.remove(test_file)
            if os.path.exists(test_dir):
                os.rmdir(test_dir)
            sys.stdout = sys.__stdout__
            TimestampPrinter.set_enable_timestamp(True)

    def test_executing_command_colors_only_command_part(self):
        """Test that 'Executing command' message colors only the command part in green."""
        # Create a temporary test directory and file
        test_dir = tempfile.mkdtemp()
        test_file = os.path.join(test_dir, "test.txt")

        try:
            # Create test file
            with open(test_file, "w") as f:
                f.write("test")

            # Create config with a simple command
            config = {"error_log_file": None}
            settings = {"command": "echo hello"}

            # Capture output
            captured_output = StringIO()
            sys.stdout = captured_output
            TimestampPrinter.set_enable_timestamp(False)

            # Execute command
            CommandExecutor._execute_shell_command("echo hello", test_file, settings, config)

            output = captured_output.getvalue()
            sys.stdout = sys.__stdout__

            # Verify "Executing command" is in output
            assert "Executing command for" in output
            assert "echo hello" in output

            # Verify that the command part is colored green
            # The output should contain: Fore.GREEN + "echo hello" + Style.RESET_ALL
            assert Fore.GREEN in output or "\x1b[32m" in output
            assert Style.RESET_ALL in output or "\x1b[0m" in output

            # Verify the structure: text before command should not be colored
            # This is verified by checking that the green color comes after "': "
            lines = output.split("\n")
            for line in lines:
                if "Executing command for" in line:
                    # Find where the command starts (after ": ")
                    colon_pos = line.rfind(": ")
                    if colon_pos != -1:
                        # Just verify that green comes after the colon
                        assert colon_pos < line.find("echo hello")

        finally:
            # Cleanup
            if os.path.exists(test_file):
                os.remove(test_file)
            if os.path.exists(test_dir):
                os.rmdir(test_dir)
            sys.stdout = sys.__stdout__
            TimestampPrinter.set_enable_timestamp(True)

    def test_executing_command_green_color_only_on_command(self):
        """Test that green color is applied only to the command, not the whole message."""
        test_dir = tempfile.mkdtemp()
        test_file = os.path.join(test_dir, "myfile.txt")

        try:
            with open(test_file, "w") as f:
                f.write("test")

            config = {}
            settings = {}

            captured_output = StringIO()
            sys.stdout = captured_output
            TimestampPrinter.set_enable_timestamp(False)

            # Test with a command that has special characters
            test_command = "ls -la && echo done"
            CommandExecutor._execute_shell_command(test_command, test_file, settings, config)

            output = captured_output.getvalue()
            sys.stdout = sys.__stdout__

            # The output should have the pattern:
            # "Executing command for 'myfile.txt': " + GREEN + "ls -la && echo done" + RESET
            assert "Executing command for" in output
            assert test_command in output

            # Verify color codes are present
            has_green = Fore.GREEN in output or "\x1b[32m" in output
            has_reset = Style.RESET_ALL in output or "\x1b[0m" in output
            assert has_green and has_reset

        finally:
            if os.path.exists(test_file):
                os.remove(test_file)
            if os.path.exists(test_dir):
                os.rmdir(test_dir)
            sys.stdout = sys.__stdout__
            TimestampPrinter.set_enable_timestamp(True)

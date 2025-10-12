#!/usr/bin/env python3
"""
Tests for timestamp printing functionality
"""

import os
import re
import shutil
import sys
import tempfile
import time
from io import StringIO

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from cat_file_watcher import FileWatcher
from timestamp_printer import TimestampPrinter


class TestTimestampPrinter:
    """Test cases for timestamp printer."""

    def test_timestamp_enabled_by_default(self):
        """Test that timestamps are enabled by default."""
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            # Reset to default
            TimestampPrinter.set_enable_timestamp(True)
            TimestampPrinter.print("Test message")

            output = captured_output.getvalue()
            # Should contain timestamp pattern [YYYY-MM-DD HH:MM:SS]
            assert re.search(r'\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]', output)
            assert "Test message" in output
        finally:
            sys.stdout = sys.__stdout__

    def test_timestamp_can_be_disabled(self):
        """Test that timestamps can be disabled."""
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            TimestampPrinter.set_enable_timestamp(False)
            TimestampPrinter.print("Test message without timestamp")

            output = captured_output.getvalue()
            # Should not contain timestamp pattern
            assert not re.search(r'\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]', output)
            assert "Test message without timestamp" in output
        finally:
            sys.stdout = sys.__stdout__
            # Reset to default
            TimestampPrinter.set_enable_timestamp(True)

    def test_timestamp_format(self):
        """Test that timestamp format is correct."""
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            TimestampPrinter.set_enable_timestamp(True)
            TimestampPrinter.print("Message")

            output = captured_output.getvalue()
            # Extract timestamp
            match = re.search(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]', output)
            assert match is not None

            # Verify timestamp can be parsed
            timestamp_str = match.group(1)
            from datetime import datetime
            parsed = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            assert parsed is not None
        finally:
            sys.stdout = sys.__stdout__


class TestTimestampConfig:
    """Test cases for timestamp configuration in FileWatcher."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, "config.toml")
        self.test_file = os.path.join(self.test_dir, "test.txt")

        # Create a test file
        with open(self.test_file, "w") as f:
            f.write("Initial content\n")

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)
        # Reset to default
        TimestampPrinter.set_enable_timestamp(True)

    def test_timestamp_enabled_by_default_in_config(self):
        """Test that timestamps are enabled by default when not specified in config."""
        # Create config without enable_timestamp setting
        config_content = f'''default_interval = "0.05s"

"{self.test_file}" = {{ command = "echo 'test'" }}
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            watcher = FileWatcher(self.config_file)
            watcher._check_files()

            output = captured_output.getvalue()
            # Should contain timestamp in "Started monitoring" message
            assert re.search(r'\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]', output)
        finally:
            sys.stdout = sys.__stdout__

    def test_timestamp_can_be_enabled_in_config(self):
        """Test that timestamps can be explicitly enabled in config."""
        # Create config with enable_timestamp = true
        config_content = f'''default_interval = "0.05s"
enable_timestamp = true

"{self.test_file}" = {{ command = "echo 'test'" }}
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            watcher = FileWatcher(self.config_file)
            watcher._check_files()

            output = captured_output.getvalue()
            # Should contain timestamp
            assert re.search(r'\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]', output)
        finally:
            sys.stdout = sys.__stdout__

    def test_timestamp_can_be_disabled_in_config(self):
        """Test that timestamps can be disabled in config."""
        # Create config with enable_timestamp = false
        config_content = f'''default_interval = "0.05s"
enable_timestamp = false

"{self.test_file}" = {{ command = "echo 'test'" }}
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            watcher = FileWatcher(self.config_file)
            watcher._check_files()

            output = captured_output.getvalue()
            # Should not contain timestamp pattern
            assert not re.search(r'\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]', output)
            assert "Started monitoring" in output
        finally:
            sys.stdout = sys.__stdout__

    def test_timestamp_in_various_messages(self):
        """Test that timestamps appear in various message types."""
        # Create config with timestamps enabled
        config_content = f'''default_interval = "0.05s"
enable_timestamp = true

"{self.test_file}" = {{ command = "echo 'test'" }}
'''
        with open(self.config_file, "w") as f:
            f.write(config_content)

        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            watcher = FileWatcher(self.config_file)

            # Check files (should show "Started monitoring")
            watcher._check_files()

            # Modify file to trigger change detection
            time.sleep(0.1)
            with open(self.test_file, "a") as f:
                f.write("Modified content\n")
            time.sleep(0.1)

            # Check files again (should show "Detected change")
            watcher._check_files()

            output = captured_output.getvalue()

            # Count timestamp patterns
            timestamp_count = len(re.findall(r'\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]', output))

            # Should have at least 3 timestamps:
            # 1. "Started monitoring"
            # 2. "Detected change"
            # 3. "Executing command"
            assert timestamp_count >= 3
        finally:
            sys.stdout = sys.__stdout__

#!/usr/bin/env python3
"""
Tests for issue #107: Terminating message should be green (info) not yellow (warning)

Verify that:
1. "Terminating process" message is displayed in green (Fore.GREEN)
2. This is an informational message, not a warning
"""

import os
import subprocess
import sys
import tempfile
import time
from io import StringIO

from colorama import Fore

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from cat_file_watcher import FileWatcher


class TestTerminateMessageColor:
    """Test cases for terminating message color."""

    def test_terminating_message_uses_green_color(self):
        """Test that 'Terminating process' message uses green color (info) not yellow (warning)."""
        test_dir = tempfile.mkdtemp()
        config_file = os.path.join(test_dir, "test_config.toml")
        error_log_file = os.path.join(test_dir, "error.log")

        # Start a test process
        test_script = os.path.join(test_dir, "test_process.py")
        with open(test_script, "w") as f:
            f.write("import time\nwhile True:\n    time.sleep(0.1)\n")

        proc = subprocess.Popen([sys.executable, test_script])
        time.sleep(0.2)  # Give it time to start

        try:
            # Verify process is running
            assert proc.poll() is None, "Test process should be running"

            # Create config with terminate_if_process
            config_content = f"""default_interval = "0.05s"
error_log_file = "{error_log_file}"

[[files]]
path = ""
terminate_if_process = "test_process\\\\.py"
"""
            with open(config_file, "w") as f:
                f.write(config_content)

            # Capture stdout to check color codes
            captured_output = StringIO()
            old_stdout = sys.stdout
            sys.stdout = captured_output

            try:
                watcher = FileWatcher(config_file)
                watcher._check_files()

                output = captured_output.getvalue()

                # Check that the "Terminating process" message contains green color code
                # The message should contain "Terminating process" and green color
                assert "Terminating process" in output, "Should print 'Terminating process' message"

                # For the "Terminating process" line specifically, verify it's green
                lines = output.split("\n")
                terminating_line = None
                for line in lines:
                    if "Terminating process" in line:
                        terminating_line = line
                        break

                assert terminating_line is not None, "Should have a line with 'Terminating process'"

                # The terminating line should have green, not yellow
                assert Fore.GREEN in terminating_line or "\x1b[32m" in terminating_line, (
                    "Terminating message should use green color (info)"
                )
                assert Fore.YELLOW not in terminating_line and "\x1b[33m" not in terminating_line, (
                    "Terminating message should NOT use yellow color (warning)"
                )

            finally:
                sys.stdout = old_stdout

            # Wait for termination to complete
            time.sleep(0.5)

            # Verify process was terminated
            assert proc.poll() is not None, "Process should have been terminated"

        finally:
            # Cleanup: ensure process is killed if still running
            if proc.poll() is None:
                proc.kill()
                proc.wait()

            # Clean up test directory
            import shutil

            shutil.rmtree(test_dir, ignore_errors=True)

#!/usr/bin/env python3
"""
Tests for issue #105: Error log clarity for process termination

Verify that:
1. Successful terminations are NOT logged to error log
2. Failed terminations ARE logged to error log
3. Warnings about multiple processes ARE logged to error log
"""

import os
import shutil
import subprocess
import sys
import tempfile
import time

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from cat_file_watcher import FileWatcher


class TestErrorLogClarity:
    """Test cases for error log clarity in process termination."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, "test_config.toml")
        self.error_log_file = os.path.join(self.test_dir, "error.log")

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_successful_termination_not_logged_to_error_log(self):
        """Test that successful process terminations are NOT logged to error log.

        This addresses issue #105: When a process is successfully terminated,
        we should not log it as an ERROR. Only actual errors should be logged.
        """
        # Start a test process
        test_script = os.path.join(self.test_dir, "test_process.py")
        with open(test_script, "w") as f:
            f.write("import time\nwhile True:\n    time.sleep(0.1)\n")

        proc = subprocess.Popen([sys.executable, test_script])
        time.sleep(0.2)  # Give it time to start

        try:
            # Verify process is running
            assert proc.poll() is None, "Test process should be running"

            # Create config with terminate_if_process
            config_content = f"""default_interval = "0.05s"
error_log_file = "{self.error_log_file}"

[[files]]
path = ""
terminate_if_process = "test_process\\\\.py"
"""
            with open(self.config_file, "w") as f:
                f.write(config_content)

            watcher = FileWatcher(self.config_file)

            # Execute check - should terminate the process
            watcher._check_files()

            # Wait for termination to complete
            time.sleep(0.5)

            # Verify process was terminated
            assert proc.poll() is not None, "Process should have been terminated"

            # Verify that NO error log was created (successful termination)
            # This is the key fix for issue #105
            if os.path.exists(self.error_log_file):
                with open(self.error_log_file, "r") as f:
                    log_content = f.read()
                # Error log should not contain success messages
                assert "Successfully sent terminate signal" not in log_content, (
                    "Success messages should NOT be in error log"
                )
                assert "Terminating process" not in log_content, "Informational messages should NOT be in error log"
        finally:
            # Cleanup: ensure process is killed if still running
            if proc.poll() is None:
                proc.kill()
                proc.wait()

    def test_multiple_process_warning_is_logged_to_error_log(self):
        """Test that warnings about multiple matching processes ARE logged to error log.

        When multiple processes match and we refuse to terminate (safety check),
        this IS an error condition that should be logged.
        """
        # Start multiple test processes
        test_script = os.path.join(self.test_dir, "test_multi.py")
        with open(test_script, "w") as f:
            f.write("import time\nwhile True:\n    time.sleep(0.1)\n")

        proc1 = subprocess.Popen([sys.executable, test_script])
        proc2 = subprocess.Popen([sys.executable, test_script])
        time.sleep(0.2)

        try:
            # Create config with terminate_if_process
            config_content = f"""default_interval = "0.05s"
error_log_file = "{self.error_log_file}"

[[files]]
path = ""
terminate_if_process = "test_multi\\\\.py"
"""
            with open(self.config_file, "w") as f:
                f.write(config_content)

            watcher = FileWatcher(self.config_file)

            # Execute check - should warn but not terminate
            watcher._check_files()

            time.sleep(0.5)

            # Verify both processes are still running (safety check worked)
            assert proc1.poll() is None, "First process should still be running"
            assert proc2.poll() is None, "Second process should still be running"

            # Verify warning WAS logged to error log
            # This is correct behavior - warnings about safety issues should be logged
            assert os.path.exists(self.error_log_file), "Error log should exist for warnings"
            with open(self.error_log_file, "r") as f:
                log_content = f.read()
            assert "ERROR: Warning: Found 2 processes" in log_content, "Warning should be in error log"
            assert "test_multi" in log_content, "Process name should be in error log"
        finally:
            # Cleanup
            for proc in [proc1, proc2]:
                if proc.poll() is None:
                    proc.kill()
                    proc.wait()

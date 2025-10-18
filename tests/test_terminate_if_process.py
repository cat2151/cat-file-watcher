#!/usr/bin/env python3
"""
Test cases for terminate_if_process functionality
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
from process_detector import ProcessDetector


class TestTerminateIfProcess:
    """Test cases for terminate_if_process functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, "test_config.toml")
        self.error_log_file = os.path.join(self.test_dir, "error.log")

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_terminate_single_process(self):
        """Test that a single matching process is terminated."""
        # Start a long-running test process
        test_script = os.path.join(self.test_dir, "test_process.py")
        with open(test_script, "w") as f:
            f.write("import time\nwhile True:\n    time.sleep(0.1)\n")

        # Start the process
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

            # Wait a bit for termination to complete
            time.sleep(0.5)

            # Verify process was terminated
            assert proc.poll() is not None, "Process should have been terminated"
        finally:
            # Cleanup: ensure process is killed if still running
            if proc.poll() is None:
                proc.kill()
                proc.wait()

    def test_terminate_no_matching_process(self):
        """Test that no action is taken when no process matches."""
        # Create config with terminate_if_process for non-existent process
        config_content = f"""default_interval = "0.05s"
error_log_file = "{self.error_log_file}"

[[files]]
path = ""
terminate_if_process = "nonexistent_process_xyz123"
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # Execute check - should do nothing (no error)
        watcher._check_files()

        # No assertion needed - just verify it doesn't crash

    def test_terminate_multiple_processes_with_single_pattern(self):
        """Test that warning is issued and no termination occurs when multiple processes match a single pattern."""
        # Start multiple test processes
        test_script = os.path.join(self.test_dir, "test_multi.py")
        with open(test_script, "w") as f:
            f.write("import time\nwhile True:\n    time.sleep(0.1)\n")

        # Start two processes
        proc1 = subprocess.Popen([sys.executable, test_script])
        proc2 = subprocess.Popen([sys.executable, test_script])
        time.sleep(0.2)  # Give them time to start

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

            # Execute check - should issue warning but not terminate
            watcher._check_files()

            # Wait a bit
            time.sleep(0.5)

            # Verify both processes are still running (safety check worked)
            assert proc1.poll() is None, "First process should still be running (not terminated)"
            assert proc2.poll() is None, "Second process should still be running (not terminated)"

            # Verify warning was logged
            assert os.path.exists(self.error_log_file), "Error log should exist"
            with open(self.error_log_file, "r") as f:
                log_content = f.read()
            assert "Found 2 processes" in log_content, "Warning about multiple processes should be logged"
        finally:
            # Cleanup: ensure processes are killed
            for proc in [proc1, proc2]:
                if proc.poll() is None:
                    proc.kill()
                    proc.wait()

    def test_terminate_with_filename_error(self):
        """Test that error is raised when terminate_if_process is used with non-empty filename."""
        test_file = os.path.join(self.test_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("test content\n")

        # Create config with terminate_if_process on non-empty filename
        config_content = f"""default_interval = "0.05s"
error_log_file = "{self.error_log_file}"

[[files]]
path = "{test_file}"
terminate_if_process = "python"

"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # Execute check - should log fatal error and continue
        watcher._check_files()

        # Verify error was logged
        assert os.path.exists(self.error_log_file), "Error log should exist"
        with open(self.error_log_file, "r") as f:
            log_content = f.read()
        assert "Fatal configuration error" in log_content, "Fatal error should be logged"
        assert "empty filename" in log_content, "Error should mention empty filename requirement"

    def test_terminate_with_command_error(self):
        """Test that error is raised when terminate_if_process is used with command field."""
        # Create config with both terminate_if_process and command
        config_content = f"""default_interval = "0.05s"
error_log_file = "{self.error_log_file}"

[[files]]
path = ""
command = "echo 'test'"
terminate_if_process = "python"
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # Execute check - should log fatal error and continue
        watcher._check_files()

        # Verify error was logged
        assert os.path.exists(self.error_log_file), "Error log should exist"
        with open(self.error_log_file, "r") as f:
            log_content = f.read()
        assert "Fatal configuration error" in log_content, "Fatal error should be logged"
        assert "command must be empty" in log_content, "Error should mention command must be empty"

    def test_terminate_respects_interval(self):
        """Test that terminate_if_process respects interval timing."""
        # Start a test process
        test_script = os.path.join(self.test_dir, "test_interval.py")
        with open(test_script, "w") as f:
            f.write("import time\nwhile True:\n    time.sleep(0.1)\n")

        proc = subprocess.Popen([sys.executable, test_script])
        time.sleep(0.2)

        try:
            # Create config with custom interval
            config_content = f"""default_interval = "10s"
error_log_file = "{self.error_log_file}"

[[files]]
path = ""
terminate_if_process = "test_interval\\\\.py"
interval = "10s"
"""
            with open(self.config_file, "w") as f:
                f.write(config_content)

            watcher = FileWatcher(self.config_file)

            # First check - should terminate
            watcher._check_files()
            time.sleep(0.3)

            # Verify process was terminated
            assert proc.poll() is not None, "Process should be terminated after first check"

            # Start another process
            proc2 = subprocess.Popen([sys.executable, test_script])
            time.sleep(0.2)

            # Second check immediately - should NOT check yet (interval not met)
            watcher._check_files()
            time.sleep(0.1)

            # Process should still be running (interval not met - we set it to 10s)
            assert proc2.poll() is None, "Process should still be running (interval not met)"

            # Cleanup the second process
            if proc2.poll() is None:
                proc2.kill()
                proc2.wait()
        finally:
            # Cleanup
            if proc.poll() is None:
                proc.kill()
                proc.wait()
            if "proc2" in locals() and proc2.poll() is None:
                proc2.kill()
                proc2.wait()

    def test_terminate_multiple_process_patterns_array(self):
        """Test that terminate_if_process can accept an array of patterns, with safety check per pattern."""
        # Start multiple different test processes
        test_script1 = os.path.join(self.test_dir, "test_proc_a.py")
        with open(test_script1, "w") as f:
            f.write("import time\nwhile True:\n    time.sleep(0.1)\n")

        test_script2 = os.path.join(self.test_dir, "test_proc_b.py")
        with open(test_script2, "w") as f:
            f.write("import time\nwhile True:\n    time.sleep(0.1)\n")

        # Start both processes
        proc1 = subprocess.Popen([sys.executable, test_script1])
        proc2 = subprocess.Popen([sys.executable, test_script2])
        time.sleep(0.2)  # Give them time to start

        try:
            # Verify both processes are running
            assert proc1.poll() is None, "First test process should be running"
            assert proc2.poll() is None, "Second test process should be running"

            # Create config with array of terminate_if_process patterns
            config_content = f"""default_interval = "0.05s"
error_log_file = "{self.error_log_file}"

[[files]]
path = ""
terminate_if_process = ["test_proc_a\\\\.py", "test_proc_b\\\\.py"]
"""
            with open(self.config_file, "w") as f:
                f.write(config_content)

            watcher = FileWatcher(self.config_file)

            # Execute check - should terminate both processes (each pattern matches exactly 1)
            watcher._check_files()

            # Wait a bit for termination to complete
            time.sleep(0.5)

            # Verify both processes were terminated
            assert proc1.poll() is not None, "First process should have been terminated"
            assert proc2.poll() is not None, "Second process should have been terminated"

            # Successful terminations should not be logged to error log
            # Error log should not exist for successful operations
            if os.path.exists(self.error_log_file):
                with open(self.error_log_file, "r") as f:
                    log_content = f.read()
                # If the file exists, it should only contain actual errors, not success messages
                assert "Successfully sent terminate signal" not in log_content, (
                    "Success messages should not be in error log"
                )
        finally:
            # Cleanup: ensure processes are killed if still running
            for proc in [proc1, proc2]:
                if proc.poll() is None:
                    proc.kill()
                    proc.wait()

    def test_terminate_multiple_instances_same_pattern_in_array(self):
        """Test that when a pattern in an array matches multiple processes, safety check prevents termination."""
        # Start multiple instances of the same script
        test_script = os.path.join(self.test_dir, "test_multi_same.py")
        with open(test_script, "w") as f:
            f.write("import time\nwhile True:\n    time.sleep(0.1)\n")

        # Start three processes with the same script
        proc1 = subprocess.Popen([sys.executable, test_script])
        proc2 = subprocess.Popen([sys.executable, test_script])
        proc3 = subprocess.Popen([sys.executable, test_script])
        time.sleep(0.2)

        try:
            # Verify all processes are running
            assert proc1.poll() is None, "First process should be running"
            assert proc2.poll() is None, "Second process should be running"
            assert proc3.poll() is None, "Third process should be running"

            # Create config with array containing pattern that matches all three
            config_content = f"""default_interval = "0.05s"
error_log_file = "{self.error_log_file}"

[[files]]
path = ""
terminate_if_process = ["test_multi_same\\\\.py"]
"""
            with open(self.config_file, "w") as f:
                f.write(config_content)

            watcher = FileWatcher(self.config_file)

            # Execute check - should warn but NOT terminate (safety check)
            watcher._check_files()

            # Wait a bit
            time.sleep(0.5)

            # Verify all processes are still running (safety check prevented termination)
            assert proc1.poll() is None, "First process should still be running (not terminated)"
            assert proc2.poll() is None, "Second process should still be running (not terminated)"
            assert proc3.poll() is None, "Third process should still be running (not terminated)"

            # Verify warning was logged
            assert os.path.exists(self.error_log_file), "Error log should exist"
            with open(self.error_log_file, "r") as f:
                log_content = f.read()
            assert "Found 3 processes" in log_content, "Warning about multiple processes should be logged"
        finally:
            # Cleanup
            for proc in [proc1, proc2, proc3]:
                if proc.poll() is None:
                    proc.kill()
                    proc.wait()

    def test_terminate_array_with_no_matches(self):
        """Test that array of patterns with no matches doesn't cause errors."""
        config_content = f"""default_interval = "0.05s"
error_log_file = "{self.error_log_file}"

[[files]]
path = ""
terminate_if_process = ["nonexistent_abc", "nonexistent_xyz"]
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)

        watcher = FileWatcher(self.config_file)

        # Execute check - should do nothing (no error)
        watcher._check_files()

        # No assertion needed - just verify it doesn't crash

    def test_terminate_array_with_partial_matches(self):
        """Test that array of patterns terminates only matching processes."""
        # Start only one of two expected processes
        test_script = os.path.join(self.test_dir, "test_partial.py")
        with open(test_script, "w") as f:
            f.write("import time\nwhile True:\n    time.sleep(0.1)\n")

        proc = subprocess.Popen([sys.executable, test_script])
        time.sleep(0.2)

        try:
            # Verify process is running
            assert proc.poll() is None, "Test process should be running"

            # Create config with array where only one pattern matches
            config_content = f"""default_interval = "0.05s"
error_log_file = "{self.error_log_file}"

[[files]]
path = ""
terminate_if_process = ["test_partial\\\\.py", "nonexistent_xyz"]
"""
            with open(self.config_file, "w") as f:
                f.write(config_content)

            watcher = FileWatcher(self.config_file)

            # Execute check - should terminate only the matching process
            watcher._check_files()

            # Wait a bit for termination to complete
            time.sleep(0.5)

            # Verify process was terminated
            assert proc.poll() is not None, "Process should have been terminated"

            # Successful terminations should not be logged to error log
            # Error log should not exist for successful operations
            if os.path.exists(self.error_log_file):
                with open(self.error_log_file, "r") as f:
                    log_content = f.read()
                # If the file exists, it should only contain actual errors, not success messages
                assert "Successfully sent terminate signal" not in log_content, (
                    "Success messages should not be in error log"
                )
        finally:
            # Cleanup
            if proc.poll() is None:
                proc.kill()
                proc.wait()

    def test_terminate_array_mixed_single_and_multiple_matches(self):
        """Test array where one pattern matches 1 process and another matches multiple processes.

        The pattern matching 1 process should terminate it.
        The pattern matching multiple processes should warn and NOT terminate (safety check).
        """
        # Start one process for pattern A
        test_script_a = os.path.join(self.test_dir, "test_single.py")
        with open(test_script_a, "w") as f:
            f.write("import time\nwhile True:\n    time.sleep(0.1)\n")

        # Start two processes for pattern B
        test_script_b = os.path.join(self.test_dir, "test_multi.py")
        with open(test_script_b, "w") as f:
            f.write("import time\nwhile True:\n    time.sleep(0.1)\n")

        proc_a = subprocess.Popen([sys.executable, test_script_a])
        proc_b1 = subprocess.Popen([sys.executable, test_script_b])
        proc_b2 = subprocess.Popen([sys.executable, test_script_b])
        time.sleep(0.2)

        try:
            # Verify all processes are running
            assert proc_a.poll() is None, "Process A should be running"
            assert proc_b1.poll() is None, "Process B1 should be running"
            assert proc_b2.poll() is None, "Process B2 should be running"

            # Create config with array: pattern A matches 1, pattern B matches 2
            config_content = f"""default_interval = "0.05s"
error_log_file = "{self.error_log_file}"

[[files]]
path = ""
terminate_if_process = ["test_single\\\\.py", "test_multi\\\\.py"]
"""
            with open(self.config_file, "w") as f:
                f.write(config_content)

            watcher = FileWatcher(self.config_file)

            # Execute check
            watcher._check_files()

            # Wait a bit
            time.sleep(0.5)

            # Process A should be terminated (matched exactly 1)
            assert proc_a.poll() is not None, "Process A should have been terminated (single match)"

            # Processes B1 and B2 should still be running (safety check for multiple matches)
            assert proc_b1.poll() is None, "Process B1 should still be running (multiple match safety)"
            assert proc_b2.poll() is None, "Process B2 should still be running (multiple match safety)"

            # Verify log contains warning for B (multiple matches)
            # Successful termination of A should NOT be in error log
            assert os.path.exists(self.error_log_file), "Error log should exist"
            with open(self.error_log_file, "r") as f:
                log_content = f.read()
            assert "test_single" not in log_content, "Successful termination should not be in error log"
            assert "Found 2 processes" in log_content, "Should log warning about multiple-match pattern"
            assert "test_multi" in log_content, "Should mention the multi-match pattern"
        finally:
            # Cleanup
            for proc in [proc_a, proc_b1, proc_b2]:
                if proc.poll() is None:
                    proc.kill()
                    proc.wait()


class TestProcessDetectorEnhancements:
    """Test cases for ProcessDetector enhancements."""

    def test_get_all_matching_processes(self):
        """Test getting all matching processes with PIDs."""
        # Get all python processes (should be at least one - this test itself)
        matches = ProcessDetector.get_all_matching_processes(r"python")

        assert isinstance(matches, list), "Should return a list"
        assert len(matches) > 0, "Should find at least one python process"

        # Verify structure
        for pid, name in matches:
            assert isinstance(pid, int), "PID should be an integer"
            assert isinstance(name, str), "Name should be a string"
            assert pid > 0, "PID should be positive"

    def test_get_all_matching_processes_no_match(self):
        """Test getting all matching processes when none exist."""
        matches = ProcessDetector.get_all_matching_processes(r"nonexistent_xyz123")

        assert isinstance(matches, list), "Should return a list"
        assert len(matches) == 0, "Should return empty list for no matches"

    def test_get_all_matching_processes_invalid_regex(self):
        """Test that invalid regex is handled gracefully."""
        matches = ProcessDetector.get_all_matching_processes(r"[invalid(regex")

        assert isinstance(matches, list), "Should return a list"
        assert len(matches) == 0, "Should return empty list for invalid regex"

    def test_terminate_process_invalid_pid(self):
        """Test that terminating invalid PID is handled gracefully."""
        # Use a very high PID that doesn't exist
        result = ProcessDetector.terminate_process(999999)

        assert result is False, "Should return False for non-existent process"

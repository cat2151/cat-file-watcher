#!/usr/bin/env python3
"""
Basic tests for cat_file_watcher
"""
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path

# Add src directory to path to import the module
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))
from cat_file_watcher import FileWatcher
from config_loader import ConfigLoader
from process_detector import ProcessDetector


class TestFileWatcher(unittest.TestCase):
    """Test cases for FileWatcher class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, 'test_config.toml')
        self.test_file = os.path.join(self.test_dir, 'test.txt')
        
        # Create a test file
        with open(self.test_file, 'w') as f:
            f.write('Initial content\n')
        
        # Create a test config
        config_content = f'''[files]
"{self.test_file}" = {{ command = "echo 'File changed'" }}
'''
        with open(self.config_file, 'w') as f:
            f.write(config_content)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_load_config(self):
        """Test that configuration is loaded correctly."""
        watcher = FileWatcher(self.config_file)
        self.assertIn('files', watcher.config)
        self.assertIn(self.test_file, watcher.config['files'])
    
    def test_get_file_timestamp(self):
        """Test that file timestamps are retrieved correctly."""
        watcher = FileWatcher(self.config_file)
        timestamp = watcher._get_file_timestamp(self.test_file)
        self.assertIsNotNone(timestamp)
        self.assertIsInstance(timestamp, float)
    
    def test_get_nonexistent_file_timestamp(self):
        """Test that nonexistent files return None for timestamp."""
        watcher = FileWatcher(self.config_file)
        timestamp = watcher._get_file_timestamp('/nonexistent/file.txt')
        self.assertIsNone(timestamp)
    
    def test_check_files_initializes_timestamps(self):
        """Test that checking files initializes timestamp tracking."""
        watcher = FileWatcher(self.config_file)
        self.assertEqual(len(watcher.file_timestamps), 0)
        watcher._check_files()
        self.assertEqual(len(watcher.file_timestamps), 1)
        self.assertIn(self.test_file, watcher.file_timestamps)
    
    def test_detect_file_change(self):
        """Test that file changes are detected."""
        watcher = FileWatcher(self.config_file)
        
        # Initialize tracking
        watcher._check_files()
        initial_timestamp = watcher.file_timestamps[self.test_file]
        
        # Wait a bit and modify the file
        time.sleep(0.1)
        with open(self.test_file, 'a') as f:
            f.write('Modified content\n')
        
        # Check again - timestamp should be different
        new_timestamp = watcher._get_file_timestamp(self.test_file)
        self.assertNotEqual(initial_timestamp, new_timestamp)
    
    def test_default_interval(self):
        """Test that default interval is used when not specified."""
        watcher = FileWatcher(self.config_file)
        settings = {}
        interval = watcher._get_interval_for_file(settings)
        # Default is 1000ms = 1 second
        self.assertEqual(interval, 1.0)
    
    def test_custom_default_interval(self):
        """Test that custom default interval is respected."""
        # Create config with custom default interval
        config_content = f'''default_interval = 500

[files]
"{self.test_file}" = {{ command = "echo 'File changed'" }}
'''
        with open(self.config_file, 'w') as f:
            f.write(config_content)
        
        watcher = FileWatcher(self.config_file)
        settings = {}
        interval = watcher._get_interval_for_file(settings)
        # Custom default is 500ms = 0.5 second
        self.assertEqual(interval, 0.5)
    
    def test_per_file_interval(self):
        """Test that per-file interval overrides default."""
        # Create config with per-file interval
        config_content = f'''default_interval = 1000

[files]
"{self.test_file}" = {{ command = "echo 'File changed'", interval = 250 }}
'''
        with open(self.config_file, 'w') as f:
            f.write(config_content)
        
        watcher = FileWatcher(self.config_file)
        settings = watcher.config['files'][self.test_file]
        interval = watcher._get_interval_for_file(settings)
        # Per-file interval is 250ms = 0.25 second
        self.assertEqual(interval, 0.25)
    
    def test_interval_throttling(self):
        """Test that files are not checked more frequently than their interval."""
        # Create config with a longer interval
        config_content = f'''default_interval = 500

[files]
"{self.test_file}" = {{ command = "echo 'File changed'" }}
'''
        with open(self.config_file, 'w') as f:
            f.write(config_content)
        
        watcher = FileWatcher(self.config_file)
        
        # First check should process the file
        watcher._check_files()
        self.assertIn(self.test_file, watcher.file_last_check)
        first_check_time = watcher.file_last_check[self.test_file]
        
        # Immediate second check should skip the file (not enough time passed)
        time.sleep(0.05)  # Much less than 500ms
        watcher._check_files()
        # Check time should not have changed
        self.assertEqual(watcher.file_last_check[self.test_file], first_check_time)
        
        # After waiting for the interval, file should be checked again
        time.sleep(0.5)  # Wait for 500ms interval
        watcher._check_files()
        # Check time should have been updated
        self.assertGreater(watcher.file_last_check[self.test_file], first_check_time)
    
    def test_interval_division_by_1000_various_values(self):
        """Test that interval division by 1000 works correctly for various values.
        
        This test clarifies that dividing milliseconds by 1000.0 produces correct
        float values in seconds for all common use cases.
        """
        watcher = FileWatcher(self.config_file)
        
        # Test various millisecond values and their expected second equivalents
        test_cases = [
            # (interval_ms, expected_seconds)
            (1000, 1.0),      # 1 second
            (500, 0.5),       # Half second (mentioned in issue)
            (250, 0.25),      # Quarter second
            (100, 0.1),       # 100 milliseconds
            (1, 0.001),       # 1 millisecond
            (2000, 2.0),      # 2 seconds
            (5000, 5.0),      # 5 seconds
            (10000, 10.0),    # 10 seconds
            (333, 0.333),     # Odd value
            (1500, 1.5),      # 1.5 seconds
        ]
        
        for interval_ms, expected_seconds in test_cases:
            settings = {'interval': interval_ms}
            result = watcher._get_interval_for_file(settings)
            self.assertEqual(result, expected_seconds,
                           f"Failed for {interval_ms}ms: expected {expected_seconds}s, got {result}s")
    
    def test_interval_division_returns_float(self):
        """Test that interval division always returns a float type.
        
        This ensures that even integer millisecond values produce float results,
        which is important for time.sleep() and time comparison operations.
        """
        watcher = FileWatcher(self.config_file)
        
        # Test with integer input
        settings = {'interval': 1000}
        result = watcher._get_interval_for_file(settings)
        self.assertIsInstance(result, float, "Result should be a float type")
        self.assertEqual(result, 1.0)
        
        # Test with another integer that should produce a fractional result
        settings = {'interval': 500}
        result = watcher._get_interval_for_file(settings)
        self.assertIsInstance(result, float, "Result should be a float type")
        self.assertEqual(result, 0.5)
    
    def test_process_detection(self):
        """Test that process detection works correctly."""
        watcher = FileWatcher(self.config_file)
        
        # Test that current python process is detected
        # The process name should be "python" or "python3"
        result = watcher._is_process_running(r'python')
        self.assertTrue(result, "Should detect running python process")
        
        # Test with a non-existent process
        result = watcher._is_process_running(r'nonexistent_process_xyz123')
        self.assertFalse(result, "Should not detect non-existent process")
    
    def test_process_detection_with_regex(self):
        """Test that process detection works with regex patterns."""
        watcher = FileWatcher(self.config_file)
        
        # Test regex pattern matching
        result = watcher._is_process_running(r'python[23]?')
        self.assertTrue(result, "Should detect python process with regex")
        
        # Test case-insensitive matching (just ensure it doesn't crash)
        result = watcher._is_process_running(r'(?i)PYTHON')
        # Result may vary based on process name case, but should not crash
        self.assertIsInstance(result, bool)
    
    def test_process_detection_invalid_regex(self):
        """Test that invalid regex patterns are handled gracefully."""
        watcher = FileWatcher(self.config_file)
        
        # Invalid regex pattern
        result = watcher._is_process_running(r'[invalid(regex')
        self.assertFalse(result, "Should return False for invalid regex")
    
    def test_command_suppression_when_process_exists(self):
        """Test that command execution is suppressed when specified process exists."""
        # Create a test file that will be modified
        test_output = os.path.join(self.test_dir, 'output.txt')
        
        # Create config with suppress_if_process for a running process (python)
        # Use short interval to speed up test
        config_content = f'''default_interval = 50

[files]
"{self.test_file}" = {{ command = "echo 'executed' > {test_output}", suppress_if_process = "python" }}
'''
        with open(self.config_file, 'w') as f:
            f.write(config_content)
        
        watcher = FileWatcher(self.config_file)
        
        # Initialize tracking
        watcher._check_files()
        
        # Modify the file
        time.sleep(0.1)
        with open(self.test_file, 'a') as f:
            f.write('Modified content\n')
        
        # Check files - command should be suppressed
        watcher._check_files()
        
        # Output file should NOT be created because command was suppressed
        self.assertFalse(os.path.exists(test_output), 
                        "Command should have been suppressed, output file should not exist")
    
    def test_command_execution_when_process_not_exists(self):
        """Test that command executes normally when specified process doesn't exist."""
        # Create a test file that will be modified
        test_output = os.path.join(self.test_dir, 'output.txt')
        
        # Create config with suppress_if_process for a non-existent process
        # Use short interval to speed up test
        config_content = f'''default_interval = 50

[files]
"{self.test_file}" = {{ command = "echo 'executed' > {test_output}", suppress_if_process = "nonexistent_process_xyz123" }}
'''
        with open(self.config_file, 'w') as f:
            f.write(config_content)
        
        watcher = FileWatcher(self.config_file)
        
        # Initialize tracking
        watcher._check_files()
        
        # Modify the file
        time.sleep(0.1)
        with open(self.test_file, 'a') as f:
            f.write('Modified content\n')
        
        # Check files - command should execute
        watcher._check_files()
        
        # Output file should be created because process doesn't exist
        self.assertTrue(os.path.exists(test_output), 
                       "Command should have executed, output file should exist")
    
    def test_command_execution_without_suppress_if_process(self):
        """Test that commands execute normally when suppress_if_process is not specified."""
        # Create a test file that will be modified
        test_output = os.path.join(self.test_dir, 'output.txt')
        
        # Create config without suppress_if_process
        # Use short interval to speed up test
        config_content = f'''default_interval = 50

[files]
"{self.test_file}" = {{ command = "echo 'executed' > {test_output}" }}
'''
        with open(self.config_file, 'w') as f:
            f.write(config_content)
        
        watcher = FileWatcher(self.config_file)
        
        # Initialize tracking
        watcher._check_files()
        
        # Modify the file
        time.sleep(0.1)
        with open(self.test_file, 'a') as f:
            f.write('Modified content\n')
        
        # Check files - command should execute
        watcher._check_files()
        
        # Output file should be created
        self.assertTrue(os.path.exists(test_output), 
                       "Command should have executed, output file should exist")


if __name__ == '__main__':
    unittest.main()

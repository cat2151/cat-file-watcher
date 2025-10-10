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


if __name__ == '__main__':
    unittest.main()

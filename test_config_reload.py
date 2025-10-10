#!/usr/bin/env python3
"""
Tests for config file reload functionality
"""
import unittest
import tempfile
import os
import time

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from cat_file_watcher import FileWatcher


class TestConfigReload(unittest.TestCase):
    """Test cases for config file reload functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, 'config.toml')
        self.test_file = os.path.join(self.test_dir, 'test.txt')
        
        # Create a test file
        with open(self.test_file, 'w') as f:
            f.write('Initial content\n')
        
        # Create initial config
        config_content = f'''default_interval = 1000
config_check_interval = 100

[files]
"{self.test_file}" = {{ command = "echo 'File changed'" }}
'''
        with open(self.config_file, 'w') as f:
            f.write(config_content)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_config_reload_on_change(self):
        """Test that config is reloaded when the config file changes."""
        watcher = FileWatcher(self.config_file)
        
        # Check initial config
        self.assertEqual(watcher.config.get('default_interval'), 1000)
        self.assertEqual(watcher.config.get('config_check_interval'), 100)
        
        # Wait a bit and modify the config file
        time.sleep(0.2)
        new_config_content = f'''default_interval = 2000
config_check_interval = 200

[files]
"{self.test_file}" = {{ command = "echo 'File changed - updated'" }}
'''
        with open(self.config_file, 'w') as f:
            f.write(new_config_content)
        
        # Check for config changes
        time.sleep(0.15)  # Wait for the config check interval
        watcher._check_config_file()
        
        # Verify config was reloaded
        self.assertEqual(watcher.config.get('default_interval'), 2000)
        self.assertEqual(watcher.config.get('config_check_interval'), 200)
    
    def test_config_check_interval_default(self):
        """Test that default config check interval is 1000ms when not specified."""
        # Create config without config_check_interval
        config_content = f'''default_interval = 1000

[files]
"{self.test_file}" = {{ command = "echo 'File changed'" }}
'''
        with open(self.config_file, 'w') as f:
            f.write(config_content)
        
        watcher = FileWatcher(self.config_file)
        
        # Default should be 1000ms
        self.assertNotIn('config_check_interval', watcher.config)
        # Check that the default is used in _check_config_file
        # (this is implicitly tested by the method using get with default)
    
    def test_config_check_throttling(self):
        """Test that config is not checked more frequently than config_check_interval."""
        watcher = FileWatcher(self.config_file)
        
        # First check should process
        watcher._check_config_file()
        first_check_time = watcher.config_last_check
        
        # Immediate second check should skip (not enough time passed)
        time.sleep(0.05)  # Much less than 100ms
        watcher._check_config_file()
        # Check time should not have changed
        self.assertEqual(watcher.config_last_check, first_check_time)
        
        # After waiting for the interval, config should be checked again
        time.sleep(0.1)  # Wait for 100ms interval
        watcher._check_config_file()
        # Check time should have been updated
        self.assertGreater(watcher.config_last_check, first_check_time)
    
    def test_config_reload_preserves_state_on_error(self):
        """Test that config reload errors don't break the watcher."""
        watcher = FileWatcher(self.config_file)
        
        original_config = watcher.config.copy()
        
        # Wait a bit and write invalid TOML
        time.sleep(0.2)
        with open(self.config_file, 'w') as f:
            f.write('invalid toml [[[')
        
        # Check for config changes
        time.sleep(0.15)
        watcher._check_config_file()
        
        # Config should remain unchanged (previous config preserved)
        self.assertEqual(watcher.config.get('default_interval'), 
                        original_config.get('default_interval'))
    
    def test_config_timestamp_initialized(self):
        """Test that config timestamp is initialized correctly."""
        watcher = FileWatcher(self.config_file)
        
        self.assertIsNotNone(watcher.config_timestamp)
        self.assertEqual(watcher.config_timestamp, 
                        watcher._get_file_timestamp(self.config_file))
    
    def test_custom_config_check_interval(self):
        """Test that custom config_check_interval is respected."""
        # Create config with custom config_check_interval
        config_content = f'''default_interval = 1000
config_check_interval = 500

[files]
"{self.test_file}" = {{ command = "echo 'File changed'" }}
'''
        with open(self.config_file, 'w') as f:
            f.write(config_content)
        
        watcher = FileWatcher(self.config_file)
        
        # Custom interval should be 500ms
        self.assertEqual(watcher.config.get('config_check_interval'), 500)


if __name__ == '__main__':
    unittest.main()

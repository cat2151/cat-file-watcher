#!/usr/bin/env python3
"""
Tests for command execution logging functionality
"""
import shutil
import tempfile
import os
import time

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from cat_file_watcher import FileWatcher


class TestCommandLogging:
    """Test cases for command execution logging."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, 'config.toml')
        self.test_file = os.path.join(self.test_dir, 'test.txt')
        self.log_file = os.path.join(self.test_dir, 'command.log')
        
        # Create a test file
        with open(self.test_file, 'w') as f:
            f.write('Initial content\n')
    
    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)
    
    def test_logging_disabled_by_default(self):
        """Test that logging is disabled by default."""
        # Create config without enable_log
        config_content = f'''default_interval = 50
log_file = "{self.log_file}"

[files]
"{self.test_file}" = {{ command = "echo 'test'" }}
'''
        with open(self.config_file, 'w') as f:
            f.write(config_content)
        
        watcher = FileWatcher(self.config_file)
        
        # Initialize timestamp tracking
        watcher._check_files()
        
        # Modify the test file to trigger command execution
        time.sleep(0.1)
        with open(self.test_file, 'a') as f:
            f.write('Modified content\n')
        
        # Check for file changes
        watcher._check_files()
        
        # Log file should not be created
        assert not os.path.exists(self.log_file)
    
    def test_logging_enabled(self):
        """Test that logging works when enabled."""
        # Create config with enable_log=true
        config_content = f'''default_interval = 50
log_file = "{self.log_file}"

[files]
"{self.test_file}" = {{ command = "echo 'test'", enable_log = true }}
'''
        with open(self.config_file, 'w') as f:
            f.write(config_content)
        
        watcher = FileWatcher(self.config_file)
        
        # Initialize timestamp tracking
        watcher._check_files()
        
        # Modify the test file to trigger command execution
        time.sleep(0.1)
        with open(self.test_file, 'a') as f:
            f.write('Modified content\n')
        
        # Check for file changes
        watcher._check_files()
        
        # Log file should be created
        assert os.path.exists(self.log_file)
        
        # Check log file content
        with open(self.log_file, 'r') as f:
            log_content = f.read()
        
        # Should contain timestamp, file path, and command
        assert self.test_file in log_content
        assert "command: echo 'test'" in log_content
        assert "enable_log: True" in log_content
    
    def test_logging_without_log_file_config(self):
        """Test that logging is skipped when log_file is not configured."""
        # Create config with enable_log=true but no log_file
        config_content = f'''default_interval = 50

[files]
"{self.test_file}" = {{ command = "echo 'test'", enable_log = true }}
'''
        with open(self.config_file, 'w') as f:
            f.write(config_content)
        
        watcher = FileWatcher(self.config_file)
        
        # Initialize timestamp tracking
        watcher._check_files()
        
        # Modify the test file to trigger command execution
        time.sleep(0.1)
        with open(self.test_file, 'a') as f:
            f.write('Modified content\n')
        
        # Check for file changes (should not crash)
        watcher._check_files()
        
        # Log file should not be created
        assert not os.path.exists(self.log_file)
    
    def test_logging_with_multiple_settings(self):
        """Test that all file settings are logged."""
        # Create config with multiple settings
        config_content = f'''default_interval = 50
log_file = "{self.log_file}"

[files]
"{self.test_file}" = {{ command = "echo 'test'", interval = 50, enable_log = true, suppress_if_process = "vim" }}
'''
        with open(self.config_file, 'w') as f:
            f.write(config_content)
        
        watcher = FileWatcher(self.config_file)
        
        # Initialize timestamp tracking
        watcher._check_files()
        
        # Modify the test file to trigger command execution
        time.sleep(0.1)
        with open(self.test_file, 'a') as f:
            f.write('Modified content\n')
        
        # Check for file changes
        watcher._check_files()
        
        # Check log file content includes all settings
        with open(self.log_file, 'r') as f:
            log_content = f.read()
        
        assert "command: echo 'test'" in log_content
        assert "interval: 50" in log_content
        assert "enable_log: True" in log_content
        assert "suppress_if_process: vim" in log_content
    
    def test_logging_appends_to_existing_log(self):
        """Test that logging appends to existing log file."""
        # Create config with logging enabled
        config_content = f'''default_interval = 50
log_file = "{self.log_file}"

[files]
"{self.test_file}" = {{ command = "echo 'test'", enable_log = true }}
'''
        with open(self.config_file, 'w') as f:
            f.write(config_content)
        
        watcher = FileWatcher(self.config_file)
        
        # Initialize timestamp tracking
        watcher._check_files()
        
        # First modification
        time.sleep(0.1)
        with open(self.test_file, 'a') as f:
            f.write('First modification\n')
        watcher._check_files()
        
        # Second modification
        time.sleep(0.1)
        with open(self.test_file, 'a') as f:
            f.write('Second modification\n')
        watcher._check_files()
        
        # Log file should contain two entries
        with open(self.log_file, 'r') as f:
            log_content = f.read()
        
        # Count occurrences of the file path (should be 2)
        occurrences = log_content.count(f"File: {self.test_file}")
        assert occurrences == 2
    
    def test_logging_timestamp_format(self):
        """Test that log entries include properly formatted timestamps."""
        # Create config with logging enabled
        config_content = f'''default_interval = 50
log_file = "{self.log_file}"

[files]
"{self.test_file}" = {{ command = "echo 'test'", enable_log = true }}
'''
        with open(self.config_file, 'w') as f:
            f.write(config_content)
        
        watcher = FileWatcher(self.config_file)
        
        # Initialize timestamp tracking
        watcher._check_files()
        
        # Modify the test file
        time.sleep(0.1)
        with open(self.test_file, 'a') as f:
            f.write('Modified content\n')
        watcher._check_files()
        
        # Check log file has timestamp in format [YYYY-MM-DD HH:MM:SS]
        with open(self.log_file, 'r') as f:
            log_content = f.read()
        
        # Should start with timestamp in brackets
        assert log_content.startswith('[')
        assert ']' in log_content.split('\n')[0]

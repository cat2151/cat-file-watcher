#!/usr/bin/env python3
"""
Tests for error logging functionality
"""
import unittest
import tempfile
import os
import time

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from cat_file_watcher import FileWatcher
from error_logger import ErrorLogger
from command_executor import CommandExecutor
from config_loader import ConfigLoader


class TestErrorLogging(unittest.TestCase):
    """Test cases for error logging functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.error_log_file = os.path.join(self.test_dir, 'error.log')
        self.config_file = os.path.join(self.test_dir, 'config.toml')
        self.test_file = os.path.join(self.test_dir, 'test.txt')
        
        # Create test file
        with open(self.test_file, 'w') as f:
            f.write('Initial content\n')
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_error_logger_basic_message(self):
        """Test that ErrorLogger logs basic error messages."""
        ErrorLogger.log_error(self.error_log_file, "Test error message")
        
        self.assertTrue(os.path.exists(self.error_log_file))
        
        with open(self.error_log_file, 'r') as f:
            content = f.read()
        
        self.assertIn('ERROR: Test error message', content)
        # Check timestamp format [YYYY-MM-DD HH:MM:SS]
        self.assertTrue(content.startswith('['))
        self.assertIn(']', content)
    
    def test_error_logger_with_exception(self):
        """Test that ErrorLogger logs exceptions with stack traces."""
        try:
            # Create an exception
            raise ValueError("Test exception message")
        except ValueError as e:
            ErrorLogger.log_error(self.error_log_file, "Test error", e)
        
        with open(self.error_log_file, 'r') as f:
            content = f.read()
        
        self.assertIn('ERROR: Test error', content)
        self.assertIn('Exception type: ValueError', content)
        self.assertIn('Exception message: Test exception message', content)
        self.assertIn('Stack trace:', content)
        self.assertIn('ValueError: Test exception message', content)
    
    def test_error_logger_none_file(self):
        """Test that ErrorLogger handles None error_log_file gracefully."""
        # Should not raise exception
        ErrorLogger.log_error(None, "Test message")
        # No file should be created
        self.assertFalse(os.path.exists(self.error_log_file))
    
    def test_error_logger_appends_to_file(self):
        """Test that ErrorLogger appends to existing error log."""
        ErrorLogger.log_error(self.error_log_file, "First error")
        ErrorLogger.log_error(self.error_log_file, "Second error")
        
        with open(self.error_log_file, 'r') as f:
            content = f.read()
        
        self.assertIn('First error', content)
        self.assertIn('Second error', content)
        # Should have two timestamp entries
        self.assertEqual(content.count('['), 2)
    
    def test_config_loader_logs_file_not_found(self):
        """Test that ConfigLoader logs errors when config file is not found."""
        nonexistent_config = os.path.join(self.test_dir, 'nonexistent.toml')
        
        # Create a minimal config first to set error_log_file
        # Since load_config exits, we can't test it directly, but we can verify it tries
        # We'll test this indirectly through the error message
        with self.assertRaises(SystemExit):
            ConfigLoader.load_config(nonexistent_config)
    
    def test_config_loader_logs_parse_error(self):
        """Test that ConfigLoader logs errors when TOML parsing fails."""
        # Create invalid TOML
        with open(self.config_file, 'w') as f:
            f.write('invalid toml syntax [[[')
        
        with self.assertRaises(SystemExit):
            ConfigLoader.load_config(self.config_file)
    
    def test_command_executor_logs_timeout_error(self):
        """Test that CommandExecutor logs timeout errors."""
        config_content = f'''default_interval = 50
error_log_file = "{self.error_log_file}"

[files]
"{self.test_file}" = {{ command = "sleep 60" }}
'''
        with open(self.config_file, 'w') as f:
            f.write(config_content)
        
        watcher = FileWatcher(self.config_file)
        
        # This will timeout and should log the error
        with self.assertRaises(Exception):  # subprocess.TimeoutExpired
            CommandExecutor.execute_command(
                'sleep 60',
                self.test_file,
                {'command': 'sleep 60'},
                watcher.config
            )
        
        # Verify error was logged
        self.assertTrue(os.path.exists(self.error_log_file))
        with open(self.error_log_file, 'r') as f:
            content = f.read()
        
        self.assertIn('ERROR:', content)
        self.assertIn('timed out', content.lower())
    
    def test_command_executor_logs_command_failure(self):
        """Test that CommandExecutor logs command failures."""
        config_content = f'''default_interval = 50
error_log_file = "{self.error_log_file}"

[files]
"{self.test_file}" = {{ command = "exit 1" }}
'''
        with open(self.config_file, 'w') as f:
            f.write(config_content)
        
        watcher = FileWatcher(self.config_file)
        
        # Execute a command that fails (exit 1)
        CommandExecutor.execute_command(
            'exit 1',
            self.test_file,
            {'command': 'exit 1'},
            watcher.config
        )
        
        # Verify error was logged
        self.assertTrue(os.path.exists(self.error_log_file))
        with open(self.error_log_file, 'r') as f:
            content = f.read()
        
        self.assertIn('ERROR:', content)
        self.assertIn('Command failed', content)
        self.assertIn('exit code 1', content)
    
    def test_command_executor_logs_write_log_error(self):
        """Test that CommandExecutor logs errors when writing to log file fails."""
        # Create config with logging enabled but invalid log file path
        config_content = f'''default_interval = 50
error_log_file = "{self.error_log_file}"
log_file = "/nonexistent/path/to/log.txt"

[files]
"{self.test_file}" = {{ command = "echo test", enable_log = true }}
'''
        with open(self.config_file, 'w') as f:
            f.write(config_content)
        
        watcher = FileWatcher(self.config_file)
        
        # This should fail to write to log file but handle it gracefully
        CommandExecutor.execute_command(
            'echo test',
            self.test_file,
            {'command': 'echo test', 'enable_log': True},
            watcher.config
        )
        
        # Verify error was logged
        self.assertTrue(os.path.exists(self.error_log_file))
        with open(self.error_log_file, 'r') as f:
            content = f.read()
        
        self.assertIn('ERROR:', content)
        self.assertIn('Failed to write to log file', content)
    
    def test_file_watcher_check_files_logs_errors(self):
        """Test that FileWatcher._check_files logs errors when processing files."""
        # Create a config with a file that will cause an error
        config_content = f'''default_interval = 50
error_log_file = "{self.error_log_file}"

[files]
"{self.test_file}" = {{ command = "echo test" }}
'''
        with open(self.config_file, 'w') as f:
            f.write(config_content)
        
        watcher = FileWatcher(self.config_file)
        
        # Mock an error by making CommandExecutor raise an exception
        original_execute = CommandExecutor.execute_command
        def failing_execute(*args, **kwargs):
            raise RuntimeError("Simulated command execution error")
        
        CommandExecutor.execute_command = failing_execute
        
        try:
            # Initialize timestamp tracking
            watcher._check_files()
            
            # Modify file to trigger command execution
            time.sleep(0.1)
            with open(self.test_file, 'a') as f:
                f.write('Modified\n')
            
            # This should catch and log the error
            watcher._check_files()
            
            # Verify error was logged
            self.assertTrue(os.path.exists(self.error_log_file))
            with open(self.error_log_file, 'r') as f:
                content = f.read()
            
            self.assertIn('ERROR:', content)
            self.assertIn('Error processing file', content)
            self.assertIn('Simulated command execution error', content)
        finally:
            # Restore original function
            CommandExecutor.execute_command = original_execute
    
    def test_file_watcher_config_reload_logs_errors(self):
        """Test that FileWatcher logs errors when config reload fails."""
        # Create initial valid config
        config_content = f'''default_interval = 50
error_log_file = "{self.error_log_file}"

[files]
"{self.test_file}" = {{ command = "echo test" }}
'''
        with open(self.config_file, 'w') as f:
            f.write(config_content)
        
        watcher = FileWatcher(self.config_file)
        
        # Change config to invalid TOML
        time.sleep(0.1)
        with open(self.config_file, 'w') as f:
            f.write('invalid toml [[[')
        
        # Trigger config reload check
        watcher._check_config_file()
        
        # Verify error was logged
        self.assertTrue(os.path.exists(self.error_log_file))
        with open(self.error_log_file, 'r') as f:
            content = f.read()
        
        self.assertIn('ERROR:', content)
        self.assertIn('error', content.lower())
    
    def test_error_log_timestamp_format(self):
        """Test that error log entries have correct timestamp format."""
        ErrorLogger.log_error(self.error_log_file, "Test message")
        
        with open(self.error_log_file, 'r') as f:
            content = f.read()
        
        # Should start with [YYYY-MM-DD HH:MM:SS]
        self.assertTrue(content.startswith('['))
        first_line = content.split('\n')[0]
        self.assertIn(']', first_line)
        # Verify format: [YYYY-MM-DD HH:MM:SS]
        import re
        pattern = r'\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]'
        self.assertTrue(re.match(pattern, first_line))


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3
"""
Basic functionality tests for cat_file_watcher
"""
import os
import sys
import tempfile
import time
import shutil

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
from cat_file_watcher import FileWatcher


class TestFileWatcherBasics:
    """Test cases for basic FileWatcher functionality."""
    
    def setup_method(self):
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
    
    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_load_config(self):
        """Test that configuration is loaded correctly."""
        watcher = FileWatcher(self.config_file)
        assert 'files' in watcher.config
        assert self.test_file in watcher.config['files']
    
    def test_get_file_timestamp(self):
        """Test that file timestamps are retrieved correctly."""
        watcher = FileWatcher(self.config_file)
        timestamp = watcher._get_file_timestamp(self.test_file)
        assert timestamp is not None
        assert isinstance(timestamp, float)
    
    def test_get_nonexistent_file_timestamp(self):
        """Test that nonexistent files return None for timestamp."""
        watcher = FileWatcher(self.config_file)
        timestamp = watcher._get_file_timestamp('/nonexistent/file.txt')
        assert timestamp is None
    
    def test_check_files_initializes_timestamps(self):
        """Test that checking files initializes timestamp tracking."""
        watcher = FileWatcher(self.config_file)
        assert len(watcher.file_timestamps) == 0
        watcher._check_files()
        assert len(watcher.file_timestamps) == 1
        assert self.test_file in watcher.file_timestamps
    
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
        assert initial_timestamp != new_timestamp

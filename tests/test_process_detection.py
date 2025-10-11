#!/usr/bin/env python3
"""
Process detection tests for cat_file_watcher
"""
import os
import sys
import tempfile
import shutil

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
from cat_file_watcher import FileWatcher


class TestProcessDetection:
    """Test cases for process detection functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, 'test_config.toml')
        self.test_file = os.path.join(self.test_dir, 'test.txt')
        
        with open(self.test_file, 'w') as f:
            f.write('Initial content\n')
        
        config_content = f'''[files]
"{self.test_file}" = {{ command = "echo 'File changed'" }}
'''
        with open(self.config_file, 'w') as f:
            f.write(config_content)
    
    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_process_detection(self):
        """Test that process detection works correctly."""
        watcher = FileWatcher(self.config_file)
        result = watcher._is_process_running(r'python')
        assert result, "Should detect running python process"
        
        result = watcher._is_process_running(r'nonexistent_process_xyz123')
        assert not result, "Should not detect non-existent process"
    
    def test_process_detection_with_regex(self):
        """Test that process detection works with regex patterns."""
        watcher = FileWatcher(self.config_file)
        result = watcher._is_process_running(r'python[23]?')
        assert result, "Should detect python process with regex"
        
        result = watcher._is_process_running(r'(?i)PYTHON')
        assert isinstance(result, bool)
    
    def test_process_detection_invalid_regex(self):
        """Test that invalid regex patterns are handled gracefully."""
        watcher = FileWatcher(self.config_file)
        result = watcher._is_process_running(r'[invalid(regex')
        assert not result, "Should return False for invalid regex"

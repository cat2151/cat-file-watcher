#!/usr/bin/env python3
"""
Interval division tests for cat_file_watcher
"""
import os
import sys
import tempfile
import unittest

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
from cat_file_watcher import FileWatcher


class TestIntervalDivision(unittest.TestCase):
    """Test cases for interval division calculations."""
    
    def setUp(self):
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
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_interval_division_by_1000_various_values(self):
        """Test that interval division by 1000 works correctly for various values."""
        watcher = FileWatcher(self.config_file)
        
        test_cases = [
            (1000, 1.0), (500, 0.5), (250, 0.25), (100, 0.1),
            (1, 0.001), (2000, 2.0), (5000, 5.0), (10000, 10.0),
            (333, 0.333), (1500, 1.5),
        ]
        
        for interval_ms, expected_seconds in test_cases:
            settings = {'interval': interval_ms}
            result = watcher._get_interval_for_file(settings)
            self.assertEqual(result, expected_seconds,
                           f"Failed for {interval_ms}ms: expected {expected_seconds}s")
    
    def test_interval_division_returns_float(self):
        """Test that interval division always returns a float type."""
        watcher = FileWatcher(self.config_file)
        
        settings = {'interval': 1000}
        result = watcher._get_interval_for_file(settings)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 1.0)
        
        settings = {'interval': 500}
        result = watcher._get_interval_for_file(settings)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 0.5)


if __name__ == '__main__':
    unittest.main()

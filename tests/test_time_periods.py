#!/usr/bin/env python3
"""
Tests for time period checking functionality
"""
import os
import sys
import tempfile
import time
import shutil
from datetime import datetime, time as dt_time
from pathlib import Path

# Add src directory to path to import the module
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
from cat_file_watcher import FileWatcher
from time_period_checker import TimePeriodChecker


class TestTimePeriodChecker:
    """Test cases for TimePeriodChecker class."""
    
    def test_parse_time_valid(self):
        """Test parsing valid time strings."""
        test_cases = [
            ("00:00", dt_time(0, 0)),
            ("09:30", dt_time(9, 30)),
            ("12:00", dt_time(12, 0)),
            ("23:59", dt_time(23, 59)),
            ("  14:25  ", dt_time(14, 25)),  # With whitespace
        ]
        for time_str, expected in test_cases:
            result = TimePeriodChecker.parse_time(time_str)
            assert result == expected
    
    def test_parse_time_invalid(self):
        """Test parsing invalid time strings."""
        invalid_times = [
            "24:00",  # Invalid hour
            "12:60",  # Invalid minute
            "25:30",  # Invalid hour
            "12:70",  # Invalid minute
            "12",     # Missing minute
            "12:",    # Missing minute
            ":30",    # Missing hour
            "abc:30", # Non-numeric
            "12:xy",  # Non-numeric
            "",       # Empty string
            "12:30:00", # Too many parts
        ]
        for time_str in invalid_times:
            result = TimePeriodChecker.parse_time(time_str)
            assert result is None
    
    def test_is_in_time_period_normal(self):
        """Test time period check for normal periods (not spanning midnight)."""
        start = dt_time(9, 0)   # 09:00
        end = dt_time(17, 0)    # 17:00
        
        # Times within period
        assert(TimePeriodChecker.is_in_time_period(start, end, dt_time(9, 0)))
        assert(TimePeriodChecker.is_in_time_period(start, end, dt_time(12, 0)))
        assert(TimePeriodChecker.is_in_time_period(start, end, dt_time(17, 0)))
        
        # Times outside period
        assert not(TimePeriodChecker.is_in_time_period(start, end, dt_time(8, 59)))
        assert not(TimePeriodChecker.is_in_time_period(start, end, dt_time(17, 1)))
        assert not(TimePeriodChecker.is_in_time_period(start, end, dt_time(23, 0)))
    
    def test_is_in_time_period_spanning_midnight(self):
        """Test time period check for periods spanning midnight."""
        start = dt_time(23, 0)  # 23:00
        end = dt_time(1, 0)     # 01:00
        
        # Times within period (before midnight)
        assert(TimePeriodChecker.is_in_time_period(start, end, dt_time(23, 0)))
        assert(TimePeriodChecker.is_in_time_period(start, end, dt_time(23, 30)))
        
        # Times within period (after midnight)
        assert(TimePeriodChecker.is_in_time_period(start, end, dt_time(0, 0)))
        assert(TimePeriodChecker.is_in_time_period(start, end, dt_time(0, 30)))
        assert(TimePeriodChecker.is_in_time_period(start, end, dt_time(1, 0)))
        
        # Times outside period
        assert not(TimePeriodChecker.is_in_time_period(start, end, dt_time(1, 1)))
        assert not(TimePeriodChecker.is_in_time_period(start, end, dt_time(12, 0)))
        assert not(TimePeriodChecker.is_in_time_period(start, end, dt_time(22, 59)))
    
    def test_is_in_time_period_edge_case_23_59_to_00_01(self):
        """Test specific edge case mentioned in requirements: 23:59 to 00:01."""
        start = dt_time(23, 59)  # 23:59
        end = dt_time(0, 1)      # 00:01
        
        # Times within period
        assert(TimePeriodChecker.is_in_time_period(start, end, dt_time(23, 59)))
        assert(TimePeriodChecker.is_in_time_period(start, end, dt_time(0, 0)))
        assert(TimePeriodChecker.is_in_time_period(start, end, dt_time(0, 1)))
        
        # Times outside period
        assert not(TimePeriodChecker.is_in_time_period(start, end, dt_time(23, 58)))
        assert not(TimePeriodChecker.is_in_time_period(start, end, dt_time(0, 2)))
    
    def test_get_time_period_config_valid(self):
        """Test retrieving valid time period configuration."""
        config = {
            'time_periods': {
                'business_hours': {
                    'start': '09:00',
                    'end': '17:00'
                },
                'night_shift': {
                    'start': '23:00',
                    'end': '01:00'
                }
            }
        }
        
        # Test business hours
        period = TimePeriodChecker.get_time_period_config(config, 'business_hours')
        assert period is not None
        assert period['start'] == dt_time(9, 0)
        assert period['end'] == dt_time(17, 0)
        
        # Test night shift
        period = TimePeriodChecker.get_time_period_config(config, 'night_shift')
        assert period is not None
        assert period['start'] == dt_time(23, 0)
        assert period['end'] == dt_time(1, 0)
    
    def test_get_time_period_config_invalid(self):
        """Test retrieving invalid or non-existent time period configuration."""
        config = {
            'time_periods': {
                'valid': {
                    'start': '09:00',
                    'end': '17:00'
                },
                'missing_end': {
                    'start': '09:00'
                },
                'invalid_time': {
                    'start': '25:00',
                    'end': '17:00'
                }
            }
        }
        
        # Non-existent period
        assert TimePeriodChecker.get_time_period_config(config, 'nonexistent') is None
        
        # Missing end time
        assert TimePeriodChecker.get_time_period_config(config, 'missing_end') is None
        
        # Invalid time format
        assert TimePeriodChecker.get_time_period_config(config, 'invalid_time') is None
        
        # No time_periods section
        assert TimePeriodChecker.get_time_period_config({}, 'any') is None
    
    def test_should_monitor_file_without_time_period(self):
        """Test that files without time_period setting are always monitored."""
        config = {}
        settings = {'command': 'echo test'}
        
        # Should always return True when no time_period is specified
        assert(TimePeriodChecker.should_monitor_file(config, settings))
    
    def test_should_monitor_file_with_valid_period(self):
        """Test file monitoring with valid time period."""
        config = {
            'time_periods': {
                'test_period': {
                    'start': '00:00',
                    'end': '23:59'
                }
            }
        }
        settings = {
            'command': 'echo test',
            'time_period': 'test_period'
        }
        
        # Should return True for any time within 00:00-23:59 (whole day)
        assert(TimePeriodChecker.should_monitor_file(config, settings))
    
    def test_should_monitor_file_with_invalid_period(self):
        """Test that invalid time period defaults to monitoring."""
        config = {
            'time_periods': {
                'valid': {
                    'start': '09:00',
                    'end': '17:00'
                }
            }
        }
        settings = {
            'command': 'echo test',
            'time_period': 'nonexistent'  # Period doesn't exist
        }
        
        # Should default to monitoring with a warning
        assert(TimePeriodChecker.should_monitor_file(config, settings))


class TestFileWatcherWithTimePeriods:
    """Test cases for FileWatcher with time period functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, 'config.toml')
        self.test_file = os.path.join(self.test_dir, 'test.txt')
        
        # Create a test file
        with open(self.test_file, 'w') as f:
            f.write('Initial content\n')
    
    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)
    
    def test_file_monitoring_with_active_time_period(self):
        """Test that files are monitored when within active time period."""
        # Create config with a time period that is always active (whole day)
        config_content = f'''default_interval = 100

[time_periods]
always_active = {{ start = "00:00", end = "23:59" }}

[files]
"{self.test_file}" = {{ command = "echo 'test'", time_period = "always_active" }}
'''
        with open(self.config_file, 'w') as f:
            f.write(config_content)
        
        watcher = FileWatcher(self.config_file)
        
        # File should be monitored
        watcher._check_files()
        assert self.test_file in watcher.file_timestamps
    
    def test_file_monitoring_without_time_period(self):
        """Test that files without time_period are monitored normally."""
        config_content = f'''default_interval = 100

[files]
"{self.test_file}" = {{ command = "echo 'test'" }}
'''
        with open(self.config_file, 'w') as f:
            f.write(config_content)
        
        watcher = FileWatcher(self.config_file)
        
        # File should be monitored
        watcher._check_files()
        assert self.test_file in watcher.file_timestamps
    
    def test_config_with_multiple_time_periods(self):
        """Test configuration with multiple time period definitions."""
        config_content = f'''default_interval = 100

[time_periods]
morning = {{ start = "06:00", end = "12:00" }}
afternoon = {{ start = "12:00", end = "18:00" }}
night = {{ start = "22:00", end = "02:00" }}

[files]
"{self.test_file}" = {{ command = "echo 'test'", time_period = "morning" }}
'''
        with open(self.config_file, 'w') as f:
            f.write(config_content)
        
        # Should load without errors
        watcher = FileWatcher(self.config_file)
        assert watcher.config.get('time_periods') is not None
        assert len(watcher.config['time_periods']) == 3

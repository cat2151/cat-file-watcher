#!/usr/bin/env python3
"""
Tests for interval parser
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from interval_parser import IntervalParser


class TestIntervalParser:
    """Test cases for IntervalParser class."""

    def test_parse_seconds(self):
        """Test parsing seconds format."""
        test_cases = [
            ("1s", 1.0),
            ("2s", 2.0),
            ("10s", 10.0),
            ("0.5s", 0.5),
            ("0.25s", 0.25),
            ("1.5s", 1.5),
            ("100s", 100.0),
        ]
        for interval_str, expected in test_cases:
            result = IntervalParser.parse_interval(interval_str)
            assert result == expected, f"Failed for {interval_str}: expected {expected}, got {result}"

    def test_parse_minutes(self):
        """Test parsing minutes format."""
        test_cases = [
            ("1m", 60.0),
            ("2m", 120.0),
            ("5m", 300.0),
            ("0.5m", 30.0),
            ("1.5m", 90.0),
            ("10m", 600.0),
        ]
        for interval_str, expected in test_cases:
            result = IntervalParser.parse_interval(interval_str)
            assert result == expected, f"Failed for {interval_str}: expected {expected}, got {result}"

    def test_parse_hours(self):
        """Test parsing hours format."""
        test_cases = [
            ("1h", 3600.0),
            ("2h", 7200.0),
            ("3h", 10800.0),
            ("0.5h", 1800.0),
            ("1.5h", 5400.0),
            ("24h", 86400.0),
        ]
        for interval_str, expected in test_cases:
            result = IntervalParser.parse_interval(interval_str)
            assert result == expected, f"Failed for {interval_str}: expected {expected}, got {result}"

    def test_parse_milliseconds(self):
        """Test parsing milliseconds format."""
        test_cases = [
            ("500ms", 0.5),
            ("1000ms", 1.0),
            ("100ms", 0.1),
            ("250ms", 0.25),
            ("1ms", 0.001),
            ("2000ms", 2.0),
            ("50ms", 0.05),
        ]
        for interval_str, expected in test_cases:
            result = IntervalParser.parse_interval(interval_str)
            assert result == expected, f"Failed for {interval_str}: expected {expected}, got {result}"

    def test_parse_with_whitespace(self):
        """Test parsing with leading/trailing whitespace."""
        test_cases = [
            ("  1s  ", 1.0),
            (" 2m ", 120.0),
            ("  3h  ", 10800.0),
            (" 0.5s ", 0.5),
            (" 500ms ", 0.5),
        ]
        for interval_str, expected in test_cases:
            result = IntervalParser.parse_interval(interval_str)
            assert result == expected

    def test_parse_decimal_formats(self):
        """Test various decimal number formats."""
        test_cases = [
            ("0.1s", 0.1),
            (".5s", 0.5),
            ("1.0s", 1.0),
            ("2.5m", 150.0),
            ("0.25h", 900.0),
            ("0.5ms", 0.0005),
            ("1.5ms", 0.0015),
        ]
        for interval_str, expected in test_cases:
            result = IntervalParser.parse_interval(interval_str)
            assert result == expected

    def test_parse_invalid_format(self):
        """Test that invalid formats raise ValueError."""
        invalid_formats = [
            "1",  # Missing unit
            "s",  # Missing number
            "1x",  # Invalid unit
            "1.2.3s",  # Invalid number
            "abc",  # Not a number
            "1 s",  # Space between number and unit
            "",  # Empty string
            "1sm",  # Invalid unit combination
            "1 ms",  # Space between number and unit (ms)
        ]
        for invalid_str in invalid_formats:
            with pytest.raises(ValueError, match="Invalid interval format"):
                IntervalParser.parse_interval(invalid_str)

    def test_parse_invalid_type(self):
        """Test that invalid types raise ValueError."""
        invalid_types = [
            None,
            [],
            {},
            True,
            1000,  # Integer not supported anymore
            500,  # Integer not supported anymore
        ]
        for invalid_value in invalid_types:
            with pytest.raises(ValueError, match="Invalid interval"):
                IntervalParser.parse_interval(invalid_value)

    def test_parse_returns_float(self):
        """Test that all parsing returns float type."""
        test_values = ["1s", "2m", "3h"]
        for value in test_values:
            result = IntervalParser.parse_interval(value)
            assert isinstance(result, float), f"Expected float, got {type(result).__name__}"

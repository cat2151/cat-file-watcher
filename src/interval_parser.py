#!/usr/bin/env python3
"""
Interval parser for File Watcher
Parses interval strings in format: "1s", "2m", "3h", "0.5s"
"""

import re


class IntervalParser:
    """Handles parsing of interval strings to seconds."""

    @staticmethod
    def parse_interval(interval_value):
        """Parse interval value to seconds.

        Supports time strings like "1s", "500ms", "2m", "3h", "0.5s".

        Args:
            interval_value: A string with time unit ("1s", "500ms", "2m", "3h", "0.5s")

        Returns:
            float: Interval in seconds

        Raises:
            ValueError: If the interval format is invalid
        """
        # Handle time string format
        if isinstance(interval_value, str):
            # Parse time string format: number + unit (ms/s/m/h)
            # Supports decimal numbers like "0.5s"
            match = re.match(r"^(\d+\.?\d*|\.\d+)(ms|s|m|h)$", interval_value.strip())
            if not match:
                raise ValueError(
                    f"Invalid interval format: '{interval_value}'. "
                    f"Expected format: '500ms' (milliseconds), '1s' (seconds), '2m' (minutes), '3h' (hours), or '0.5s' (decimal)"
                )

            number_str, unit = match.groups()
            number = float(number_str)

            # Convert to seconds based on unit
            if unit == "ms":
                return number / 1000.0
            elif unit == "s":
                return number
            elif unit == "m":
                return number * 60.0
            elif unit == "h":
                return number * 3600.0

        raise ValueError(f"Invalid interval type: {type(interval_value).__name__}. Expected string (time format)")

#!/usr/bin/env python3
"""
Time period checker for File Watcher
Validates if current time is within configured time periods
"""

from datetime import datetime, time

from colorama import Fore

# Support both relative and absolute imports
try:
    from .timestamp_printer import TimestampPrinter
except ImportError:
    from timestamp_printer import TimestampPrinter


class TimePeriodChecker:
    """Handles time period validation for file watching."""

    @staticmethod
    def parse_time(time_str):
        """Parse time string in HH:MM format.

        Args:
            time_str: Time string in format "HH:MM" (e.g., "09:00", "23:59")

        Returns:
            datetime.time object or None if parsing fails
        """
        try:
            parts = time_str.strip().split(":")
            if len(parts) != 2:
                return None
            hour = int(parts[0])
            minute = int(parts[1])
            if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                return None
            return time(hour, minute)
        except (ValueError, AttributeError):
            return None

    @staticmethod
    def is_in_time_period(start_time, end_time, current_time=None):
        """Check if current time is within the specified time period.

        Supports time periods that span across midnight (e.g., 23:00-01:00).

        Args:
            start_time: Start time (datetime.time object)
            end_time: End time (datetime.time object)
            current_time: Current time to check (datetime.time object), defaults to now

        Returns:
            bool: True if current time is within the period, False otherwise
        """
        if current_time is None:
            current_time = datetime.now().time()

        # If start_time < end_time, it's a normal period (e.g., 09:00-17:00)
        if start_time <= end_time:
            return start_time <= current_time <= end_time
        else:
            # Period spans midnight (e.g., 23:00-01:00)
            # Current time is in period if it's >= start OR <= end
            return current_time >= start_time or current_time <= end_time

    @staticmethod
    def get_time_period_config(config, period_name):
        """Get time period configuration by name.

        Args:
            config: Configuration dictionary
            period_name: Name of the time period to retrieve

        Returns:
            dict with 'start' and 'end' keys (as time objects), or None if not found/invalid
        """
        if "time_periods" not in config:
            return None

        time_periods = config["time_periods"]
        if period_name not in time_periods:
            return None

        period_config = time_periods[period_name]
        if "start" not in period_config or "end" not in period_config:
            return None

        start_time = TimePeriodChecker.parse_time(period_config["start"])
        end_time = TimePeriodChecker.parse_time(period_config["end"])

        if start_time is None or end_time is None:
            return None

        return {"start": start_time, "end": end_time}

    @staticmethod
    def should_monitor_file(config, settings):
        """Check if a file should be monitored based on its time period setting.

        Args:
            config: Global configuration dictionary
            settings: File-specific settings dictionary

        Returns:
            bool: True if file should be monitored (no time period or within period),
                  False if outside the configured time period
        """
        # If no time period is specified, always monitor
        if "time_period" not in settings:
            return True

        period_name = settings["time_period"]
        period_config = TimePeriodChecker.get_time_period_config(config, period_name)

        # If time period config is invalid, default to monitoring
        if period_config is None:
            TimestampPrinter.print(f"Warning: Time period '{period_name}' not found or invalid, monitoring anyway", Fore.YELLOW)
            return True

        return TimePeriodChecker.is_in_time_period(period_config["start"], period_config["end"])

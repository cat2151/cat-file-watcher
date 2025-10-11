#!/usr/bin/env python3
"""
Timestamp printer utility for File Watcher
Provides timestamped printing functionality
"""

from datetime import datetime


class TimestampPrinter:
    """Handles printing with optional timestamps."""

    # Global configuration for timestamp display
    _enable_timestamp = True

    @staticmethod
    def set_enable_timestamp(enable):
        """Set whether to enable timestamps in print statements.

        Args:
            enable: Boolean value to enable/disable timestamps
        """
        TimestampPrinter._enable_timestamp = enable

    @staticmethod
    def print(message):
        """Print a message with optional timestamp prefix.

        Args:
            message: The message to print
        """
        if TimestampPrinter._enable_timestamp:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] {message}")
        else:
            print(message)

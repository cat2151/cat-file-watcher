#!/usr/bin/env python3
"""
Timestamp printer utility for File Watcher
Provides timestamped printing functionality
"""

from datetime import datetime

from colorama import Style, init

# Initialize colorama for cross-platform colored terminal output
init(autoreset=True)


class TimestampPrinter:
    """Handles printing with optional timestamps and colors."""

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
    def print(message, color=None):
        """Print a message with optional timestamp prefix and color.

        Args:
            message: The message to print
            color: Optional color code from colorama.Fore (e.g., Fore.GREEN, Fore.RED)
                   If None, uses default terminal color
        """
        # Construct the message with timestamp if enabled
        if TimestampPrinter._enable_timestamp:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            output = f"[{timestamp}] {message}"
        else:
            output = message

        # Apply color if specified
        if color:
            print(f"{color}{output}{Style.RESET_ALL}")
        else:
            print(output)

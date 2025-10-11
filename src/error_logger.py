#!/usr/bin/env python3
"""
Error logger for File Watcher
Handles logging of exceptions and errors to a specified error log file with timestamps and stack traces.
"""

import sys
import traceback
from datetime import datetime


class ErrorLogger:
    """Handles error logging with timestamps and stack traces."""

    @staticmethod
    def log_error(error_log_file, message, exception=None):
        """Log an error message with timestamp and optional stack trace to error log file.

        Args:
            error_log_file: Path to the error log file (can be None to skip logging)
            message: Error message to log
            exception: Optional exception object to include stack trace
        """
        if not error_log_file:
            return

        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open(error_log_file, "a") as f:
                f.write(f"[{timestamp}] ERROR: {message}\n")

                if exception:
                    # Write exception details
                    f.write(f"Exception type: {type(exception).__name__}\n")
                    f.write(f"Exception message: {str(exception)}\n")

                    # Write stack trace
                    f.write("Stack trace:\n")
                    tb_lines = traceback.format_exception(type(exception), exception, exception.__traceback__)
                    for line in tb_lines:
                        f.write(f"  {line}")

                f.write("\n")
        except Exception as e:
            # If we can't write to error log, print to stderr
            print(f"Warning: Failed to write to error log file '{error_log_file}': {e}", file=sys.stderr)

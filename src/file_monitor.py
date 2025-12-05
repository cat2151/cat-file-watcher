#!/usr/bin/env python3
"""
File monitoring logic for File Watcher
"""

import os
import time

from colorama import Fore

# Support both relative and absolute imports
try:
    from .command_executor import CommandExecutor
    from .config_loader import ConfigLoader
    from .error_logger import ErrorLogger
    from .time_period_checker import TimePeriodChecker
    from .timestamp_printer import TimestampPrinter
except ImportError:
    from command_executor import CommandExecutor
    from config_loader import ConfigLoader
    from error_logger import ErrorLogger
    from time_period_checker import TimePeriodChecker
    from timestamp_printer import TimestampPrinter


class FileMonitor:
    """Handles file monitoring and change detection logic."""

    @staticmethod
    def get_file_timestamp(filepath):
        """Get the modification timestamp of a file.

        Args:
            filepath: Path to the file

        Returns:
            float: Timestamp or None if file is not accessible
        """
        try:
            return os.path.getmtime(filepath)
        except OSError:
            return None

    @staticmethod
    def check_files(config, file_timestamps, file_last_check):
        """Check all files for timestamp changes and execute commands if needed.

        Args:
            config: Configuration dictionary
            file_timestamps: Dictionary tracking file timestamps
            file_last_check: Dictionary tracking last check time per file

        Returns:
            tuple: Updated (file_timestamps, file_last_check) dictionaries
        """
        if "files" not in config:
            TimestampPrinter.print("Warning: No 'files' section found in configuration.", Fore.YELLOW)
            return file_timestamps, file_last_check

        error_log_file = config.get("error_log_file")
        current_time = time.time()
        files_config = config["files"]

        for index, entry in enumerate(files_config):
            filename = entry.get("path", "")
            settings = entry
            entry_key = f"#{index}"

            try:
                # Validate and check if entry should be processed
                if not FileMonitor._should_process_entry(filename, settings, error_log_file):
                    continue

                # Check time period
                if not TimePeriodChecker.should_monitor_file(config, settings):
                    continue

                # Check interval timing
                interval = ConfigLoader.get_interval_for_file(config, settings)
                if entry_key in file_last_check:
                    if current_time - file_last_check[entry_key] < interval:
                        continue

                file_last_check[entry_key] = current_time

                # Process the entry
                file_timestamps = FileMonitor._process_entry(filename, settings, entry_key, config, file_timestamps)

            except Exception as e:
                error_msg = f"Error processing file '{filename}'"
                TimestampPrinter.print(f"{error_msg}: {e}", Fore.RED)
                ErrorLogger.log_error(error_log_file, error_msg, e)
                continue

        return file_timestamps, file_last_check

    @staticmethod
    def _should_process_entry(filename, settings, error_log_file):
        """Validate and check if entry should be processed.

        Args:
            filename: File path
            settings: Entry settings
            error_log_file: Error log file path

        Returns:
            bool: True if entry should be processed
        """
        # Validate terminate_if_process configuration
        if "terminate_if_process" in settings:
            if filename != "":
                error_msg = f"Fatal configuration error: terminate_if_process can only be used with empty filename, but filename is '{filename}'"
                TimestampPrinter.print(error_msg, Fore.RED)
                ErrorLogger.log_error(error_log_file, error_msg)
                return False

            if "command" in settings and settings["command"]:
                error_msg = "Fatal configuration error: terminate_if_process cannot be used with command field (command must be empty)"
                TimestampPrinter.print(error_msg, Fore.RED)
                ErrorLogger.log_error(error_log_file, error_msg)
                return False

        # Validate terminate_if_window_title configuration
        if "terminate_if_window_title" in settings:
            if filename != "":
                error_msg = f"Fatal configuration error: terminate_if_window_title can only be used with empty filename, but filename is '{filename}'"
                TimestampPrinter.print(error_msg, Fore.RED)
                ErrorLogger.log_error(error_log_file, error_msg)
                return False

            if "command" in settings and settings["command"]:
                error_msg = "Fatal configuration error: terminate_if_window_title cannot be used with command field (command must be empty)"
                TimestampPrinter.print(error_msg, Fore.RED)
                ErrorLogger.log_error(error_log_file, error_msg)
                return False

        # Check if command is specified
        if (
            "command" not in settings
            and "terminate_if_process" not in settings
            and "terminate_if_window_title" not in settings
        ):
            TimestampPrinter.print(f"Warning: No command specified for file '{filename}'", Fore.YELLOW)
            return False

        return True

    @staticmethod
    def _process_entry(filename, settings, entry_key, config, file_timestamps):
        """Process a single file entry.

        Args:
            filename: File path
            settings: Entry settings
            entry_key: Unique key for tracking
            config: Configuration dictionary
            file_timestamps: Dictionary tracking file timestamps

        Returns:
            dict: Updated file_timestamps dictionary
        """
        # Handle empty filename (periodic tasks)
        if filename == "":
            command = settings.get("command", "")
            CommandExecutor.execute_command(command, filename, settings, config)
            return file_timestamps

        # Get current timestamp
        current_timestamp = FileMonitor.get_file_timestamp(filename)

        if current_timestamp is None:
            if entry_key in file_timestamps:
                TimestampPrinter.print(f"Warning: File '{filename}' is no longer accessible", Fore.YELLOW)
                del file_timestamps[entry_key]
            return file_timestamps

        # Check if first time seeing this file
        if entry_key not in file_timestamps:
            file_timestamps[entry_key] = current_timestamp
            TimestampPrinter.print(f"Started monitoring '{filename}'", Fore.GREEN)
        # Check if timestamp changed
        elif current_timestamp != file_timestamps[entry_key]:
            TimestampPrinter.print(f"Detected change in '{filename}'")
            CommandExecutor.execute_command(settings["command"], filename, settings, config)
            file_timestamps[entry_key] = current_timestamp

        return file_timestamps

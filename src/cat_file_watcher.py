#!/usr/bin/env python3
"""
File Watcher - Monitor files and execute commands on timestamp changes
"""

import os
import time

# Support both relative and absolute imports
try:
    from .command_executor import CommandExecutor
    from .config_loader import ConfigLoader
    from .error_logger import ErrorLogger
    from .interval_parser import IntervalParser
    from .process_detector import ProcessDetector
    from .time_period_checker import TimePeriodChecker
    from .timestamp_printer import TimestampPrinter
except ImportError:
    from command_executor import CommandExecutor
    from config_loader import ConfigLoader
    from error_logger import ErrorLogger
    from interval_parser import IntervalParser
    from process_detector import ProcessDetector
    from time_period_checker import TimePeriodChecker
    from timestamp_printer import TimestampPrinter


class FileWatcher:
    """Monitors files and executes commands when timestamps change."""

    def __init__(self, config_path):
        """Initialize the file watcher with a configuration file."""
        self.config_path = config_path
        self.config = ConfigLoader.load_config(config_path)
        self.file_timestamps = {}
        self.file_last_check = {}
        self.config_last_check = 0
        self.config_timestamp = self._get_file_timestamp(config_path)

        # Configure timestamp display from config (default: True)
        enable_timestamp = self.config.get("enable_timestamp", True)
        TimestampPrinter.set_enable_timestamp(enable_timestamp)

    def _get_file_timestamp(self, filepath):
        """Get the modification timestamp of a file."""
        try:
            return os.path.getmtime(filepath)
        except OSError:
            return None

    def _get_interval_for_file(self, settings):
        """Get the interval for a file in seconds (backward compatibility)."""
        return ConfigLoader.get_interval_for_file(self.config, settings)

    def _is_process_running(self, process_pattern):
        """Check if a process is running (backward compatibility)."""
        return ProcessDetector.is_process_running(process_pattern)

    def _calculate_main_loop_interval(self):
        """Calculate the main loop interval from config settings.

        Returns the minimum interval to ensure adequate polling granularity
        for all configured checks (default_interval, config_check_interval,
        and all per-file intervals).

        Returns:
            float: Interval in seconds
        """
        intervals = []

        # Add default_interval (supports both old format and new format)
        default_interval = self.config.get("default_interval", "1s")
        intervals.append(IntervalParser.parse_interval(default_interval))

        # Add config_check_interval (supports both old format and new format)
        config_check_interval = self.config.get("config_check_interval", "1s")
        intervals.append(IntervalParser.parse_interval(config_check_interval))

        # Add all per-file intervals
        if "files" in self.config:
            for filename, settings in self.config["files"].items():
                if "interval" in settings:
                    file_interval = settings["interval"]
                    intervals.append(IntervalParser.parse_interval(file_interval))

        # Return the minimum interval to ensure we poll frequently enough
        return min(intervals)

    def _check_config_file(self):
        """Check if config file has been modified and reload if needed."""
        current_time = time.time()

        # Get config check interval (supports both old and new format), default to "1s"
        config_check_interval_value = self.config.get("config_check_interval", "1s")
        config_check_interval = IntervalParser.parse_interval(config_check_interval_value)

        # Check if enough time has passed since last check
        if current_time - self.config_last_check < config_check_interval:
            return

        self.config_last_check = current_time
        current_timestamp = self._get_file_timestamp(self.config_path)

        if current_timestamp is None:
            TimestampPrinter.print(f"Warning: Config file '{self.config_path}' is no longer accessible")
            return

        # Check if the config file has been modified
        if current_timestamp != self.config_timestamp:
            TimestampPrinter.print(f"Detected change in config file '{self.config_path}', reloading...")
            error_log_file = self.config.get("error_log_file")
            try:
                new_config = ConfigLoader.load_config(self.config_path)
                self.config = new_config
                self.config_timestamp = current_timestamp
                TimestampPrinter.print("Config reloaded successfully")
            except SystemExit as e:
                error_msg = f"Fatal error reloading config file '{self.config_path}'"
                TimestampPrinter.print(f"Error reloading config: {e}")
                ErrorLogger.log_error(error_log_file, error_msg, e)
                TimestampPrinter.print("Continuing with previous config")
            except Exception as e:
                error_msg = f"Error reloading config file '{self.config_path}'"
                TimestampPrinter.print(f"Error reloading config: {e}")
                ErrorLogger.log_error(error_log_file, error_msg, e)
                TimestampPrinter.print("Continuing with previous config")

    def _check_files(self):
        """Check all files for timestamp changes and execute commands if needed."""
        if "files" not in self.config:
            TimestampPrinter.print("Warning: No 'files' section found in configuration.")
            return

        error_log_file = self.config.get("error_log_file")
        current_time = time.time()
        files_config = self.config["files"]
        for filename, settings in files_config.items():
            if "command" not in settings:
                TimestampPrinter.print(f"Warning: No command specified for file '{filename}'")
                continue

            try:
                # Check if file should be monitored based on time period
                if not TimePeriodChecker.should_monitor_file(self.config, settings):
                    # Skip monitoring this file - outside time period
                    continue

                interval = ConfigLoader.get_interval_for_file(self.config, settings)

                # Check if enough time has passed since last check
                if filename in self.file_last_check:
                    if current_time - self.file_last_check[filename] < interval:
                        continue

                self.file_last_check[filename] = current_time

                # Special case: empty filename means execute command without file monitoring
                # This is useful for process health monitoring or periodic tasks
                if filename == "":
                    CommandExecutor.execute_command(settings["command"], filename, settings, self.config)
                    continue

                current_timestamp = self._get_file_timestamp(filename)

                if current_timestamp is None:
                    if filename in self.file_timestamps:
                        TimestampPrinter.print(f"Warning: File '{filename}' is no longer accessible")
                        del self.file_timestamps[filename]
                    continue

                # Check if this is the first time we're seeing this file
                if filename not in self.file_timestamps:
                    self.file_timestamps[filename] = current_timestamp
                    TimestampPrinter.print(f"Started monitoring '{filename}'")
                # Check if the timestamp has changed
                elif current_timestamp != self.file_timestamps[filename]:
                    TimestampPrinter.print(f"Detected change in '{filename}'")
                    CommandExecutor.execute_command(settings["command"], filename, settings, self.config)
                    self.file_timestamps[filename] = current_timestamp
            except Exception as e:
                error_msg = f"Error processing file '{filename}'"
                TimestampPrinter.print(f"{error_msg}: {e}")
                ErrorLogger.log_error(error_log_file, error_msg, e)
                # Continue processing other files despite error
                continue

    def run(self, interval=None):
        """Run the file watcher with the specified check interval (in seconds).

        Args:
            interval: Optional interval in seconds. If not specified, calculates the
                     minimum interval from config settings to ensure adequate polling
                     granularity for all configured checks.
        """
        # If interval not specified, calculate from config
        if interval is None:
            interval = self._calculate_main_loop_interval()

        TimestampPrinter.print(f"Starting file watcher with config: {self.config_path}")
        TimestampPrinter.print(f"Checking for changes every {interval} second(s)...")
        TimestampPrinter.print("Press Ctrl+C to stop.")

        try:
            while True:
                self._check_config_file()
                self._check_files()
                time.sleep(interval)
        except KeyboardInterrupt:
            TimestampPrinter.print("\nStopping file watcher...")

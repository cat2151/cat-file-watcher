#!/usr/bin/env python3
"""
File Watcher - Monitor files and execute commands on timestamp changes
"""

import os
import time

from colorama import Fore

# Support both relative and absolute imports
try:
    from .config_loader import ConfigLoader
    from .error_logger import ErrorLogger
    from .file_monitor import FileMonitor
    from .interval_parser import IntervalParser
    from .process_detector import ProcessDetector
    from .timestamp_printer import TimestampPrinter
except ImportError:
    from config_loader import ConfigLoader
    from error_logger import ErrorLogger
    from file_monitor import FileMonitor
    from interval_parser import IntervalParser
    from process_detector import ProcessDetector
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

        # Track external files and their timestamps
        self.external_file_paths = []
        self.external_file_timestamps = {}
        self._update_external_file_tracking()

        # Configure timestamp display from config (default: True)
        enable_timestamp = self.config.get("enable_timestamp", True)
        TimestampPrinter.set_enable_timestamp(enable_timestamp)

    def _get_file_timestamp(self, filepath):
        """Get the modification timestamp of a file (backward compatibility)."""
        return FileMonitor.get_file_timestamp(filepath)

    def _get_interval_for_file(self, settings):
        """Get the interval for a file in seconds (backward compatibility)."""
        return ConfigLoader.get_interval_for_file(self.config, settings)

    def _is_process_running(self, process_pattern):
        """Check if a process is running (backward compatibility)."""
        return ProcessDetector.is_process_running(process_pattern)

    def _resolve_external_file_paths(self):
        """Resolve external file paths from config to absolute paths.

        Returns:
            list: List of absolute paths to external files
        """
        external_files = self.config.get("external_files", [])
        if not isinstance(external_files, list):
            return []

        # Get directory of main config file for resolving relative paths
        main_config_dir = os.path.dirname(os.path.abspath(self.config_path))

        resolved_paths = []
        for external_file in external_files:
            # Resolve relative paths relative to main config file
            if not os.path.isabs(external_file):
                external_file = os.path.join(main_config_dir, external_file)
            resolved_paths.append(external_file)

        return resolved_paths

    def _update_external_file_tracking(self):
        """Update the tracking of external files and their timestamps."""
        self.external_file_paths = self._resolve_external_file_paths()

        # Initialize or update timestamps for all external files
        new_timestamps = {}
        for filepath in self.external_file_paths:
            timestamp = self._get_file_timestamp(filepath)
            new_timestamps[filepath] = timestamp

        self.external_file_timestamps = new_timestamps

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
            for entry in self.config["files"]:
                if "interval" in entry:
                    file_interval = entry["interval"]
                    intervals.append(IntervalParser.parse_interval(file_interval))

        # Add all per-command intervals (from commands section before merging)
        if "commands" in self.config:
            for entry in self.config["commands"]:
                if "interval" in entry:
                    command_interval = entry["interval"]
                    intervals.append(IntervalParser.parse_interval(command_interval))

        # Add all per-process intervals (from processes section before merging)
        if "processes" in self.config:
            for entry in self.config["processes"]:
                if "interval" in entry:
                    process_interval = entry["interval"]
                    intervals.append(IntervalParser.parse_interval(process_interval))

        # Return the minimum interval to ensure we poll frequently enough
        return min(intervals)

    def _check_config_file(self):
        """Check if config file or external files have been modified and reload if needed."""
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
            TimestampPrinter.print(f"Warning: Config file '{self.config_path}' is no longer accessible", Fore.YELLOW)
            return

        config_changed = False
        changed_file = None

        # Check if the main config file has been modified
        if current_timestamp != self.config_timestamp:
            config_changed = True
            changed_file = self.config_path

        # Check if any external files have been modified
        if not config_changed:
            for filepath in self.external_file_paths:
                current_external_timestamp = self._get_file_timestamp(filepath)

                if current_external_timestamp is None:
                    TimestampPrinter.print(f"Warning: External file '{filepath}' is no longer accessible", Fore.YELLOW)
                    continue

                previous_timestamp = self.external_file_timestamps.get(filepath)
                if current_external_timestamp != previous_timestamp:
                    config_changed = True
                    changed_file = filepath
                    break

        # If any config file changed, reload the entire config
        if config_changed:
            TimestampPrinter.print(f"Detected change in config file '{changed_file}', reloading...", Fore.GREEN)
            error_log_file = self.config.get("error_log_file")
            try:
                new_config = ConfigLoader.load_config(self.config_path)
                self.config = new_config
                self.config_timestamp = self._get_file_timestamp(self.config_path)
                # Update external file tracking after reload (list may have changed)
                self._update_external_file_tracking()
                TimestampPrinter.print("Config reloaded successfully", Fore.GREEN)
            except SystemExit as e:
                error_msg = f"Fatal error reloading config file '{changed_file}'"
                TimestampPrinter.print(f"Error reloading config: {e}", Fore.RED)
                ErrorLogger.log_error(error_log_file, error_msg, e)
                TimestampPrinter.print("Continuing with previous config", Fore.YELLOW)
            except Exception as e:
                error_msg = f"Error reloading config file '{changed_file}'"
                TimestampPrinter.print(f"Error reloading config: {e}", Fore.RED)
                ErrorLogger.log_error(error_log_file, error_msg, e)
                TimestampPrinter.print("Continuing with previous config", Fore.YELLOW)

    def _check_files(self):
        """Check all files for timestamp changes and execute commands if needed."""
        self.file_timestamps, self.file_last_check = FileMonitor.check_files(
            self.config, self.file_timestamps, self.file_last_check
        )

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

        TimestampPrinter.print(f"Starting file watcher with config: {self.config_path}", Fore.GREEN)
        TimestampPrinter.print(f"Checking for changes every {interval} second(s)...")
        TimestampPrinter.print("Press Ctrl+C to stop.")

        try:
            while True:
                self._check_config_file()
                self._check_files()
                time.sleep(interval)
        except KeyboardInterrupt:
            TimestampPrinter.print("\nStopping file watcher...")

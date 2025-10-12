#!/usr/bin/env python3
"""
Command executor for File Watcher
"""

import subprocess
from datetime import datetime

from colorama import Fore, Style

# Support both relative and absolute imports
try:
    from .error_logger import ErrorLogger
    from .process_detector import ProcessDetector
    from .timestamp_printer import TimestampPrinter
except ImportError:
    from error_logger import ErrorLogger
    from process_detector import ProcessDetector
    from timestamp_printer import TimestampPrinter


class CommandExecutor:
    """Handles execution of shell commands with process suppression support."""

    @staticmethod
    def execute_command(command, filepath, settings, config=None):
        """Execute a shell command if the conditions are met.

        Args:
            command: The shell command to execute
            filepath: The path to the file that changed
            settings: Dictionary containing file-specific settings including optional 'suppress_if_process', 'enable_log'
            config: Optional global configuration dictionary containing 'log_file'
        """
        # Check if command execution should be suppressed based on running processes
        if "suppress_if_process" in settings:
            process_pattern = settings["suppress_if_process"]
            matched_process = ProcessDetector.get_matching_process(process_pattern)
            if matched_process:
                TimestampPrinter.print(f"Skipping command for '{filepath}': process matching '{process_pattern}' is running", Style.DIM)
                # Write to suppression log file if configured
                if config and config.get("suppression_log_file"):
                    CommandExecutor._write_to_suppression_log(filepath, process_pattern, matched_process, config)
                return

        TimestampPrinter.print(f"Executing command for '{filepath}': {command}", Fore.GREEN)

        # Write to log file if enabled
        if settings.get("enable_log", False) and config and config.get("log_file"):
            CommandExecutor._write_to_log(filepath, settings, config)

        error_log_file = config.get("error_log_file") if config else None

        # Get cwd setting if specified
        cwd = settings.get("cwd")

        try:
            # Use capture_output=False to allow real-time output for long-running commands
            result = subprocess.run(command, shell=True, capture_output=False, text=True, timeout=30, cwd=cwd)
            if result.returncode != 0:
                error_msg = f"Command failed for '{filepath}' with exit code {result.returncode}"
                TimestampPrinter.print(f"Error: {error_msg}", Fore.RED)
                # Log command execution error (without stderr since we're not capturing it)
                if error_log_file:
                    ErrorLogger.log_error(
                        error_log_file, f"{error_msg}\nCommand: {command}"
                    )
        except subprocess.TimeoutExpired as e:
            error_msg = f"Command timed out after 30 seconds for '{filepath}'"
            TimestampPrinter.print(f"Error: {error_msg}", Fore.RED)
            ErrorLogger.log_error(error_log_file, error_msg, e)
            raise
        except Exception as e:
            error_msg = f"Error executing command for '{filepath}'"
            TimestampPrinter.print(f"{error_msg}: {e}", Fore.RED)
            ErrorLogger.log_error(error_log_file, error_msg, e)
            raise

    @staticmethod
    def _write_to_log(filepath, settings, config):
        """Write command execution information to log file.

        Args:
            filepath: The path to the file that changed
            settings: Dictionary containing file-specific settings
            config: Global configuration dictionary containing 'log_file'
        """
        error_log_file = config.get("error_log_file") if config else None
        try:
            log_file = config.get("log_file")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open(log_file, "a") as f:
                f.write(f"[{timestamp}] File: {filepath}\n")
                for key, value in settings.items():
                    f.write(f"  {key}: {value}\n")
                f.write("\n")
        except Exception as e:
            error_msg = f"Failed to write to log file for '{filepath}'"
            TimestampPrinter.print(f"Warning: {error_msg}: {e}", Fore.YELLOW)
            ErrorLogger.log_error(error_log_file, error_msg, e)

    @staticmethod
    def _write_to_suppression_log(filepath, process_pattern, matched_process, config):
        """Write command suppression information to suppression log file.

        Args:
            filepath: The path to the file that changed
            process_pattern: The regex pattern used to match processes
            matched_process: The actual process name that matched
            config: Global configuration dictionary containing 'suppression_log_file'
        """
        error_log_file = config.get("error_log_file") if config else None
        try:
            suppression_log_file = config.get("suppression_log_file")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open(suppression_log_file, "a") as f:
                f.write(f"[{timestamp}] File: {filepath}\n")
                f.write(f"  Process pattern: {process_pattern}\n")
                f.write(f"  Matched process: {matched_process}\n")
                f.write("\n")
        except Exception as e:
            error_msg = f"Failed to write to suppression log file for '{filepath}'"
            TimestampPrinter.print(f"Warning: {error_msg}: {e}", Fore.YELLOW)
            ErrorLogger.log_error(error_log_file, error_msg, e)

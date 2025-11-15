#!/usr/bin/env python3
"""
Command executor for File Watcher
"""

import shlex
import subprocess
import sys
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
            settings: Dictionary containing file-specific settings including optional 'suppress_if_process', 'enable_log', 'terminate_if_process'
            config: Optional global configuration dictionary containing 'log_file'
        """
        # Handle terminate_if_process feature
        if "terminate_if_process" in settings:
            CommandExecutor._handle_process_termination(settings, config)
            return

        # Check if command execution should be suppressed based on running processes
        if CommandExecutor._check_process_suppression(filepath, settings, config):
            return

        # Execute the command
        CommandExecutor._execute_shell_command(command, filepath, settings, config)

    @staticmethod
    def _check_process_suppression(filepath, settings, config):
        """Check if command execution should be suppressed based on running processes.

        Args:
            filepath: The path to the file that changed
            settings: Dictionary containing file-specific settings
            config: Optional global configuration dictionary

        Returns:
            bool: True if command should be suppressed, False otherwise
        """
        if "suppress_if_process" not in settings:
            return False

        process_pattern = settings["suppress_if_process"]
        matched_process = ProcessDetector.get_matching_process(process_pattern)
        if matched_process:
            # For empty filename, show the command being skipped instead
            if filepath == "":
                command = settings.get("command", "")
                TimestampPrinter.print(
                    f"Skipping command '{command}': process matching '{process_pattern}' is running", Style.DIM
                )
            else:
                TimestampPrinter.print(
                    f"Skipping command for '{filepath}': process matching '{process_pattern}' is running", Style.DIM
                )
            # Write to suppression log file if configured
            if config and config.get("suppression_log_file"):
                CommandExecutor._write_to_suppression_log(filepath, process_pattern, matched_process, config, settings)
            return True

        return False

    @staticmethod
    def _execute_shell_command(command, filepath, settings, config):
        """Execute a shell command and handle the result.

        Args:
            command: The shell command to execute
            filepath: The path to the file that changed
            settings: Dictionary containing file-specific settings
            config: Optional global configuration dictionary
        """
        # Color only the command part in green for emphasis
        # For empty filename, show the command directly instead of "for ''"
        if filepath == "":
            message = f"Executing command: {Fore.GREEN}{command}{Style.RESET_ALL}"
        else:
            message = f"Executing command for '{filepath}': {Fore.GREEN}{command}{Style.RESET_ALL}"
        TimestampPrinter.print(message)

        # Write to log file if enabled
        if settings.get("enable_log", False) and config and config.get("log_file"):
            CommandExecutor._write_to_log(filepath, settings, config)

        error_log_file = config.get("error_log_file") if config else None
        cwd = settings.get("cwd")
        no_focus = settings.get("no_focus", False)

        try:
            # Use capture_output=False to allow real-time output for long-running commands
            if no_focus:
                # When no_focus is enabled, prevent focus stealing with platform-specific mechanisms
                result = CommandExecutor._run_no_focus_command(command, cwd)
            else:
                # Default behavior: use shell=True
                result = subprocess.run(command, shell=True, capture_output=False, text=True, timeout=30, cwd=cwd)
            CommandExecutor._handle_command_result(result, command, filepath, error_log_file)
        except subprocess.TimeoutExpired as e:
            if filepath == "":
                error_msg = f"Command timed out after 30 seconds: {command}"
            else:
                error_msg = f"Command timed out after 30 seconds for '{filepath}'"
            TimestampPrinter.print(f"Error: {error_msg}", Fore.RED)
            ErrorLogger.log_error(error_log_file, error_msg, e)
            raise
        except Exception as e:
            if filepath == "":
                error_msg = f"Error executing command: {command}"
            else:
                error_msg = f"Error executing command for '{filepath}'"
            TimestampPrinter.print(f"{error_msg}: {e}", Fore.RED)
            ErrorLogger.log_error(error_log_file, error_msg, e)
            raise

    @staticmethod
    def _run_no_focus_command(command, cwd):
        """Run a command without stealing focus (Windows only, asynchronous).

        This method launches the command asynchronously and does not wait for it to complete.
        The window will be shown but will not steal focus from the current foreground window.

        Args:
            command: The shell command to execute
            cwd: Working directory for the command

        Returns:
            subprocess.CompletedProcess: A mock result object with returncode 0
        """
        if sys.platform != "win32":
            # no_focus is only supported on Windows
            TimestampPrinter.print(
                "Warning: no_focus is only supported on Windows. Falling back to normal execution.", Fore.YELLOW
            )
            # Fallback to normal execution
            result = subprocess.run(command, shell=True, capture_output=False, text=True, timeout=30, cwd=cwd)
            return result

        # Use shlex.split for proper argument parsing (handles quotes, escapes, etc.)
        command_args = shlex.split(command)

        # Windows-specific: Show window without stealing focus
        # SW_SHOWNOACTIVATE (4) shows the window without activating it
        SW_SHOWNOACTIVATE = 4

        # Configure startupinfo to show window without focus
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = SW_SHOWNOACTIVATE

        # Launch asynchronously - don't wait for the process to complete
        subprocess.Popen(
            command_args,
            shell=False,
            cwd=cwd,
            startupinfo=startupinfo,
        )

        # Return a mock CompletedProcess object since we're not waiting
        # This maintains compatibility with the existing code structure
        class MockResult:
            returncode = 0

        return MockResult()

    @staticmethod
    def _handle_command_result(result, command, filepath, error_log_file):
        """Handle the result of a command execution.

        Args:
            result: subprocess.CompletedProcess result object
            command: The shell command that was executed
            filepath: The path to the file that changed
            error_log_file: Path to error log file (optional)
        """
        if result.returncode != 0:
            if filepath == "":
                error_msg = f"Command failed with exit code {result.returncode}: {command}"
            else:
                error_msg = f"Command failed for '{filepath}' with exit code {result.returncode}"
            TimestampPrinter.print(f"Error: {error_msg}", Fore.RED)
            # Log command execution error (without stderr since we're not capturing it)
            if error_log_file:
                ErrorLogger.log_error(error_log_file, f"{error_msg}\nCommand: {command}")

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
    def _write_to_suppression_log(filepath, process_pattern, matched_process, config, settings=None):
        """Write command suppression information to suppression log file.

        Args:
            filepath: The path to the file that changed
            process_pattern: The regex pattern used to match processes
            matched_process: The actual process name that matched
            config: Global configuration dictionary containing 'suppression_log_file'
            settings: Dictionary containing file-specific settings (optional)
        """
        error_log_file = config.get("error_log_file") if config else None
        try:
            suppression_log_file = config.get("suppression_log_file")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open(suppression_log_file, "a") as f:
                f.write(f"[{timestamp}] File: {filepath}\n")
                f.write(f"  Process pattern: {process_pattern}\n")
                f.write(f"  Matched process: {matched_process}\n")
                # Write all settings if provided
                if settings:
                    for key, value in settings.items():
                        f.write(f"  {key}: {value}\n")
                f.write("\n")
        except Exception as e:
            error_msg = f"Failed to write to suppression log file for '{filepath}'"
            TimestampPrinter.print(f"Warning: {error_msg}: {e}", Fore.YELLOW)
            ErrorLogger.log_error(error_log_file, error_msg, e)

    @staticmethod
    def _handle_process_termination(settings, config):
        """Handle process termination based on terminate_if_process setting.

        Args:
            settings: Dictionary containing 'terminate_if_process' regex pattern(s) - can be a string or list of strings
            config: Optional global configuration dictionary
        """
        process_patterns = settings["terminate_if_process"]
        error_log_file = config.get("error_log_file") if config else None

        # Normalize to list if a single string is provided
        if isinstance(process_patterns, str):
            process_patterns = [process_patterns]

        # Process each pattern independently with safety check
        for pattern in process_patterns:
            matched_processes = ProcessDetector.get_all_matching_processes(pattern)
            CommandExecutor._process_matched_processes(pattern, matched_processes, error_log_file)

    @staticmethod
    def _process_matched_processes(pattern, matched_processes, error_log_file):
        """Process the matched processes for a given pattern.

        Args:
            pattern: The regex pattern used to match processes
            matched_processes: List of (pid, process_name) tuples
            error_log_file: Path to error log file (optional)
        """
        if len(matched_processes) == 0:
            # No processes found - this is normal, no action needed
            return

        if len(matched_processes) == 1:
            # Exactly one process found - terminate it
            CommandExecutor._terminate_single_process(pattern, matched_processes[0], error_log_file)
        else:
            # Multiple processes found - safety check, don't terminate
            CommandExecutor._handle_multiple_matches(pattern, matched_processes, error_log_file)

    @staticmethod
    def _terminate_single_process(pattern, process_info, error_log_file):
        """Terminate a single matched process.

        Args:
            pattern: The regex pattern that matched this process
            process_info: Tuple of (pid, process_name)
            error_log_file: Path to error log file (optional)
        """
        pid, process_name = process_info
        msg = f"Terminating process (PID: {pid}, Name: {process_name}) matching pattern '{pattern}'"
        TimestampPrinter.print(msg, Fore.GREEN)

        success = ProcessDetector.terminate_process(pid)
        if success:
            success_msg = f"Successfully sent terminate signal to process {pid}"
            TimestampPrinter.print(success_msg, Fore.GREEN)
        else:
            error_msg = f"Failed to terminate process {pid}"
            TimestampPrinter.print(error_msg, Fore.RED)
            ErrorLogger.log_error(error_log_file, error_msg)

    @staticmethod
    def _handle_multiple_matches(pattern, matched_processes, error_log_file):
        """Handle the case when multiple processes match a pattern.

        Args:
            pattern: The regex pattern that matched multiple processes
            matched_processes: List of (pid, process_name) tuples
            error_log_file: Path to error log file (optional)
        """
        warning_msg = f"Warning: Found {len(matched_processes)} processes matching pattern '{pattern}'. Not terminating for safety."
        TimestampPrinter.print(warning_msg, Fore.YELLOW)
        ErrorLogger.log_error(error_log_file, warning_msg)

        # Log details of matched processes
        for pid, process_name in matched_processes:
            detail_msg = f"  - PID: {pid}, Name: {process_name}"
            TimestampPrinter.print(detail_msg, Fore.YELLOW)
            ErrorLogger.log_error(error_log_file, detail_msg)

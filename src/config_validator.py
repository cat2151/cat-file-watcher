#!/usr/bin/env python3
"""
Configuration validation for File Watcher
"""

import sys

from colorama import Fore

# Support both relative and absolute imports
try:
    from .error_logger import ErrorLogger
    from .timestamp_printer import TimestampPrinter
except ImportError:
    from error_logger import ErrorLogger
    from timestamp_printer import TimestampPrinter


class ConfigValidator:
    """Handles validation of TOML configuration sections."""

    @staticmethod
    def validate_files_format(config, error_log_file):
        """Validate that files section uses the correct format.

        Args:
            config: Configuration dictionary to validate
            error_log_file: Error log file path for logging

        Raises:
            SystemExit: If files section format is invalid
        """
        if "files" not in config:
            return

        files_section = config["files"]

        # Files section must be a list (array of tables)
        if not isinstance(files_section, list):
            error_msg = "[files] section must use array of tables format: [[files]]\\nEach entry should have 'path' and 'command' fields"
            TimestampPrinter.print(f"Error: {error_msg}", Fore.RED)
            ErrorLogger.log_error(error_log_file, error_msg, None)
            sys.exit(1)

        # Validate each file entry
        for i, entry in enumerate(files_section):
            if not isinstance(entry, dict):
                error_msg = f"[files] entry #{i + 1} is not a valid table"
                TimestampPrinter.print(f"Error: {error_msg}", Fore.RED)
                ErrorLogger.log_error(error_log_file, error_msg, None)
                sys.exit(1)

            if "path" not in entry:
                error_msg = f"[files] entry #{i + 1} is missing required 'path' field"
                TimestampPrinter.print(f"Error: {error_msg}", Fore.RED)
                ErrorLogger.log_error(error_log_file, error_msg, None)
                sys.exit(1)

    @staticmethod
    def validate_commands_format(config, error_log_file):
        """Validate that commands section uses the correct format.

        Args:
            config: Configuration dictionary to validate
            error_log_file: Error log file path for logging

        Raises:
            SystemExit: If commands section format is invalid
        """
        if "commands" not in config:
            return

        commands_section = config["commands"]

        # Commands section must be a list (array of tables)
        if not isinstance(commands_section, list):
            error_msg = "[commands] section must use array of tables format: [[commands]]\\nEach entry should have 'command' field but NOT 'path' field"
            TimestampPrinter.print(f"Error: {error_msg}", Fore.RED)
            ErrorLogger.log_error(error_log_file, error_msg, None)
            sys.exit(1)

        # Validate each command entry
        for i, entry in enumerate(commands_section):
            if not isinstance(entry, dict):
                error_msg = f"[commands] entry #{i + 1} is not a valid table"
                TimestampPrinter.print(f"Error: {error_msg}", Fore.RED)
                ErrorLogger.log_error(error_log_file, error_msg, None)
                sys.exit(1)

            if "path" in entry:
                error_msg = (
                    f"[commands] entry #{i + 1} must NOT have 'path' field (path is forbidden in [[commands]] section)"
                )
                TimestampPrinter.print(f"Error: {error_msg}", Fore.RED)
                ErrorLogger.log_error(error_log_file, error_msg, None)
                sys.exit(1)

    @staticmethod
    def validate_processes_format(config, error_log_file):
        """Validate that processes section uses the correct format.

        Args:
            config: Configuration dictionary to validate
            error_log_file: Error log file path for logging

        Raises:
            SystemExit: If processes section format is invalid
        """
        if "processes" not in config:
            return

        processes_section = config["processes"]

        # Processes section must be a list (array of tables)
        if not isinstance(processes_section, list):
            error_msg = "[processes] section must use array of tables format: [[processes]]\\nEach entry should have process-related fields but NOT 'path' or 'command' fields"
            TimestampPrinter.print(f"Error: {error_msg}", Fore.RED)
            ErrorLogger.log_error(error_log_file, error_msg, None)
            sys.exit(1)

        # Validate each process entry
        for i, entry in enumerate(processes_section):
            if not isinstance(entry, dict):
                error_msg = f"[processes] entry #{i + 1} is not a valid table"
                TimestampPrinter.print(f"Error: {error_msg}", Fore.RED)
                ErrorLogger.log_error(error_log_file, error_msg, None)
                sys.exit(1)

            if "path" in entry:
                error_msg = f"[processes] entry #{i + 1} must NOT have 'path' field (path is forbidden in [[processes]] section)"
                TimestampPrinter.print(f"Error: {error_msg}", Fore.RED)
                ErrorLogger.log_error(error_log_file, error_msg, None)
                sys.exit(1)

            if "command" in entry:
                error_msg = f"[processes] entry #{i + 1} must NOT have 'command' field (command is forbidden in [[processes]] section)"
                TimestampPrinter.print(f"Error: {error_msg}", Fore.RED)
                ErrorLogger.log_error(error_log_file, error_msg, None)
                sys.exit(1)

    @staticmethod
    def validate_no_focus_commands(config, error_log_file):
        """Validate that no_focus entries use argv array instead of command.

        Args:
            config: Configuration dictionary to validate
            error_log_file: Error log file path for logging

        Raises:
            SystemExit: If no_focus entry has invalid configuration
        """
        if "files" not in config:
            return

        files_section = config["files"]

        # Files section must be a list (array of tables)
        if not isinstance(files_section, list):
            return

        # Validate each file entry
        for i, entry in enumerate(files_section):
            if not isinstance(entry, dict):
                continue

            # Check if no_focus is enabled
            if not entry.get("no_focus", False):
                continue

            # When no_focus=true, 'command' field must NOT be present
            if "command" in entry:
                error_msg = (
                    f"[files] entry #{i + 1}: no_focus=trueの場合、commandフィールドは使用できません。"
                    f"代わりにargvフィールド（配列）を使用してください。例: argv = ['notepad.exe', 'file.txt']"
                )
                TimestampPrinter.print(f"Error: {error_msg}", Fore.RED)
                ErrorLogger.log_error(error_log_file, error_msg, None)
                sys.exit(1)

            # When no_focus=true, 'argv' field MUST be present and must be an array
            if "argv" not in entry:
                error_msg = (
                    f"[files] entry #{i + 1}: no_focus=trueの場合、argvフィールド（配列）が必須です。"
                    f"例: argv = ['notepad.exe', 'file.txt']"
                )
                TimestampPrinter.print(f"Error: {error_msg}", Fore.RED)
                ErrorLogger.log_error(error_log_file, error_msg, None)
                sys.exit(1)

            # Validate that argv is an array
            argv = entry.get("argv")
            if not isinstance(argv, list):
                error_msg = f"[files] entry #{i + 1}: argvフィールドは配列でなければなりません。例: argv = ['notepad.exe', 'file.txt']"
                TimestampPrinter.print(f"Error: {error_msg}", Fore.RED)
                ErrorLogger.log_error(error_log_file, error_msg, None)
                sys.exit(1)

            # Validate that argv is not empty
            if len(argv) == 0:
                error_msg = (
                    f"[files] entry #{i + 1}: argvフィールドは空の配列にできません。少なくとも実行ファイル名が必要です"
                )
                TimestampPrinter.print(f"Error: {error_msg}", Fore.RED)
                ErrorLogger.log_error(error_log_file, error_msg, None)
                sys.exit(1)

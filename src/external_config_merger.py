#!/usr/bin/env python3
"""
External configuration file merger for File Watcher
"""

import os
import sys

import toml
from colorama import Fore

# Support both relative and absolute imports
try:
    from .config_validator import ConfigValidator
    from .error_logger import ErrorLogger
    from .timestamp_printer import TimestampPrinter
except ImportError:
    from config_validator import ConfigValidator
    from error_logger import ErrorLogger
    from timestamp_printer import TimestampPrinter


class ExternalConfigMerger:
    """Handles merging of external TOML configuration files."""

    @staticmethod
    def merge_sections(config, error_log_file):
        """Merge commands and processes sections into files section.

        Args:
            config: Configuration dictionary
            error_log_file: Error log file path for logging
        """
        # Initialize files section if it doesn't exist
        if "files" not in config:
            config["files"] = []

        # Merge commands section (add empty path to each entry)
        if "commands" in config:
            for entry in config["commands"]:
                # Add path="" to commands entries
                merged_entry = {"path": ""}
                merged_entry.update(entry)
                config["files"].append(merged_entry)

        # Merge processes section (add empty path to each entry)
        if "processes" in config:
            for entry in config["processes"]:
                # Add path="" to processes entries
                merged_entry = {"path": ""}
                merged_entry.update(entry)
                config["files"].append(merged_entry)

    @staticmethod
    def merge_external_files(config, main_config_path, error_log_file):
        """Merge files sections from external TOML files.

        Args:
            config: Main configuration dictionary to merge into
            main_config_path: Path to the main config file (for resolving relative paths)
            error_log_file: Error log file path for logging

        Raises:
            SystemExit: If external file is not found, cannot be parsed, or contains invalid sections
        """
        external_files = config.get("external_files", [])
        if not isinstance(external_files, list):
            error_msg = "external_files must be a list of file paths"
            TimestampPrinter.print(f"Error: {error_msg}", Fore.RED)
            ErrorLogger.log_error(error_log_file, error_msg, None)
            sys.exit(1)

        # Get directory of main config file for resolving relative paths
        main_config_dir = os.path.dirname(os.path.abspath(main_config_path))

        # Initialize files section if it doesn't exist
        if "files" not in config:
            config["files"] = []

        for external_file in external_files:
            # Resolve relative paths relative to main config file
            if not os.path.isabs(external_file):
                external_file = os.path.join(main_config_dir, external_file)

            try:
                with open(external_file, "r", encoding="utf-8") as f:
                    external_config = toml.load(f)

                # Validate that external file only contains 'files', 'commands', or 'processes' sections
                allowed_sections = {"files", "commands", "processes"}
                found_sections = set(external_config.keys())
                invalid_sections = found_sections - allowed_sections

                if invalid_sections:
                    error_msg = f"External file '{external_file}' contains invalid sections: {', '.join(invalid_sections)}. Only [files], [commands], and [processes] sections are allowed."
                    TimestampPrinter.print(f"Error: {error_msg}", Fore.RED)
                    ErrorLogger.log_error(error_log_file, error_msg, None)
                    sys.exit(1)

                # Validate external file format for each section
                ConfigValidator.validate_files_format(external_config, error_log_file)
                ConfigValidator.validate_commands_format(external_config, error_log_file)
                ConfigValidator.validate_processes_format(external_config, error_log_file)

                # Merge files section (extend the list)
                if "files" in external_config:
                    config["files"].extend(external_config["files"])

                # Merge commands section (extend the list)
                if "commands" in external_config:
                    if "commands" not in config:
                        config["commands"] = []
                    config["commands"].extend(external_config["commands"])

                # Merge processes section (extend the list)
                if "processes" in external_config:
                    if "processes" not in config:
                        config["processes"] = []
                    config["processes"].extend(external_config["processes"])

                if any(section in external_config for section in allowed_sections):
                    TimestampPrinter.print(f"Loaded external files from: {external_file}")

            except FileNotFoundError as e:
                error_msg = f"External configuration file '{external_file}' not found."
                TimestampPrinter.print(f"Error: {error_msg}", Fore.RED)
                ErrorLogger.log_error(error_log_file, error_msg, e)
                sys.exit(1)
            except toml.TomlDecodeError as e:
                error_msg = f"Failed to parse external TOML configuration '{external_file}': {e}"
                TimestampPrinter.print(f"Error: {error_msg}", Fore.RED)
                ErrorLogger.log_error(error_log_file, error_msg, e)
                sys.exit(1)
            except Exception as e:
                error_msg = f"Unexpected error loading external config file '{external_file}'"
                TimestampPrinter.print(f"Error: {error_msg}: {e}", Fore.RED)
                ErrorLogger.log_error(error_log_file, error_msg, e)
                sys.exit(1)

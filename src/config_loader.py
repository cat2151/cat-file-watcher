#!/usr/bin/env python3
"""
Configuration loader for File Watcher
"""

import sys

import toml
from colorama import Fore

# Support both relative and absolute imports
try:
    from .config_validator import ConfigValidator
    from .error_logger import ErrorLogger
    from .external_config_merger import ExternalConfigMerger
    from .interval_parser import IntervalParser
    from .timestamp_printer import TimestampPrinter
except ImportError:
    from config_validator import ConfigValidator
    from error_logger import ErrorLogger
    from external_config_merger import ExternalConfigMerger
    from interval_parser import IntervalParser
    from timestamp_printer import TimestampPrinter


class ConfigLoader:
    """Handles loading and parsing TOML configuration files."""

    @staticmethod
    def load_config(config_path):
        """Load and parse the TOML configuration file.

        Args:
            config_path: Path to the TOML configuration file

        Returns:
            dict: Parsed configuration

        Raises:
            SystemExit: If configuration file is not found or cannot be parsed
        """
        error_log_file = None
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = toml.load(f)
            # Get error_log_file from config if it exists
            error_log_file = config.get("error_log_file")

            # Validate files section format
            ConfigValidator.validate_files_format(config, error_log_file)

            # Validate commands section format
            ConfigValidator.validate_commands_format(config, error_log_file)

            # Validate processes section format
            ConfigValidator.validate_processes_format(config, error_log_file)

            # Load external files if specified
            if "external_files" in config:
                ExternalConfigMerger.merge_external_files(config, config_path, error_log_file)

            # Merge commands and processes sections into files
            ExternalConfigMerger.merge_sections(config, error_log_file)

            # Validate no_focus commands don't use 'start' (after merging)
            ConfigValidator.validate_no_focus_commands(config, error_log_file)

            return config
        except FileNotFoundError as e:
            error_msg = f"Configuration file '{config_path}' not found."
            TimestampPrinter.print(f"Error: {error_msg}", Fore.RED)
            ErrorLogger.log_error(error_log_file, error_msg, e)
            sys.exit(1)
        except toml.TomlDecodeError as e:
            error_msg = f"Failed to parse TOML configuration: {e}"
            TimestampPrinter.print(f"Error: {error_msg}", Fore.RED)
            ErrorLogger.log_error(error_log_file, error_msg, e)
            sys.exit(1)
        except Exception as e:
            error_msg = f"Unexpected error loading config file '{config_path}'"
            TimestampPrinter.print(f"Error: {error_msg}: {e}", Fore.RED)
            ErrorLogger.log_error(error_log_file, error_msg, e)
            sys.exit(1)

    @staticmethod
    def get_interval_for_file(config, settings):
        """Get the interval for a file in seconds.

        Supports time strings like "1s", "2m", "3h", "0.5s".

        Examples:
        - "1s" -> 1.0s, "2m" -> 120.0s, "0.5s" -> 0.5s

        Args:
            config: Global configuration dictionary
            settings: Dictionary containing file-specific settings, may include 'interval' key

        Returns:
            float: Interval in seconds
        """
        # Get default interval from config, default to "1s" (1 second)
        default_interval = config.get("default_interval", "1s")

        # Get file-specific interval, or use default
        interval_value = settings.get("interval", default_interval)

        # Parse interval using IntervalParser
        return IntervalParser.parse_interval(interval_value)

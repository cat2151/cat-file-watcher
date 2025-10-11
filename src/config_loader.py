#!/usr/bin/env python3
"""
Configuration loader for File Watcher
"""
import sys
import os
import toml

# Support both relative and absolute imports
try:
    from .error_logger import ErrorLogger
except ImportError:
    from error_logger import ErrorLogger


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
            with open(config_path, 'r') as f:
                config = toml.load(f)
            # Get error_log_file from config if it exists
            error_log_file = config.get('error_log_file')
            
            # Load external files if specified
            if 'external_files' in config:
                ConfigLoader._merge_external_files(config, config_path, error_log_file)
            
            return config
        except FileNotFoundError as e:
            error_msg = f"Configuration file '{config_path}' not found."
            print(f"Error: {error_msg}")
            ErrorLogger.log_error(error_log_file, error_msg, e)
            sys.exit(1)
        except toml.TomlDecodeError as e:
            error_msg = f"Failed to parse TOML configuration: {e}"
            print(f"Error: {error_msg}")
            ErrorLogger.log_error(error_log_file, error_msg, e)
            sys.exit(1)
        except Exception as e:
            error_msg = f"Unexpected error loading config file '{config_path}'"
            print(f"Error: {error_msg}: {e}")
            ErrorLogger.log_error(error_log_file, error_msg, e)
            sys.exit(1)
    
    @staticmethod
    def _merge_external_files(config, main_config_path, error_log_file):
        """Merge files sections from external TOML files.
        
        Args:
            config: Main configuration dictionary to merge into
            main_config_path: Path to the main config file (for resolving relative paths)
            error_log_file: Error log file path for logging
            
        Raises:
            SystemExit: If external file is not found, cannot be parsed, or contains invalid sections
        """
        external_files = config.get('external_files', [])
        if not isinstance(external_files, list):
            error_msg = "external_files must be a list of file paths"
            print(f"Error: {error_msg}")
            ErrorLogger.log_error(error_log_file, error_msg, None)
            sys.exit(1)
        
        # Get directory of main config file for resolving relative paths
        main_config_dir = os.path.dirname(os.path.abspath(main_config_path))
        
        # Initialize files section if it doesn't exist
        if 'files' not in config:
            config['files'] = {}
        
        for external_file in external_files:
            # Resolve relative paths relative to main config file
            if not os.path.isabs(external_file):
                external_file = os.path.join(main_config_dir, external_file)
            
            try:
                with open(external_file, 'r') as f:
                    external_config = toml.load(f)
                
                # Validate that external file only contains 'files' section
                allowed_sections = {'files'}
                found_sections = set(external_config.keys())
                invalid_sections = found_sections - allowed_sections
                
                if invalid_sections:
                    error_msg = f"External file '{external_file}' contains invalid sections: {', '.join(invalid_sections)}. Only [files] section is allowed."
                    print(f"Error: {error_msg}")
                    ErrorLogger.log_error(error_log_file, error_msg, None)
                    sys.exit(1)
                
                # Merge files section
                if 'files' in external_config:
                    config['files'].update(external_config['files'])
                    print(f"Loaded external files from: {external_file}")
                
            except FileNotFoundError as e:
                error_msg = f"External configuration file '{external_file}' not found."
                print(f"Error: {error_msg}")
                ErrorLogger.log_error(error_log_file, error_msg, e)
                sys.exit(1)
            except toml.TomlDecodeError as e:
                error_msg = f"Failed to parse external TOML configuration '{external_file}': {e}"
                print(f"Error: {error_msg}")
                ErrorLogger.log_error(error_log_file, error_msg, e)
                sys.exit(1)
            except Exception as e:
                error_msg = f"Unexpected error loading external config file '{external_file}'"
                print(f"Error: {error_msg}: {e}")
                ErrorLogger.log_error(error_log_file, error_msg, e)
                sys.exit(1)
    
    @staticmethod
    def get_interval_for_file(config, settings):
        """Get the interval for a file in seconds (converts from milliseconds if specified).
        
        Converts milliseconds to seconds by dividing by 1000.0 (float division).
        This ensures proper float results for all values:
        - 1000ms -> 1.0s
        - 500ms -> 0.5s
        - 250ms -> 0.25s
        
        Args:
            config: Global configuration dictionary
            settings: Dictionary containing file-specific settings, may include 'interval' key
            
        Returns:
            float: Interval in seconds
        """
        # Get default interval from config (in milliseconds), default to 1000ms (1 second)
        default_interval_ms = config.get('default_interval', 1000)
        
        # Get file-specific interval (in milliseconds), or use default
        interval_ms = settings.get('interval', default_interval_ms)
        
        # Convert milliseconds to seconds using float division
        # Division by 1000.0 (not 1000) ensures float result for proper time operations
        return interval_ms / 1000.0

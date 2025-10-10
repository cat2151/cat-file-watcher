#!/usr/bin/env python3
"""
Configuration loader for File Watcher
"""
import sys
import toml


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
        try:
            with open(config_path, 'r') as f:
                config = toml.load(f)
            return config
        except FileNotFoundError:
            print(f"Error: Configuration file '{config_path}' not found.")
            sys.exit(1)
        except toml.TomlDecodeError as e:
            print(f"Error: Failed to parse TOML configuration: {e}")
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

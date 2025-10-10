#!/usr/bin/env python3
"""
File Watcher - Monitor files and execute commands on timestamp changes
"""
import argparse
import os
import re
import sys
import time
import subprocess
import toml
import psutil


class FileWatcher:
    """Monitors files and executes commands when timestamps change."""
    
    def __init__(self, config_path):
        """Initialize the file watcher with a configuration file."""
        self.config_path = config_path
        self.config = self._load_config()
        self.file_timestamps = {}
        self.file_last_check = {}  # Track last check time for each file
        
    def _load_config(self):
        """Load and parse the TOML configuration file."""
        try:
            with open(self.config_path, 'r') as f:
                config = toml.load(f)
            return config
        except FileNotFoundError:
            print(f"Error: Configuration file '{self.config_path}' not found.")
            sys.exit(1)
        except toml.TomlDecodeError as e:
            print(f"Error: Failed to parse TOML configuration: {e}")
            sys.exit(1)
    
    def _get_file_timestamp(self, filepath):
        """Get the modification timestamp of a file."""
        try:
            return os.path.getmtime(filepath)
        except OSError:
            return None
    
    def _is_process_running(self, process_pattern):
        """Check if a process matching the given regex pattern is running.
        
        Args:
            process_pattern: Regular expression pattern to match against process names
            
        Returns:
            bool: True if a matching process is found, False otherwise
        """
        try:
            # Compile the regex pattern
            pattern = re.compile(process_pattern)
            
            # Iterate through all running processes
            for proc in psutil.process_iter(['name', 'cmdline']):
                try:
                    # Check process name
                    if proc.info['name'] and pattern.search(proc.info['name']):
                        return True
                    
                    # Check command line arguments
                    if proc.info['cmdline']:
                        cmdline = ' '.join(proc.info['cmdline'])
                        if pattern.search(cmdline):
                            return True
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    # Process may have terminated or we don't have access
                    continue
            
            return False
        except re.error as e:
            print(f"Warning: Invalid regex pattern '{process_pattern}': {e}")
            return False
        except Exception as e:
            print(f"Warning: Error checking for process '{process_pattern}': {e}")
            return False
    
    def _execute_command(self, command, filepath, settings):
        """Execute a shell command if the conditions are met.
        
        Args:
            command: The shell command to execute
            filepath: The path to the file that changed
            settings: Dictionary containing file-specific settings including optional 'suppress_if_process'
        """
        # Check if command execution should be suppressed based on running processes
        if 'suppress_if_process' in settings:
            process_pattern = settings['suppress_if_process']
            if self._is_process_running(process_pattern):
                print(f"Skipping command for '{filepath}': process matching '{process_pattern}' is running")
                return
        
        print(f"Executing command for '{filepath}': {command}")
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                if result.stdout:
                    print(f"Output: {result.stdout.strip()}")
            else:
                print(f"Error (exit code {result.returncode}): {result.stderr.strip()}")
        except subprocess.TimeoutExpired:
            print(f"Error: Command timed out after 30 seconds")
        except Exception as e:
            print(f"Error executing command: {e}")
    
    def _get_interval_for_file(self, settings):
        """Get the interval for a file in seconds (converts from milliseconds if specified).
        
        Converts milliseconds to seconds by dividing by 1000.0 (float division).
        This ensures proper float results for all values:
        - 1000ms -> 1.0s
        - 500ms -> 0.5s
        - 250ms -> 0.25s
        
        Args:
            settings: Dictionary containing file-specific settings, may include 'interval' key
            
        Returns:
            float: Interval in seconds
        """
        # Get default interval from config (in milliseconds), default to 1000ms (1 second)
        default_interval_ms = self.config.get('default_interval', 1000)
        
        # Get file-specific interval (in milliseconds), or use default
        interval_ms = settings.get('interval', default_interval_ms)
        
        # Convert milliseconds to seconds using float division
        # Division by 1000.0 (not 1000) ensures float result for proper time operations
        return interval_ms / 1000.0
    
    def _check_files(self):
        """Check all files for timestamp changes and execute commands if needed."""
        if 'files' not in self.config:
            print("Warning: No 'files' section found in configuration.")
            return
        
        current_time = time.time()
        files_config = self.config['files']
        for filename, settings in files_config.items():
            if 'command' not in settings:
                print(f"Warning: No command specified for file '{filename}'")
                continue
            
            # Get the interval for this file
            interval = self._get_interval_for_file(settings)
            
            # Check if enough time has passed since last check
            if filename in self.file_last_check:
                time_since_last_check = current_time - self.file_last_check[filename]
                if time_since_last_check < interval:
                    continue  # Skip this file, not enough time has passed
            
            # Update last check time
            self.file_last_check[filename] = current_time
            
            current_timestamp = self._get_file_timestamp(filename)
            
            if current_timestamp is None:
                if filename in self.file_timestamps:
                    print(f"Warning: File '{filename}' is no longer accessible")
                    del self.file_timestamps[filename]
                continue
            
            # Check if this is the first time we're seeing this file
            if filename not in self.file_timestamps:
                self.file_timestamps[filename] = current_timestamp
                print(f"Started monitoring '{filename}'")
            # Check if the timestamp has changed
            elif current_timestamp != self.file_timestamps[filename]:
                print(f"Detected change in '{filename}'")
                self._execute_command(settings['command'], filename, settings)
                self.file_timestamps[filename] = current_timestamp
    
    def run(self, interval=0.1):
        """Run the file watcher with the specified check interval (in seconds).
        
        Note: The interval parameter controls how often _check_files is called.
        Individual files may have their own check intervals configured in the TOML file.
        This should be set to a small value (default 0.1s) for responsiveness.
        """
        print(f"Starting file watcher with config: {self.config_path}")
        print(f"Checking for changes every {interval} second(s)...")
        print("Press Ctrl+C to stop.")
        
        try:
            while True:
                self._check_files()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nStopping file watcher...")


def main():
    """Main entry point for the file watcher."""
    parser = argparse.ArgumentParser(
        description='Monitor files and execute commands on timestamp changes'
    )
    parser.add_argument(
        '--config-filename',
        required=True,
        help='Path to the TOML configuration file'
    )
    
    args = parser.parse_args()
    
    watcher = FileWatcher(args.config_filename)
    watcher.run()


if __name__ == '__main__':
    main()

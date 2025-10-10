#!/usr/bin/env python3
"""
File Watcher - Monitor files and execute commands on timestamp changes
"""
import argparse
import os
import sys
import time
import subprocess
import toml


class FileWatcher:
    """Monitors files and executes commands when timestamps change."""
    
    def __init__(self, config_path):
        """Initialize the file watcher with a configuration file."""
        self.config_path = config_path
        self.config = self._load_config()
        self.file_timestamps = {}
        
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
    
    def _execute_command(self, command, filepath):
        """Execute a shell command."""
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
    
    def _check_files(self):
        """Check all files for timestamp changes and execute commands if needed."""
        if 'files' not in self.config:
            print("Warning: No 'files' section found in configuration.")
            return
        
        files_config = self.config['files']
        for filename, settings in files_config.items():
            if 'command' not in settings:
                print(f"Warning: No command specified for file '{filename}'")
                continue
            
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
                self._execute_command(settings['command'], filename)
                self.file_timestamps[filename] = current_timestamp
    
    def run(self, interval=1):
        """Run the file watcher with the specified check interval (in seconds)."""
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
    parser.add_argument(
        '--interval',
        type=float,
        default=1.0,
        help='Check interval in seconds (default: 1.0)'
    )
    
    args = parser.parse_args()
    
    watcher = FileWatcher(args.config_filename)
    watcher.run(interval=args.interval)


if __name__ == '__main__':
    main()

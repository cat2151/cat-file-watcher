#!/usr/bin/env python3
"""
File Watcher - Monitor files and execute commands on timestamp changes
"""
import os
import time

# Support both relative and absolute imports
try:
    from .config_loader import ConfigLoader
    from .command_executor import CommandExecutor
    from .process_detector import ProcessDetector
    from .time_period_checker import TimePeriodChecker
except ImportError:
    from config_loader import ConfigLoader
    from command_executor import CommandExecutor
    from process_detector import ProcessDetector
    from time_period_checker import TimePeriodChecker


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
        
    def _get_file_timestamp(self, filepath):
        """Get the modification timestamp of a file."""
        try:
            return os.path.getmtime(filepath)
        except OSError:
            return None
    
    def _get_interval_for_file(self, settings):
        """Get the interval for a file in seconds (backward compatibility)."""
        return ConfigLoader.get_interval_for_file(self.config, settings)
    
    def _is_process_running(self, process_pattern):
        """Check if a process is running (backward compatibility)."""
        return ProcessDetector.is_process_running(process_pattern)
    
    def _check_config_file(self):
        """Check if config file has been modified and reload if needed."""
        current_time = time.time()
        
        # Get config check interval (in milliseconds), default to 1000ms (1 second)
        config_check_interval_ms = self.config.get('config_check_interval', 1000)
        config_check_interval = config_check_interval_ms / 1000.0
        
        # Check if enough time has passed since last check
        if current_time - self.config_last_check < config_check_interval:
            return
        
        self.config_last_check = current_time
        current_timestamp = self._get_file_timestamp(self.config_path)
        
        if current_timestamp is None:
            print(f"Warning: Config file '{self.config_path}' is no longer accessible")
            return
        
        # Check if the config file has been modified
        if current_timestamp != self.config_timestamp:
            print(f"Detected change in config file '{self.config_path}', reloading...")
            try:
                new_config = ConfigLoader.load_config(self.config_path)
                self.config = new_config
                self.config_timestamp = current_timestamp
                print("Config reloaded successfully")
            except (SystemExit, Exception) as e:
                print(f"Error reloading config: {e}")
                print("Continuing with previous config")
    
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
            
            # Check if file should be monitored based on time period
            if not TimePeriodChecker.should_monitor_file(self.config, settings):
                # Skip monitoring this file - outside time period
                continue
            
            interval = ConfigLoader.get_interval_for_file(self.config, settings)
            
            # Check if enough time has passed since last check
            if filename in self.file_last_check:
                if current_time - self.file_last_check[filename] < interval:
                    continue
            
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
                CommandExecutor.execute_command(settings['command'], filename, settings, self.config)
                self.file_timestamps[filename] = current_timestamp
    
    def run(self, interval=0.1):
        """Run the file watcher with the specified check interval (in seconds)."""
        print(f"Starting file watcher with config: {self.config_path}")
        print(f"Checking for changes every {interval} second(s)...")
        print("Press Ctrl+C to stop.")
        
        try:
            while True:
                self._check_config_file()
                self._check_files()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nStopping file watcher...")


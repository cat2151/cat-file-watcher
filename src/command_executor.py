#!/usr/bin/env python3
"""
Command executor for File Watcher
"""
import subprocess
from datetime import datetime

# Support both relative and absolute imports
try:
    from .process_detector import ProcessDetector
except ImportError:
    from process_detector import ProcessDetector


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
        if 'suppress_if_process' in settings:
            process_pattern = settings['suppress_if_process']
            if ProcessDetector.is_process_running(process_pattern):
                print(f"Skipping command for '{filepath}': process matching '{process_pattern}' is running")
                return
        
        print(f"Executing command for '{filepath}': {command}")
        
        # Write to log file if enabled
        if settings.get('enable_log', False) and config and config.get('log_file'):
            CommandExecutor._write_to_log(filepath, settings, config)
        
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
    
    @staticmethod
    def _write_to_log(filepath, settings, config):
        """Write command execution information to log file.
        
        Args:
            filepath: The path to the file that changed
            settings: Dictionary containing file-specific settings
            config: Global configuration dictionary containing 'log_file'
        """
        try:
            log_file = config.get('log_file')
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            with open(log_file, 'a') as f:
                f.write(f"[{timestamp}] File: {filepath}\n")
                for key, value in settings.items():
                    f.write(f"  {key}: {value}\n")
                f.write("\n")
        except Exception as e:
            print(f"Warning: Failed to write to log file: {e}")

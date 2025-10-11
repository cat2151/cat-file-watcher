#!/usr/bin/env python3
"""
Process detection utilities for File Watcher
"""
import re
import psutil


class ProcessDetector:
    """Handles detection of running processes."""
    
    @staticmethod
    def is_process_running(process_pattern):
        """Check if a process matching the given regex pattern is running.
        
        Args:
            process_pattern: Regular expression pattern to match against process names
            
        Returns:
            bool: True if a matching process is found, False otherwise
        """
        result = ProcessDetector.get_matching_process(process_pattern)
        return result is not None
    
    @staticmethod
    def get_matching_process(process_pattern):
        """Get the first process matching the given regex pattern.
        
        Args:
            process_pattern: Regular expression pattern to match against process names
            
        Returns:
            str: Name of the matched process, or None if no match found
        """
        try:
            # Compile the regex pattern
            pattern = re.compile(process_pattern)
            
            # Iterate through all running processes
            for proc in psutil.process_iter(['name', 'cmdline']):
                try:
                    # Check process name
                    if proc.info['name'] and pattern.search(proc.info['name']):
                        return proc.info['name']
                    
                    # Check command line arguments
                    if proc.info['cmdline']:
                        cmdline = ' '.join(proc.info['cmdline'])
                        if pattern.search(cmdline):
                            return cmdline
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    # Process may have terminated or we don't have access
                    continue
            
            return None
        except re.error as e:
            print(f"Warning: Invalid regex pattern '{process_pattern}': {e}")
            return None
        except Exception as e:
            print(f"Warning: Error checking for process '{process_pattern}': {e}")
            return None

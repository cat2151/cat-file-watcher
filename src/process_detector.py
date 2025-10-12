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
            for proc in psutil.process_iter(["name", "cmdline"]):
                try:
                    # Check process name
                    if proc.info["name"] and pattern.search(proc.info["name"]):
                        return proc.info["name"]

                    # Check command line arguments
                    if proc.info["cmdline"]:
                        cmdline = " ".join(proc.info["cmdline"])
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

    @staticmethod
    def get_all_matching_processes(process_pattern):
        """Get all processes matching the given regex pattern with their PIDs.

        Args:
            process_pattern: Regular expression pattern to match against process names

        Returns:
            list: List of tuples (pid, process_name) for matched processes, or empty list if none found
        """
        try:
            # Compile the regex pattern
            pattern = re.compile(process_pattern)
            matched_processes = []

            # Iterate through all running processes
            for proc in psutil.process_iter(["pid", "name", "cmdline"]):
                try:
                    # Check process name
                    if proc.info["name"] and pattern.search(proc.info["name"]):
                        matched_processes.append((proc.info["pid"], proc.info["name"]))
                        continue

                    # Check command line arguments
                    if proc.info["cmdline"]:
                        cmdline = " ".join(proc.info["cmdline"])
                        if pattern.search(cmdline):
                            matched_processes.append((proc.info["pid"], cmdline))
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    # Process may have terminated or we don't have access
                    continue

            return matched_processes
        except re.error as e:
            print(f"Warning: Invalid regex pattern '{process_pattern}': {e}")
            return []
        except Exception as e:
            print(f"Warning: Error checking for processes '{process_pattern}': {e}")
            return []

    @staticmethod
    def terminate_process(pid):
        """Terminate a process by sending a terminate signal.

        Args:
            pid: Process ID to terminate

        Returns:
            bool: True if termination signal was sent successfully, False otherwise
        """
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            return True
        except psutil.NoSuchProcess:
            print(f"Warning: Process {pid} does not exist")
            return False
        except psutil.AccessDenied:
            print(f"Warning: Access denied when trying to terminate process {pid}")
            return False
        except Exception as e:
            print(f"Warning: Error terminating process {pid}: {e}")
            return False

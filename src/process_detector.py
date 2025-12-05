#!/usr/bin/env python3
"""
Process detection utilities for File Watcher
"""

import re
import sys

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

    @staticmethod
    def get_all_windows_by_title(title_pattern):
        """Get all windows matching the given regex pattern with their process IDs.

        This function is Windows-specific. On non-Windows platforms, it returns an empty list.
        Uses EnumWindows, GetWindowText, and GetWindowThreadProcessId Win32 APIs.

        Args:
            title_pattern: Regular expression pattern to match against window titles

        Returns:
            list: List of tuples (pid, window_title) for matched windows, or empty list if none found
        """
        if sys.platform != "win32":
            print("Warning: terminate_if_window_title is only supported on Windows")
            return []

        try:
            import ctypes
            from ctypes import wintypes

            # Compile the regex pattern
            pattern = re.compile(title_pattern)
            matched_windows = []

            # Define Win32 API functions
            user32 = ctypes.windll.user32
            EnumWindows = user32.EnumWindows
            GetWindowTextW = user32.GetWindowTextW
            GetWindowTextLengthW = user32.GetWindowTextLengthW
            GetWindowThreadProcessId = user32.GetWindowThreadProcessId
            IsWindowVisible = user32.IsWindowVisible

            # Define the callback function type
            WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

            def enum_windows_callback(hwnd, lparam):
                """Callback function for EnumWindows."""
                # Skip invisible windows
                if not IsWindowVisible(hwnd):
                    return True

                # Get window text length
                length = GetWindowTextLengthW(hwnd)
                if length == 0:
                    return True

                # Get window text
                buffer = ctypes.create_unicode_buffer(length + 1)
                GetWindowTextW(hwnd, buffer, length + 1)
                window_title = buffer.value

                # Check if title matches the pattern
                if pattern.search(window_title):
                    # Get process ID
                    pid = wintypes.DWORD()
                    GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                    matched_windows.append((pid.value, window_title))

                return True

            # Enumerate all windows
            EnumWindows(WNDENUMPROC(enum_windows_callback), 0)

            return matched_windows
        except re.error as e:
            print(f"Warning: Invalid regex pattern '{title_pattern}': {e}")
            return []
        except Exception as e:
            print(f"Warning: Error enumerating windows for pattern '{title_pattern}': {e}")
            return []

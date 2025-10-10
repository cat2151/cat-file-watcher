#!/usr/bin/env python3
"""
Main entry point for File Watcher
"""
import argparse

# Support both relative and absolute imports
try:
    from .cat_file_watcher import FileWatcher
except ImportError:
    from cat_file_watcher import FileWatcher


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

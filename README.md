# cat-file-watcher

**File Change Monitoring Tool - Detects file changes and executes commands**

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
</p>

※Most of this document is AI-generated. I threw issues to the agent and had it generate them. Some parts (concepts, usage distinctions) are written manually.

## Quick Links
| Item | Link |
|------|--------|
| 📊 Development Status | [generated-docs/daily-summaries](generated-docs/daily-summaries) |

## Overview

This is a file monitoring tool that observes changes in file timestamps and executes a command when a file is updated.

## Features

- Monitor multiple files simultaneously
- Execute custom commands on file change
- Configurable via TOML settings file
- Lightweight and easy to use

## Installation

1. Clone this repository:
```bash
git clone https://github.com/cat2151/cat-file-watcher.git
cd cat-file-watcher
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the file watcher by specifying a configuration file:

```bash
python -m src --config-filename config.toml
```

Arguments:
- `--config-filename`: Path to the TOML configuration file (required)

## Configuration

Create a TOML configuration file to define the files to monitor and the commands to execute:

```toml
# Default monitoring interval
# Time format: "1s" (1 second), "2m" (2 minutes), "3h" (3 hours), "0.5s" (0.5 seconds)
# Old format (integer milliseconds, e.g., 1000) is also supported for backward compatibility
default_interval = "1s"

# Check interval for changes to the config file itself
config_check_interval = "1s"

# File path for command execution logs (optional)
log_file = "command_execution.log"

# Time period definitions (optional)
[time_periods]
business_hours = { start = "09:00", end = "17:00" }
night_shift = { start = "23:00", end = "01:00" }

[files]
"myfile.txt" = { command = "echo 'File changed!'" }
"script.py" = { command = "python -m pytest tests/", interval = "2s" }
"src/main.py" = { command = "make build", suppress_if_process = "vim|emacs|code" }
"batch.csv" = { command = "./process.sh", time_period = "night_shift" }
"important.txt" = { command = "backup.sh", enable_log = true }
"lib/module.c" = { command = "gcc -c module.c -o module.o", cwd = "./lib" }
```

### Configuration Format

The configuration file requires a `[files]` section where each entry maps a filename to a command:

- **Key**: The path to the file or directory to monitor (relative or absolute path)
  - For files: The command is executed when the file's modification time changes.
  - For directories: The command is executed when the directory's modification time changes (e.g., file added/deleted).
- **Value**: An object with a `command` field containing the shell command to execute.
  - `command` (required): The shell command to execute when the file or directory changes.
  - `interval` (optional): The monitoring interval for this specific file or directory. Specified in time format ("1s", "2m", "3h", "0.5s"). Decimal values are allowed (e.g., "0.5s" is 0.5 seconds). The old format (integer milliseconds) is also supported for backward compatibility. If omitted, `default_interval` is used.
  - `suppress_if_process` (optional): A regular expression pattern to match against running process names. If a matching process is found, command execution is skipped. Useful for preventing actions from triggering while specific programs like editors are running.
  - `time_period` (optional): The name of a time period during which the file or directory should be monitored. Specifies a time period name defined in the `[time_periods]` section. Monitoring only occurs within the specified time period.
  - `enable_log` (optional): If set to `true`, detailed command execution will be logged to the log file (default: `false`). The `log_file` setting must be configured in global settings.
  - `cwd` (optional): Changes the working directory to the specified path before executing the command. This allows relative paths within the command to be resolved from the specified directory.

### Global Configuration

- `default_interval` (optional): The default monitoring interval for all files and directories. Specified in time format ("1s", "2m", "3h", "0.5s"). Decimal values are allowed (e.g., "0.5s" is 0.5 seconds). The old format (integer milliseconds, e.g., 1000) is also supported for backward compatibility. If omitted, "1s" (1 second) is used.
- `config_check_interval` (optional): The check interval for changes to the configuration file itself. Specified in time format ("1s", "2m", "3h", "0.5s"). The configuration file will be automatically reloaded if it changes. If omitted, "1s" (1 second) is used.
- `log_file` (optional): The path to a log file where detailed command execution information will be recorded. If set, command execution details (timestamp, path, TOML configuration content) for files or directories with `enable_log = true` will be written to this file.

### Time Period Configuration

You can define time periods in the `[time_periods]` section (optional):

- Each time period is defined with a name.
- `start`: Start time (HH:MM format, e.g., "09:00").
- `end`: End time (HH:MM format, e.g., "17:00").
- Time periods spanning across midnight are also supported (e.g., `start = "23:00", end = "01:00"`).
- By specifying a time period name with the `time_period` parameter for each file, that file or directory will only be monitored within that specific time period.

Example:
```toml
[time_periods]
business_hours = { start = "09:00", end = "17:00" }  # Regular business hours
night_shift = { start = "23:00", end = "01:00" }     # Time period spanning midnight
```

### Configuration Examples

Refer to `examples/config.example.toml` for complete examples of various use cases.

```toml
# Set default monitoring interval to 1 second
default_interval = 1000

# Set config file change check interval to 1 second
config_check_interval = 1000

# Log file for detailed command execution (optional)
log_file = "command_execution.log"

# Define time periods
[time_periods]
business_hours = { start = "09:00", end = "17:00" }
after_hours = { start = "18:00", end = "08:00" }  # Spans midnight

[files]
# Use default interval (checks every 1 second)
"document.txt" = { command = "cp document.txt document.txt.bak" }

# Specify custom interval (checks every 500ms)
"app.log" = { command = "notify-send 'Log Updated' 'New entries in app.log'", interval = 500 }

# Specify custom interval (checks every 5 seconds)
"config.ini" = { command = "systemctl reload myapp", interval = 5000 }

# Monitor only during business hours
"report.txt" = { command = "python generate_report.py", time_period = "business_hours" }

# Monitor only outside business hours (e.g., for batch processing)
"batch.csv" = { command = "./process_batch.sh", time_period = "after_hours" }

# Enable logging for important files (records timestamp, file path, and config details)
"important.txt" = { command = "backup.sh", enable_log = true }
```

## How it Works

1. The tool reads the TOML configuration file.
2. It monitors the modification timestamps of all specified files.
3. When a file's timestamp changes, the associated command is executed.
4. The configuration file itself is also monitored and automatically reloaded if it changes.
5. This process continuously repeats until stopped with Ctrl+C.

## Concept

Prioritizes simple and maintainable TOML descriptions.

## When to Use

For easy and hassle-free file change monitoring: cat-file-watcher

For quickly turning on/off change monitoring for scattered files: cat-file-watcher

If you want to use the unique features available here: cat-file-watcher

For more advanced features: other applications

For TypeScript app development, etc.: standard task runners

## License

MIT License - See LICENSE file for details

※This README.md is automatically generated by GitHub Actions based on README.ja.md translated by Gemini.
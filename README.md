# cat-file-watcher

**File Change Monitoring Tool - Detects file changes and executes commands**

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
</p>

*Note: This document is largely AI-generated. Issues were submitted to an agent for generation. Some parts (Concepts, Usage Scenarios) were written manually.*

## Quick Links
| Item | Link |
|------|--------|
| 📊 Development Status | [generated-docs/daily-summaries](generated-docs/daily-summaries) |

## Overview

This is a file monitoring tool that watches for changes in file timestamps and executes commands when files are updated.

## Features

- Monitor multiple files simultaneously
- Execute custom commands on file change
- Configurable with a TOML configuration file
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
python src/cat_file_watcher.py --config-filename config.toml
```

Arguments:
- `--config-filename`: Path to the TOML configuration file (required)

## Configuration

Create a TOML configuration file to define files to monitor and commands to execute:

```toml
# Default monitoring interval (in milliseconds)
default_interval = 1000

# Interval for checking changes to the configuration file itself (in milliseconds)
config_check_interval = 1000

# File path for command execution logs (optional)
log_file = "command_execution.log"

# Time period definitions (optional)
[time_periods]
business_hours = { start = "09:00", end = "17:00" }
night_shift = { start = "23:00", end = "01:00" }

[files]
"myfile.txt" = { command = "echo 'File changed!'" }
"script.py" = { command = "python -m pytest tests/", interval = 2000 }
"src/main.py" = { command = "make build", suppress_if_process = "vim|emacs|code" }
"batch.csv" = { command = "./process.sh", time_period = "night_shift" }
"important.txt" = { command = "backup.sh", enable_log = true }
```

### Configuration Format

The configuration file requires a `[files]` section where each entry maps a filename to a command:

- **Key**: Path to the file to monitor (relative or absolute path)
- **Value**: An object containing a `command` field with the shell command to execute
  - `command` (required): The shell command to execute when the file changes
  - `interval` (optional): The monitoring interval for this file (in milliseconds). If omitted, `default_interval` will be used.
  - `suppress_if_process` (optional): A regular expression pattern to match against running process names. If a matching process is found, command execution is skipped. This is useful for preventing actions from being triggered when a specific program, like an editor, is running.
  - `time_period` (optional): The name of a time period during which the file should be monitored. Specify a time period name defined in the `[time_periods]` section. The file will only be monitored within the specified time period.
  - `enable_log` (optional): If set to `true`, detailed command execution will be logged to the `log_file` (default: `false`). The `log_file` setting must be configured in the global settings.

### Global Settings

- `default_interval` (optional): Default monitoring interval for all files (in milliseconds). If omitted, 1000ms (1 second) will be used.
- `config_check_interval` (optional): Interval for checking changes to the configuration file itself (in milliseconds). If the config file changes, it will be automatically reloaded. If omitted, 1000ms (1 second) will be used.
- `log_file` (optional): Path to the log file for recording detailed command execution. If configured, command execution information (timestamp, file path, TOML configuration content) for files with `enable_log = true` will be recorded in this file.

### Time Period Settings

You can define time periods in the `[time_periods]` section (optional):

- Each time period is defined with a name.
- `start`: Start time (HH:MM format, e.g., "09:00")
- `end`: End time (HH:MM format, e.g., "17:00")
- Time periods spanning across midnight are also supported (e.g., `start = "23:00", end = "01:00"`).
- If a `time_period` parameter is specified for each file, that file will only be monitored within that designated time period.

Example:
```toml
[time_periods]
business_hours = { start = "09:00", end = "17:00" }  # Regular business hours
night_shift = { start = "23:00", end = "01:00" }     # Period spanning across midnight
```

### Configuration Example

Refer to `examples/config.example.toml` for a complete example of various use cases.

```toml
# Set default monitoring interval to 1 second
default_interval = 1000

# Set configuration file change check interval to 1 second
config_check_interval = 1000

# Log file for detailed command execution (optional)
log_file = "command_execution.log"

# Time period definitions
[time_periods]
business_hours = { start = "09:00", end = "17:00" }
after_hours = { start = "18:00", end = "08:00" }  # Spans across midnight

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

# Enable logging for important files (records timestamp, file path, and config content)
"important.txt" = { command = "backup.sh", enable_log = true }
```

## How it Works

1. The tool loads the TOML configuration file.
2. It monitors the modification timestamps of all specified files.
3. When a file's timestamp changes, the associated command is executed.
4. The configuration file itself is also monitored and automatically reloaded if changes are detected.
5. This process continuously repeats until stopped with Ctrl+C.

## Concepts

Priority is given to simple and easily maintainable TOML descriptions.

## Usage Scenarios

For easy file change monitoring and straightforward operation, use cat-file-watcher.

For more advanced features, consider other applications.

## License

MIT License - See the LICENSE file for details.

*Note: This README.md is automatically generated from README.ja.md using Gemini's translation via GitHub Actions.*
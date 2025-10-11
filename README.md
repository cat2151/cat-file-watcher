# cat-file-watcher

**File Watcher - Detects file changes and executes commands**

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
</p>

*Note: This document is mostly AI-generated. Issues were submitted to an agent for generation. Some sections (Concept, Usage Scenarios) were written manually.*

## Quick Links
| Item | Link |
|------|--------|
| 📊 Development Status | [generated-docs/daily-summaries](generated-docs/daily-summaries) |

## Overview

This is a file monitoring tool that watches for changes in file timestamps and executes commands when files are updated.

## Features

- Monitor multiple files simultaneously
- Execute custom commands on file changes
- Configurable via TOML configuration file
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
default_interval = "1s"

# Interval for checking changes to the configuration file itself
config_check_interval = "1s"

# Path to the command execution log file (optional)
log_file = "command_execution.log"

# Path to the error log file (optional)
# error_log_file = "error.log"

# Path to the command execution suppression log file (optional)
# suppression_log_file = "suppression.log"

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

The configuration file requires a `[files]` section where each entry maps a filename (or directory) to a command:

- **Key**: Path to the file or directory to monitor (relative or absolute path)
  - For files: Executes the command when the file's modification time changes.
  - For directories: Executes the command when the directory's modification time changes (e.g., files added/deleted).
- **Value**: An object containing a `command` field that specifies the shell command to execute.
  - `command` (required): The shell command to execute when the file or directory changes.
  - `interval` (optional): The monitoring interval for this file or directory. Specified in time format ("1s", "2m", "3h", "0.5s"). Decimal values are also supported (e.g., "0.5s" for 0.5 seconds). If omitted, `default_interval` will be used.
  - `suppress_if_process` (optional): A regular expression pattern to match against running process names. If a matching process is found, command execution will be skipped. This is useful for avoiding triggering actions when specific programs like editors are running.
  - `time_period` (optional): The name of a time period during which the file or directory should be monitored. Specify a time period name defined in the `[time_periods]` section. Monitoring will only occur within the specified time period.
  - `enable_log` (optional): If set to `true`, details of command execution will be recorded in the log file (default: `false`). The `log_file` must be configured in global settings.
  - `cwd` (optional): Changes the working directory to the specified path before executing the command. This allows relative paths within the command to be resolved from the specified directory.

### Global Settings

- `default_interval` (optional): The default monitoring interval for all files and directories. Specified in time format ("1s", "2m", "3h", "0.5s"). Decimal values are also supported (e.g., "0.5s" for 0.5 seconds). If omitted, "1s" (1 second) will be used.
- `config_check_interval` (optional): The interval for checking changes to the configuration file itself. Specified in time format ("1s", "2m", "3h", "0.5s"). If the configuration file changes, it will be automatically reloaded. If omitted, "1s" (1 second) will be used.
- `log_file` (optional): The path to the log file where details of command execution will be recorded. If set, command execution information (timestamp, path, TOML configuration content) for files or directories with `enable_log = true` will be logged to this file.
- `error_log_file` (optional): The path to the error log file where detailed error information will be recorded. If set, when a command fails, detailed information (error message, executed command, stderr output, stack trace) will be logged to this file.
- `suppression_log_file` (optional): The path to the suppression log file where command execution suppression details will be recorded. If set, when command execution is skipped due to `suppress_if_process`, information (timestamp, file path, process pattern, matched process) will be logged to this file.


### Time Period Settings

You can define time periods in the `[time_periods]` section (optional):

- Each time period is defined with a name.
- `start`: Start time (HH:MM format, e.g., "09:00")
- `end`: End time (HH:MM format, e.g., "17:00")
- Time periods spanning across midnight are also supported (e.g., `start = "23:00", end = "01:00"`).
- If you specify a time period name using the `time_period` parameter for a file, that file or directory will only be monitored within that time period.

Example:
```toml
[time_periods]
business_hours = { start = "09:00", end = "17:00" }  # Regular business hours
night_shift = { start = "23:00", end = "01:00" }     # Time period spanning midnight
```

### Configuration Examples

For complete examples of various use cases, please refer to `examples/config.example.toml`.

```toml
# Set default monitoring interval to 1 second
default_interval = "1s"

# Set configuration file check interval to 1 second
config_check_interval = "1s"

# Log file for detailed command execution (optional)
log_file = "command_execution.log"

# Error log file (optional)
# error_log_file = "error.log"

# Command execution suppression log file (optional)
# suppression_log_file = "suppression.log"

# Define time periods
[time_periods]
business_hours = { start = "09:00", end = "17:00" }
after_hours = { start = "18:00", end = "08:00" }  # Spans across midnight

[files]
# Uses default interval (checks every 1 second)
"document.txt" = { command = "cp document.txt document.txt.bak" }

# Custom interval specified (checks every 0.5 seconds)
"app.log" = { command = "notify-send 'Log Updated' 'New entries in app.log'", interval = "0.5s" }

# Custom interval specified (checks every 5 seconds)
"config.ini" = { command = "systemctl reload myapp", interval = "5s" }

# Monitored only during business hours
"report.txt" = { command = "python generate_report.py", time_period = "business_hours" }

# Monitored only after hours (e.g., for batch processing)
"batch.csv" = { command = "./process_batch.sh", time_period = "after_hours" }

# Enable logging for important files (records timestamp, file path, and config details)
"important.txt" = { command = "backup.sh", enable_log = true }
```

## How It Works

1. The tool reads the TOML configuration file.
2. It monitors the modification timestamps of all specified files.
3. When a file's timestamp changes, the associated command is executed.
4. The configuration file itself is also monitored and automatically reloaded if changes are detected.
5. This process continuously repeats until stopped with Ctrl+C.

### Command Output

The standard output and standard error output of executed commands are displayed in the console:

- **On success (exit code 0)**: If there is stdout output, it will be displayed as `Output: <output content>`
- **On failure (non-zero exit code)**: The stderr output will be displayed as `Error (exit code <code>): <error content>`
- **Error log file**: If `error_log_file` is configured, detailed error information (error message, executed command, stderr output, stack trace) will be logged to the file when a command fails

Command execution has a timeout of 30 seconds, after which a timeout error will occur.

## Concept

Prioritizes simple and maintainable TOML descriptions.

## Usage Scenarios

Use cat-file-watcher when you want to easily monitor file updates and maintain effortless operation.

Use cat-file-watcher when you need to quickly toggle update monitoring on/off for scattered files.

Use cat-file-watcher when you want to leverage its unique features.

For more advanced features, consider other applications.

For TypeScript application development and similar tasks, a standard task runner is recommended.

## License

MIT License - See the LICENSE file for details.

*Note: This README.md is automatically generated from README.ja.md using Gemini's translation via GitHub Actions.*
# cat-file-watcher

**File Change Monitoring Tool - Detects file changes and executes commands**

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
</p>

※ This document is largely AI-generated. Issues were submitted to an agent for generation. Some parts (Concept, Usage Scenarios) were written manually.

## Quick Links
| Item | Link |
|------|--------|
| 📊 Development Status | [generated-docs/daily-summaries](generated-docs/daily-summaries) |

## Overview

A file monitoring tool that watches for changes in file timestamps and executes commands when files are updated.

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

Create a TOML configuration file that defines the files to monitor and the commands to execute:

```toml
# Default monitoring interval (in milliseconds)
default_interval = 1000

# Interval for checking changes in the configuration file itself (in milliseconds)
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
"lib/module.c" = { command = "gcc -c module.c -o module.o", chdir = "./lib" }
```

### Configuration Format

The configuration file requires a `[files]` section where each entry maps a filename or directory to a command:

- **Key**: Path to the file or directory to monitor (relative or absolute)
  - For files: Execute the command when the file's modification time changes
  - For directories: Execute the command when the directory's modification time changes (e.g., file added/deleted)
- **Value**: An object with a `command` field containing the shell command to execute
  - `command` (required): The shell command to execute when the file or directory changes
  - `interval` (optional): Monitoring interval for this file or directory (in milliseconds). If omitted, `default_interval` will be used.
  - `suppress_if_process` (optional): A regex pattern that matches running process names. If a matching process is found, command execution will be skipped. Useful for preventing actions from being triggered when certain programs like editors are running.
  - `time_period` (optional): The name of a time period during which the file or directory should be monitored. Specify a time period name defined in the `[time_periods]` section. Monitoring will only occur within the specified time period.
  - `enable_log` (optional): If set to `true`, command execution details will be logged to a file (default: `false`). The `log_file` setting in global configuration is required.
  - `chdir` (optional): Change the working directory to the specified path before executing the command. This allows relative paths in the command to be resolved from the specified directory.

### Global Settings

- `default_interval` (optional): Default monitoring interval for all files and directories (in milliseconds). If omitted, 1000ms (1 second) will be used.
- `config_check_interval` (optional): Interval for checking changes in the configuration file itself (in milliseconds). If the configuration file changes, it will be reloaded automatically. If omitted, 1000ms (1 second) will be used.
- `log_file` (optional): Path to the log file for recording command execution details. If set, command execution information (timestamp, path, TOML configuration content) for files or directories with `enable_log = true` will be recorded in this file.

### Time Period Settings

You can define time periods in the `[time_periods]` section (optional):

- Each time period is defined with a name.
- `start`: Start time (HH:MM format, e.g., "09:00")
- `end`: End time (HH:MM format, e.g., "17:00")
- Time periods spanning across midnight are also supported (e.g., `start = "23:00", end = "01:00"`).
- By specifying a time period name using the `time_period` parameter for each file, that file or directory will only be monitored within that time period.

Example:
```toml
[time_periods]
business_hours = { start = "09:00", end = "17:00" }  # Normal hours
night_shift = { start = "23:00", end = "01:00" }     # Spanning across midnight
```

### Configuration Example

For a complete example of various use cases, refer to `examples/config.example.toml`.

```toml
# Set default monitoring interval to 1 second
default_interval = 1000

# Set configuration file self-check interval to 1 second
config_check_interval = 1000

# Log file for command execution details (optional)
log_file = "command_execution.log"

# Time period definitions
[time_periods]
business_hours = { start = "09:00", end = "17:00" }
after_hours = { start = "18:00", end = "08:00" }  # Spanning across midnight

[files]
# Use default interval (check every 1 second)
"document.txt" = { command = "cp document.txt document.txt.bak" }

# Specify custom interval (check every 500ms)
"app.log" = { command = "notify-send 'Log Updated' 'New entries in app.log'", interval = 500 }

# Specify custom interval (check every 5 seconds)
"config.ini" = { command = "systemctl reload myapp", interval = 5000 }

# Monitor only during business hours
"report.txt" = { command = "python generate_report.py", time_period = "business_hours" }

# Monitor only outside business hours (e.g., for batch processing)
"batch.csv" = { command = "./process_batch.sh", time_period = "after_hours" }

# Enable logging for important files (records timestamp, file path, and configuration content)
"important.txt" = { command = "backup.sh", enable_log = true }
```

## How It Works

1. The tool reads the TOML configuration file.
2. It monitors the modification timestamps of all specified files.
3. When a file's timestamp changes, the associated command is executed.
4. The configuration file itself is also monitored, and if it changes, it's automatically reloaded.
5. This process continuously repeats until stopped with Ctrl+C.

## Concept

Prioritize simple and maintainable TOML descriptions.

## Usage Scenarios

For easy file change monitoring and straightforward operation, use `cat-file-watcher`.

For quickly enabling/disabling monitoring of scattered files, use `cat-file-watcher`.

If you want to utilize the unique features it offers, use `cat-file-watcher`.

For more advanced features, consider other applications.

For TypeScript application development, etc., a standard task runner is typically used.

## License

MIT License - See the LICENSE file for details.

※ This `README.md` is automatically generated from `README.ja.md` using Gemini's translation via GitHub Actions.
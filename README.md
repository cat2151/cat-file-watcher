# cat-file-watcher

**File Change Monitoring Tool - Detects file changes and executes commands**

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
</p>

*This document is largely AI-generated. Issues were submitted to an agent for generation. Some parts (concepts, usage distinctions) were written manually.*

## Quick Links
| Item | Link |
|------|--------|
| 📊 Development Status | [generated-docs/daily-summaries](generated-docs/daily-summaries) |

## Overview

This is a file monitoring tool that watches for changes in file timestamps and executes commands when a file is updated.

## Features

- Monitor multiple files simultaneously
- Execute custom commands on file change
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

Create a TOML configuration file that defines the files to monitor and the commands to execute:

```toml
# Default monitoring interval
# Time format: "1s" (1 second), "2m" (2 minutes), "3h" (3 hours), "0.5s" (0.5 seconds)
default_interval = "1s"

# Interval for checking changes to the config file itself
config_check_interval = "1s"

# File path for command execution logs (optional)
log_file = "command_execution.log"

# File path for error logs (optional)
# error_log_file = "error.log"

# File path for suppression logs (optional)
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

The configuration file requires a `[files]` section where each entry maps a file name to a command:

- **Key**: Path to the file or directory to monitor (relative or absolute)
  - For files: Executes the command when the file's modification time changes
  - For directories: Executes the command when the directory's modification time changes (e.g., file added/deleted)
- **Value**: An object containing a `command` field with the shell command to execute
  - `command` (required): The shell command to execute when the file or directory changes
  - `interval` (optional): The monitoring interval for this file or directory. Specified in time format ("1s", "2m", "3h", "0.5s"). Decimal values are also supported (e.g., "0.5s" for 0.5 seconds). If omitted, `default_interval` will be used.
  - `suppress_if_process` (optional): A regular expression pattern to match against running process names. If a matching process is found, command execution will be skipped. This is useful for preventing actions from being triggered while specific programs like editors are running.
  - `time_period` (optional): The name of a time period during which the file or directory should be monitored. Specify a time period name defined in the `[time_periods]` section. Monitoring will only occur within the specified time period.
  - `enable_log` (optional): If set to `true`, detailed command execution information will be logged to a file (default: `false`). Requires `log_file` to be configured in the global settings.
  - `cwd` (optional): Changes the working directory to the specified path before executing the command. This ensures that relative paths within the command are resolved from the specified directory.

### Global Settings

- `default_interval` (optional): The default monitoring interval for all files and directories. Specified in time format ("1s", "2m", "3h", "0.5s"). Decimal values are also supported (e.g., "0.5s" for 0.5 seconds). If omitted, "1s" (1 second) will be used.
- `config_check_interval` (optional): The interval for checking changes to the configuration file itself. Specified in time format ("1s", "2m", "3h", "0.5s"). If the configuration file changes, it will be reloaded automatically. If omitted, "1s" (1 second) will be used.
- `log_file` (optional): The path to a log file where detailed command execution information will be recorded. If set, command execution details (timestamp, path, TOML configuration content) for files or directories with `enable_log = true` will be logged to this file.
- `error_log_file` (optional): The path to an error log file where detailed command execution errors will be recorded. If set, details such as error messages, executed commands, standard error output, and stack traces on command failure will be logged to this file.
- `suppression_log_file` (optional): The path to a log file where details of command execution suppression will be recorded. If set, information (timestamp, file path, process pattern, matched process) when command execution is skipped due to `suppress_if_process` will be logged to this file.

### Time Period Settings

You can define time periods in the `[time_periods]` section (optional):

- Each time period is defined with a name.
- `start`: Start time (HH:MM format, e.g., "09:00")
- `end`: End time (HH:MM format, e.g., "17:00")
- Time periods spanning across midnight are also supported (e.g., `start = "23:00", end = "01:00"`)
- By specifying a time period name using the `time_period` parameter for each file, that file or directory will only be monitored within that time period.

Example:
```toml
[time_periods]
business_hours = { start = "09:00", end = "17:00" }  # Normal business hours
night_shift = { start = "23:00", end = "01:00" }     # Time period spanning midnight
```

### Configuration Example

For a complete example with various use cases, refer to `examples/config.example.toml`.

```toml
# Set the default monitoring interval to 1 second
default_interval = "1s"

# Set the config file change check interval to 1 second
config_check_interval = "1s"

# Log file for detailed command execution (optional)
log_file = "command_execution.log"

# Error log file (optional)
# error_log_file = "error.log"

# Command execution suppression log file (optional)
# suppression_log_file = "suppression.log"

# Time period definitions
[time_periods]
business_hours = { start = "09:00", end = "17:00" }
after_hours = { start = "18:00", end = "08:00" }  # Spans across midnight

[files]
# Use default interval (check every 1 second)
"document.txt" = { command = "cp document.txt document.txt.bak" }

# Specify custom interval (check every 0.5 seconds)
"app.log" = { command = "notify-send 'Log Updated' 'New entries in app.log'", interval = "0.5s" }

# Specify custom interval (check every 5 seconds)
"config.ini" = { command = "systemctl reload myapp", interval = "5s" }

# Monitor only during business hours
"report.txt" = { command = "python generate_report.py", time_period = "business_hours" }

# Monitor only during after-hours (e.g., for batch processing)
"batch.csv" = { command = "./process_batch.sh", time_period = "after_hours" }

# Enable logging for important files (records timestamp, file path, config content)
"important.txt" = { command = "backup.sh", enable_log = true }
```

## How It Works

1. The tool reads the TOML configuration file.
2. It monitors the modification timestamps of all specified files.
3. When a file's timestamp changes, it executes the associated command.
4. The configuration file itself is also monitored, and if changes are detected, it is automatically reloaded.
5. This process continuously repeats until stopped by Ctrl+C.

### Command Execution Handling

**Important**: Commands are executed **sequentially**.

- When a file change is detected and a command is executed, the next file check will not occur until that command completes (or times out after 30 seconds).
- For example, if a command for one file takes 25 seconds, monitoring of other files will be paused for those 25 seconds.
- Even if other files are updated during this time, they will not be detected until the currently running command finishes (they will be detected in the next main loop after the command completes).
- The current implementation does not support parallel monitoring and execution of multiple files.

For commands that require long execution times, it is necessary to implement background execution within the command or launch them as separate processes.

**Methods for Non-Blocking Execution**:
- **Linux/macOS**: Append `&` to the end of the command (e.g., `command = "long_task.sh &"`)
- **Windows**: Prepend `start ` to the command (e.g., `command = "start long_task.bat"`)

### Command Execution Output

The standard output and standard error output of executed commands are displayed to the console **in real-time**:

- **Output Display**: The standard output and standard error output of commands are progressively displayed to the console during execution. Even for long-running commands, you can monitor their progress in real-time.
- **On Failure**: If a command fails (exit code other than 0), an `Error: Command failed for '<file path>' with exit code <code_value>` message will be displayed.
- **Error Log File**: If `error_log_file` is configured, the error message and executed command upon failure will be logged to the error file.

The command execution timeout is set to 30 seconds; exceeding this will result in a timeout error.

## Concept

Prioritizes simple and maintainable TOML descriptions.

## When to Use

- If you want to easily monitor file updates and simplify operations, use cat-file-watcher.
- If you need to quickly toggle update monitoring for scattered files, use cat-file-watcher.
- If you want to use its unique features, use cat-file-watcher.
- If you need more advanced features, consider other applications.
- For TypeScript app development, etc., a standard task runner is typically used.

## License

MIT License - See the LICENSE file for details

*This README.md is automatically generated by GitHub Actions using Gemini's translation based on README.ja.md*
# cat-file-watcher

**File Change Monitoring Tool - Detects file changes and executes commands**

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
</p>

※Most of this document is AI-generated. Issues were submitted to an agent to generate it. Some parts (concept, use cases) were written manually.

## Quick Links
| Item | Link |
|------|--------|
| 📊 Development Status | [generated-docs/development-status](generated-docs/development-status.md) |

## Overview

This is a file monitoring tool that watches for changes in file timestamps and executes a command when a file is updated.

## Features

- Monitor multiple files simultaneously
- Execute custom commands on file changes
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
default_interval = "1s"

# Interval for checking changes in the configuration file itself
config_check_interval = "1s"

# File path for command execution logs (optional)
log_file = "command_execution.log"

# File path for error logs (optional)
# error_log_file = "error.log"

# File path for command suppression logs (optional)
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

The configuration file requires a `[files]` section where each entry maps a filename to a command:

- **Key**: The path to the file or directory to monitor (relative or absolute path).
  - For files: The command is executed when the file's modification time changes.
  - For directories: The command is executed when the directory's modification time changes (e.g., file added/deleted).
- **Value**: An object with a `command` field specifying the shell command to execute.
  - `command` (required): The shell command to execute when the file or directory changes.
  - `interval` (optional): The monitoring interval for this specific file or directory. Specified in time format ("1s", "2m", "3h", "0.5s"). Decimal values are also allowed (e.g., "0.5s" for 0.5 seconds). If omitted, `default_interval` will be used.
  - `suppress_if_process` (optional): A regular expression pattern that matches a running process name. If a matching process is found, command execution is skipped. This is useful for preventing actions from being triggered while specific programs like editors are running.
  - `time_period` (optional): The name of a time period during which the file or directory should be monitored. Specifies a time period name defined in the `[time_periods]` section. Monitoring will only occur within the specified time period.
  - `enable_log` (optional): If set to `true`, details of command execution will be logged to the log file (default: `false`). The `log_file` global setting must be configured.
  - `cwd` (optional): Changes the working directory to the specified path before executing the command. This allows relative paths within the command to be resolved from the specified directory.

### Global Settings

- `default_interval` (optional): The default monitoring interval for all files and directories. Specified in time format ("1s", "2m", "3h", "0.5s"). Decimal values are also allowed (e.g., "0.5s" for 0.5 seconds). If omitted, "1s" (1 second) will be used.
- `config_check_interval` (optional): The interval for checking changes in the configuration file itself. Specified in time format ("1s", "2m", "3h", "0.5s"). If the configuration file changes, it will be automatically reloaded. If omitted, "1s" (1 second) will be used.
- `log_file` (optional): The path to a log file where details of command execution are recorded. If set, command execution information (timestamp, path, TOML configuration content) for files or directories with `enable_log = true` will be recorded in this file.
- `error_log_file` (optional): The path to an error log file where details of command execution errors are recorded. If set, detailed information such as error messages, executed commands, standard error output, and stack traces on command failure will be recorded in this file.
- `suppression_log_file` (optional): The path to a log file where details of command execution suppression are recorded. If set, information when command execution is skipped due to `suppress_if_process` (timestamp, file path, process pattern, matched process) will be recorded in this file.

### Time Period Settings

You can define time periods in the `[time_periods]` section (optional):

- Each time period is defined with a name.
- `start`: Start time (HH:MM format, e.g., "09:00").
- `end`: End time (HH:MM format, e.g., "17:00").
- Time periods spanning across days are supported (e.g., `start = "23:00", end = "01:00"`).
- By specifying a time period name with the `time_period` parameter for each file, that file or directory will only be monitored during that specified time period.

Example:
```toml
[time_periods]
business_hours = { start = "09:00", end = "17:00" }  # Regular business hours
night_shift = { start = "23:00", end = "01:00" }     # Time period spanning across days
```

### Configuration Examples

Refer to `examples/config.example.toml` for complete examples of various use cases.

```toml
# Set default monitoring interval to 1 second
default_interval = "1s"

# Set configuration file change check interval to 1 second
config_check_interval = "1s"

# Log file for command execution details (optional)
log_file = "command_execution.log"

# Error log file (optional)
# error_log_file = "error.log"

# Command suppression log file (optional)
# suppression_log_file = "suppression.log"

# Time period definitions
[time_periods]
business_hours = { start = "09:00", end = "17:00" }
after_hours = { start = "18:00", end = "08:00" }  # Spans across days

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

# Enable logging for important files (records timestamp, file path, configuration details)
"important.txt" = { command = "backup.sh", enable_log = true }
```

## How It Works

1.  The tool reads the TOML configuration file.
2.  It monitors the modification timestamps of all specified files.
3.  When a file's timestamp changes, the associated command is executed.
4.  The configuration file itself is also monitored and automatically reloaded if changed.
5.  This process continuously repeats until stopped with Ctrl+C.

### Command Execution Processing Method

**Important**: Commands are executed **sequentially**.

- When a file change is detected and a command is executed, the next file will not be checked until that command completes (or times out after 30 seconds).
- For example, if a command for one file takes 25 seconds, monitoring of other files will be paused for those 25 seconds.
- Even if other files are updated during this time, they will not be detected until the running command completes (they will be detected in the next main loop after the command completes).
- The current implementation does not support parallelizing the monitoring and execution of multiple files.

For commands that require long execution times, you need to make arrangements to run them in the background within the command itself or launch them as a separate process.

**Methods for non-blocking execution**:
- **Linux/macOS**: Append `&` to the command (e.g., `command = "long_task.sh &"`).
- **Windows**: Prepend `start ` to the command (e.g., `command = "start long_task.bat"`).

### Command Execution Output

The standard output and standard error of executed commands are displayed **in real-time** in the console:

- **Output Display**: The standard output and standard error of commands are progressively displayed in the console during execution. Even for long-running commands, you can check their progress in real-time.
- **On Failure**: If a command fails (exits with a non-zero code), a message `Error: Command failed for '<file_path>' with exit code <code_number>` will be displayed.
- **Error Log File**: If `error_log_file` is configured, the error message and the executed command on failure will be recorded in the log file.

Command execution has a timeout of 30 seconds; exceeding this will result in a timeout error.

## Concept

Prioritizes simple and maintainable TOML descriptions.

## When to Use

Use cat-file-watcher for easy file change monitoring.

Use cat-file-watcher for effortless operation.

Use cat-file-watcher for quickly enabling/disabling change monitoring for scattered files.

Use cat-file-watcher to leverage its unique features.

For more advanced features, consider other applications.

For TypeScript app development, standard task runners are typically used.

## Development

### Environment Setup

To set up the development environment:

```bash
# Install runtime dependencies
pip install -r requirements.txt

# Install development dependencies (including Ruff)
pip install -r dev-requirements.txt
```

### Code Quality Checks

This project uses [Ruff](https://docs.astral.sh/ruff/) to maintain code quality.

#### Running Ruff

```bash
# Lint checking
ruff check src/

# Automatically fix fixable issues
ruff check --fix src/

# Check code formatting
ruff format --check src/

# Apply code formatting
ruff format src/
```

#### Automated CI/CD Checks

When you create a Pull Request, GitHub Actions automatically runs the following checks:

- `ruff check src/` - Linter checks for code quality
- `ruff format --check src/` - Code formatting verification

If these checks fail, the PR will be blocked from merging. It is recommended to run Ruff locally and format your code before creating a PR.

### Running Tests

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v
```

## License

MIT License - See the LICENSE file for details.

※This README.md is automatically generated by GitHub Actions using a Gemini translation based on README.ja.md.
# cat-file-watcher

**File Change Monitoring Tool - Detects file changes and executes commands**

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
</p>

※This document is largely AI-generated. Issues were submitted to an agent for generation. Parts (Concept, Use Cases) were written manually.

## Quick Links
| Item | Link |
|------|--------|
| 📊 Development Status | [generated-docs/development-status](generated-docs/development-status.md) |

## Overview

This is a file monitoring tool that observes changes in file timestamps and executes commands when a file is updated.

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

## Quick Start

Get started immediately with minimal configuration! It works with **just one line in a TOML file**:

1. Create a configuration file (`config.toml`):
```toml
files = [{path = "test.txt", command = "echo File changed"}]
```

2. Create the file to be monitored:
```bash
touch test.txt
```

3. Start the file watcher:
```bash
python -m src --config-filename config.toml
```

That's it! This will monitor changes to `test.txt` and execute the command if it changes.

Try editing the file:
```bash
echo "Test" >> test.txt
```

You will see "File changed" displayed in the console.

**Note**: The single-line format above is the official TOML syntax using inline array notation. A more readable multi-line format is also available (see the [Configuration](#configuration) section for details).

## Usage

Run the file watcher by specifying the configuration file:

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

The configuration file requires a `[files]` section where each entry maps a file or directory path to a command:

-   **Key**: Path to the file or directory to monitor (relative or absolute path).
    -   For files: The command is executed when the file's modification time changes.
    -   For directories: The command is executed when the directory's modification time changes (e.g., due to file addition/deletion).
-   **Value**: An object with a `command` field specifying the shell command to execute.
    -   `command` (required): The shell command to execute when the file or directory changes.
    -   `interval` (optional): Monitoring interval for this specific file or directory. Specified in time format ("1s", "2m", "3h", "0.5s"). Decimal points are also supported (e.g., "0.5s" for 0.5 seconds). If omitted, `default_interval` is used.
    -   `suppress_if_process` (optional): A regex pattern to match against running process names. If a matching process is found, command execution is skipped. Useful for not triggering actions when specific programs like editors are running.
    -   `time_period` (optional): The name of a time period during which the file or directory should be monitored. Specifies a time period name defined in the `[time_periods]` section. Monitoring only occurs within the specified time period.
    -   `enable_log` (optional): If set to `true`, detailed command execution will be logged to the `log_file` (default: `false`). The global `log_file` setting must be configured.
    -   `cwd` (optional): Changes the working directory to the specified path before executing the command. This ensures that relative paths in the command are resolved from the specified directory.

### Global Settings

-   `default_interval` (optional): The default monitoring interval for all files and directories. Specified in time format ("1s", "2m", "3h", "0.5s"). Decimal points are also supported (e.g., "0.5s" for 0.5 seconds). If omitted, "1s" (1 second) is used.
-   `config_check_interval` (optional): The interval for checking changes to the configuration file itself. Specified in time format ("1s", "2m", "3h", "0.5s"). The configuration file is automatically reloaded if it changes. If omitted, "1s" (1 second) is used.
-   `log_file` (optional): Path to a log file where detailed command executions are recorded. If set, command execution information (timestamp, path, TOML configuration content) for files or directories with `enable_log = true` will be recorded in this file.
-   `error_log_file` (optional): Path to an error log file where details of command execution errors are recorded. If set, detailed information such as error messages on command failure, the executed command, standard error output, and stack traces will be recorded in this file.
-   `suppression_log_file` (optional): Path to a log file where details of command execution suppression are recorded. If set, information when command execution is skipped due to `suppress_if_process` (timestamp, file path, process pattern, matched process) will be recorded in this file.

### Time Period Settings

You can define time periods in the `[time_periods]` section (optional):

-   Each time period is defined with a name.
-   `start`: Start time (HH:MM format, e.g., "09:00").
-   `end`: End time (HH:MM format, e.g., "17:00").
-   Time periods spanning across midnight are also supported (e.g., `start = "23:00", end = "01:00"`).
-   If you specify a `time_period` parameter for a file, that file or directory will only be monitored during that defined time period.

Example:
```toml
[time_periods]
business_hours = { start = "09:00", end = "17:00" }  # Regular business hours
night_shift = { start = "23:00", end = "01:00" }     # Time period spanning across midnight
```

### Configuration Example

Refer to `examples/config.example.toml` for a complete example with various use cases.

```toml
# Set default monitoring interval to 1 second
default_interval = "1s"

# Set configuration file change check interval to 1 second
config_check_interval = "1s"

# Log file for detailed command execution (optional)
log_file = "command_execution.log"

# Error log file (optional)
# error_log_file = "error.log"

# Command suppression log file (optional)
# suppression_log_file = "suppression.log"

# Time period definitions
[time_periods]
business_hours = { start = "09:00", end = "17:00" }
after_hours = { start = "18:00", end = "08:00" }  # Spans across midnight

[files]
# Uses default interval (checks every 1 second)
"document.txt" = { command = "cp document.txt document.txt.bak" }

# Specifies a custom interval (checks every 0.5 seconds)
"app.log" = { command = "notify-send 'Log Updated' 'New entries in app.log'", interval = "0.5s" }

# Specifies a custom interval (checks every 5 seconds)
"config.ini" = { command = "systemctl reload myapp", interval = "5s" }

# Monitors only during business hours
"report.txt" = { command = "python generate_report.py", time_period = "business_hours" }

# Monitors only during after-hours (e.g., for batch processing)
"batch.csv" = { command = "./process_batch.sh", time_period = "after_hours" }

# Enables logging for important files (records timestamp, file path, and configuration content)
"important.txt" = { command = "backup.sh", enable_log = true }
```

## How It Works

1.  The tool reads the TOML configuration file.
2.  It monitors the modification timestamps of all specified files.
3.  When a file's timestamp changes, the associated command is executed.
4.  The configuration file itself is also monitored and automatically reloaded if it changes.
5.  This process continuously repeats until stopped with Ctrl+C.

### Command Execution Mechanism

**Important**: Commands are executed **sequentially**.

-   When a file change is detected and a command is executed, the next file will not be checked until that command completes (or times out after 30 seconds).
-   For example, if a command for one file takes 25 seconds, monitoring of other files will be paused for that 25-second duration.
-   Even if other files are updated during this time, they will not be detected until the currently running command completes (they will be detected in the next main loop after the command finishes).
-   The current implementation does not support parallel monitoring and execution of multiple files.

For commands that require a long execution time, you will need to run them in the background within the command or launch them as a separate process.

**Methods for Non-Blocking Execution**:
-   **Linux/macOS**: Append `&` to the end of the command (e.g., `command = "long_task.sh &"`)
-   **Windows**: Prefix the command with `start ` (e.g., `command = "start long_task.bat"`)

### Command Execution Output

The standard output and standard error of executed commands are displayed on the console **in real-time**:

-   **Output Display**: The standard output and standard error of commands are shown sequentially on the console during execution. Even for long-running commands, you can monitor their progress in real-time.
-   **On Failure**: If a command fails (exit code other than 0), a message like `Error: Command failed for '<file_path>' with exit code <code_value>` will be displayed.
-   **Error Log File**: If `error_log_file` is configured, error messages and the executed command on failure will be recorded in the log file.

Command execution has a timeout of 30 seconds; exceeding this will result in a timeout error.

## Concept

Prioritizes simplicity and maintainability of TOML descriptions.

## Use Cases and Differentiation

For easily monitoring file updates and wanting simple operation, use cat-file-watcher.

For quickly enabling/disabling update monitoring for scattered files, use cat-file-watcher.

If you want to use the unique features available here, use cat-file-watcher.

For more advanced features, consider other applications.

For TypeScript application development, standard task runners are recommended.

## Development

### Environment Setup

Set up your development environment:

```bash
# Install dependencies (for runtime environment)
pip install -r requirements.txt

# Install development dependencies (including Ruff)
pip install -r dev-requirements.txt
```

### Code Quality Checks

This project uses [Ruff](https://docs.astral.sh/ruff/) to maintain code quality.

#### Running Ruff

```bash
# Linter check
ruff check src/

# Fix auto-fixable issues
ruff check --fix src/

# Code format check
ruff format --check src/

# Apply code format
ruff format src/
```

#### Automated Checks in CI/CD

When you create a Pull Request, GitHub Actions automatically performs the following:

1.  **Automated Code Formatting**:
    -   `ruff format src/` - Automatically formats the code (e.g., removes trailing spaces)
    -   `ruff check --fix src/` - Fixes auto-fixable lint issues
    -   If formatting causes changes, it automatically commits and pushes them.

2.  **Quality Checks**:
    -   `ruff check src/` - Performs linter checks for code quality.
    -   `ruff format --check src/` - Verifies code formatting.

If checks fail even after automatic formatting, the PR merge will be blocked. It is recommended to run Ruff locally to format your code beforehand.

### Running Tests

```bash
# Run all tests
pytest

# Run tests with detailed output
pytest -v
```

## License

MIT License - See the LICENSE file for details.

※This README.md is automatically generated by GitHub Actions using Gemini's translation based on README.ja.md.
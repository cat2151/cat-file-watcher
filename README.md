# cat-file-watcher - Cat is watching your file -

**File Monitoring Tool - Detects file changes and executes commands**

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
  <a href="https://deepwiki.com/cat2151/cat-file-watcher"><img src="https://deepwiki.com/badge.svg" alt="Ask DeepWiki"></a>
</p>

※ This document is largely AI-generated. Issues were submitted to an agent for generation. Some parts (Concept, Use Cases, Tests) were written manually.

## Quick Links
| Section | Link |
|---------|------|
| 📊 Development Status | [generated-docs/development-status](generated-docs/development-status.md) |

## Overview

A file monitoring tool that watches for changes in file timestamps and executes a command when a file is updated.

## Features

- Monitor multiple files simultaneously
- Execute custom commands on file changes
- Configurable via a TOML configuration file
- Lightweight and easy to use
- On Windows, can be configured not to steal focus from the launched application (or rather, to quickly reclaim it)

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

Get started right away with minimal configuration! It works with **just a single-line TOML file**:

1. Create a configuration file (`config.toml`):
```toml
files = [{path = "test.txt", command = "echo File has been changed"}]
```

2. Create the file to be monitored:
```bash
touch test.txt
```

3. Start the file watcher:
```bash
python -m src --config-filename config.toml
```

That's it! It will now monitor `test.txt` and execute the command when changes are detected!

Try editing the file:
```bash
echo "Test" >> test.txt
```

"File has been changed" will be displayed in your console.

**Key Point**: The single-line format above is a valid TOML syntax using inline array notation. A more readable multi-line format is also available (see the [Configuration](#configuration) section for details).

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

# Interval for checking the configuration file itself
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

The configuration file requires a `[files]` section where each entry maps a file name to a command:

- **Key**: The path to the file or directory to monitor (relative or absolute).
  - For files: The command is executed when the file's modification time changes.
  - For directories: The command is executed when the directory's modification time changes (e.g., adding or deleting files).
- **Value**: An object containing a `command` field (normal mode) or an `argv` field (no_focus mode) and other optional parameters:
  - `command` (required for normal mode): The shell command to execute when the file or directory changes. **Note**: Cannot be used when `no_focus=true`.
  - `argv` (required for no_focus mode): An array field required when `no_focus=true`. Specifies the executable name and arguments as an array. Example: `argv = ["notepad.exe", "file.txt"]`
  - `interval` (optional): The monitoring interval for this specific file or directory. Specified in time format ("1s", "2m", "3h", "0.5s"). Decimal values are allowed (e.g., "0.5s" for 0.5 seconds). If omitted, `default_interval` is used.
  - `suppress_if_process` (optional): A regular expression pattern to match against running process names. If a matching process is found, command execution will be skipped. Useful for preventing actions from triggering when specific programs (like editors) are running.
  - `time_period` (optional): The name of a time period during which the file or directory should be monitored. Specifies a time period name defined in the `[time_periods]` section. Monitoring only occurs within the specified time period.
  - `enable_log` (optional): If set to `true`, detailed command execution will be logged to the log file (default: `false`). Requires `log_file` to be set in the global configuration.
  - `cwd` (optional): Changes the working directory to the specified path before executing the command. This ensures that relative paths within the command are resolved from the specified directory.
  - `no_focus` (optional): If set to `true`, the command will be executed without stealing focus (default: `false`). **Windows-specific** - Commands are launched asynchronously (the tool does not wait for completion), and the window is displayed but not activated, preventing focus theft. Uses `shell=False`. On non-Windows platforms, it will issue a warning and fall back to normal execution. **Important**: When `no_focus=true`, the `command` field cannot be used. Instead, the `argv` array field is required. Example: `argv = ["notepad.exe", "file.txt"]`

### Global Settings

- `default_interval` (optional): The default monitoring interval for all files and directories. Specified in time format ("1s", "2m", "3h", "0.5s"). Decimal values are allowed (e.g., "0.5s" for 0.5 seconds). If omitted, "1s" (1 second) is used.
- `config_check_interval` (optional): The interval for checking changes in the configuration file itself. Specified in time format ("1s", "2m", "3h", "0.5s"). The configuration file will be reloaded automatically if changed. If omitted, "1s" (1 second) is used.
- `log_file` (optional): The path to a log file where detailed command execution information is recorded. If set, command execution details (timestamp, path, TOML configuration content) for files or directories with `enable_log = true` will be recorded in this file.
- `error_log_file` (optional): The path to an error log file where detailed command execution errors are recorded. If set, detailed information such as error messages, executed commands, standard error output, and stack traces will be recorded in this file upon command failure.
- `suppression_log_file` (optional): The path to a log file where details of command execution suppression are recorded. If set, information when command execution is skipped due to `suppress_if_process` (timestamp, file path, process pattern, matched process) will be recorded in this file.

### Time Period Settings

You can define time periods in the `[time_periods]` section (optional):

- Each time period is defined with a name.
- `start`: Start time (HH:MM format, e.g., "09:00").
- `end`: End time (HH:MM format, e.g., "17:00").
- Time periods spanning across midnight are also supported (e.g., `start = "23:00", end = "01:00"`).
- By specifying a `time_period` parameter for each file, that file or directory will only be monitored within that defined time period.

Example:
```toml
[time_periods]
business_hours = { start = "09:00", end = "17:00" }  # Normal business hours
night_shift = { start = "23:00", end = "01:00" }     # Time period spanning across midnight
```

### Configuration Examples

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

# Define time periods
[time_periods]
business_hours = { start = "09:00", end = "17:00" }
after_hours = { start = "18:00", end = "08:00" }  # Spans across midnight

[files]
# Uses default interval (checks every 1 second)
"document.txt" = { command = "cp document.txt document.txt.bak" }

# Specifies custom interval (checks every 0.5 seconds)
"app.log" = { command = "notify-send 'Log Updated' 'New entries in app.log'", interval = "0.5s" }

# Specifies custom interval (checks every 5 seconds)
"config.ini" = { command = "systemctl reload myapp", interval = "5s" }

# Monitors only during business hours
"report.txt" = { command = "python generate_report.py", time_period = "business_hours" }

# Monitors only after business hours (e.g., for batch processing)
"batch.csv" = { command = "./process_batch.sh", time_period = "after_hours" }

# Enables logging for important files (records timestamp, file path, and configuration details)
"important.txt" = { command = "backup.sh", enable_log = true }
```

## How It Works

1. The tool reads the TOML configuration file.
2. It monitors the modification timestamps of all specified files.
3. When a file's timestamp changes, the associated command is executed.
4. The configuration file itself is also monitored and automatically reloaded if changed.
5. This process continuously repeats until stopped with Ctrl+C.

### Command Execution Processing Method

**Important**: Commands are executed **sequentially**.

- When a file change is detected and a command is executed, the next file check will not occur until that command completes (or times out after 30 seconds for foreground execution).
- For example, if a command for one file takes 25 seconds, monitoring of other files will be paused for those 25 seconds.
- Even if other files are updated during this time, they will not be detected until the currently running command completes (they will be detected in the next main loop after the command finishes).
- The current implementation does not support parallel monitoring and execution of multiple files.

For commands that require a long execution time, you will need to implement background execution within the command or launch it as a separate process.

**Non-blocking Execution Methods**:
- **Linux/macOS**: Append `&` to the command (e.g., `command = "long_task.sh &"`).
- **Windows**: Prepend `start ` to the command (e.g., `command = "start long_task.bat"`).

### Command Output During Execution

Standard output and standard error from executed commands are displayed in the console **in real-time**:

- **Output Display**: The standard output and standard error of commands are displayed incrementally in the console as they run. Even for long-running commands, you can monitor their progress in real-time.
- **On Failure**: If a command fails (exit code other than 0), a message like `Error: Command failed for '<file_path>' with exit code <code_number>` will be displayed.
- **Error Log File**: If `error_log_file` is configured, error messages and executed commands upon failure will be recorded in the log file.

Foreground commands have a timeout of 30 seconds; exceeding this will result in a timeout error. For commands requiring longer execution, use background execution (with `&`). Background executed commands are not subject to the timeout limit because `subprocess.run()` completes immediately.

## Concept

Prioritizes simple and maintainable TOML descriptions.

## Use Cases

For easy and convenient file change monitoring, use cat-file-watcher.

For quickly enabling/disabling monitoring of scattered files, use cat-file-watcher.

For utilizing its unique features, use cat-file-watcher.

For more advanced features, consider other applications.

For TypeScript application development, standard task runners are recommended.

## Development

### Environment Setup

Set up the development environment:

```bash
# Install dependencies (for runtime environment)
pip install -r requirements.txt

# Install development dependencies (including Ruff)
pip install -r dev-requirements.txt
```

### Code Quality Check

This project uses [Ruff](https://docs.astral.sh/ruff/) to maintain code quality.

#### Running Ruff

```bash
# Linter check
ruff check src/

# Fix auto-fixable issues
ruff check --fix src/

# Check code formatting
ruff format --check src/

# Apply code formatting
ruff format src/
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v
```

- Linux
  - All tests are for Linux.
  - Tests were generated and TDD'd by the GitHub Copilot Coding Agent on GitHub Actions (Linux Runner).

- Windows
  - Running tests on Windows without WSL2 frequently results in test failures (red), as the tests are designed for Linux.
  - To run tests in a Windows environment, use WSL2.
  - Specifically, install WSL2, prepare with `wsl pip install -r dev-requirements.txt`, then run `wsl pytest`.
  - While some tests might still fail (red) under WSL2, this is acceptable. The benchmark is that tests should be green when TDD'd by the agent after an issue is submitted.

## License

MIT License - See LICENSE file for details

※ The English README.md is automatically generated by GitHub Actions using Gemini's translation based on README.ja.md.

*Big Brother watched your files. Now the cat does. 🐱*
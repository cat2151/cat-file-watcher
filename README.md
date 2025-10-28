# cat-file-watcher

**File Change Monitoring Tool - Detects file changes and executes commands**

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
</p>

*Most of this document is AI-generated. I threw issues at an agent and had it generate the content. Some parts (concepts, usage scenarios, tests) were written manually.*

## Quick Links
| Item | Link |
|------|--------|
| 📊 Development Status | [generated-docs/development-status](generated-docs/development-status.md) |

## Overview

This is a file monitoring tool that observes changes in file timestamps and executes commands when a file is updated.

## Features

- Monitors multiple files simultaneously
- Executes custom commands upon file modification
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

## Quick Start

Get started immediately with minimal configuration! It works with **just one line in a TOML file**:

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

That's it! It will monitor `test.txt` for changes and execute the command when detected!

Try editing the file:
```bash
echo "Test" >> test.txt
```

"File has been changed" will be displayed in the console.

**Note**: The single-line format above is a valid TOML syntax using inline array notation. A more readable multi-line format is also available (see the [Configuration](#configuration) section for details).

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

The configuration file requires a `[files]` section where each entry maps a filename to a command:

- **Key**: The path to the file or directory to monitor (relative or absolute path)
  - For files: The command is executed when the file's modification time changes.
  - For directories: The command is executed when the directory's modification time changes (e.g., files added/deleted).
- **Value**: An object with a `command` field containing the shell command to execute.
  - `command` (required): The shell command to execute when the file or directory changes.
  - `interval` (optional): The monitoring interval for this specific file or directory. Specified in time format ("1s", "2m", "3h", "0.5s"). Decimal values are allowed (e.g., "0.5s" is 0.5 seconds). If omitted, `default_interval` is used.
  - `suppress_if_process` (optional): A regular expression pattern that matches running process names. If a matching process is found, command execution is skipped. This is useful for preventing actions from triggering while specific programs like editors are running.
  - `time_period` (optional): The name of the time period during which the file or directory should be monitored. Specifies a time period name defined in the `[time_periods]` section. Monitoring only occurs within the specified time period.
  - `enable_log` (optional): Set to `true` to log detailed command execution information to the log file (default: `false`). Requires `log_file` to be configured in global settings.
  - `cwd` (optional): Changes the working directory to the specified path before executing the command. This ensures that relative paths in the command are resolved from the specified directory.

### Global Settings

- `default_interval` (optional): The default monitoring interval for all files and directories. Specified in time format ("1s", "2m", "3h", "0.5s"). Decimal values are allowed (e.g., "0.5s" is 0.5 seconds). If omitted, "1s" (1 second) is used.
- `config_check_interval` (optional): The interval for checking the configuration file itself for changes. Specified in time format ("1s", "2m", "3h", "0.5s"). The configuration file is automatically reloaded if it changes. If omitted, "1s" (1 second) is used.
- `log_file` (optional): The path to a log file where detailed command execution information is recorded. If set, command execution details (timestamp, path, TOML configuration content) for files or directories with `enable_log = true` will be recorded in this file.
- `error_log_file` (optional): The path to an error log file where detailed command execution errors are recorded. If set, detailed information such as error messages upon command failure, the executed command, standard error output, and stack traces will be recorded in this file.
- `suppression_log_file` (optional): The path to a log file where detailed command suppression information is recorded. If set, information about commands skipped due to `suppress_if_process` (timestamp, file path, process pattern, matched process) will be recorded in this file.

### Time Period Settings

You can define time periods in the `[time_periods]` section (optional):

- Each time period is defined with a name.
- `start`: Start time (HH:MM format, e.g., "09:00").
- `end`: End time (HH:MM format, e.g., "17:00").
- Time periods spanning across midnight are supported (e.g., `start = "23:00", end = "01:00"`).
- By specifying a `time_period` parameter for each file, that file or directory will only be monitored within the specified time period.

Example:
```toml
[time_periods]
business_hours = { start = "09:00", end = "17:00" }  # Regular hours
night_shift = { start = "23:00", end = "01:00" }     # Spans across midnight
```

### Configuration Example

Refer to `examples/config.example.toml` for a complete example covering various use cases.

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

# Monitors only outside business hours (e.g., for batch processing)
"batch.csv" = { command = "./process_batch.sh", time_period = "after_hours" }

# Enables logging for important files (records timestamp, file path, and configuration)
"important.txt" = { command = "backup.sh", enable_log = true }
```

## How It Works

1. The tool reads the TOML configuration file.
2. It monitors the modification timestamps of all specified files.
3. When a file's timestamp changes, the associated command is executed.
4. The configuration file itself is also monitored and automatically reloaded if it changes.
5. This process continuously repeats until stopped by Ctrl+C.

### Command Execution Processing Method

**Important**: Commands are executed **sequentially**.

- When a file change is detected and a command is executed, the next file check will not occur until that command completes (or times out after 30 seconds if running in the foreground).
- For example, if a command for one file takes 25 seconds, monitoring of other files is paused for those 25 seconds.
- Even if other files are updated during this time, they will not be detected until the running command completes (they will be detected in the next main loop).
- The current implementation does not support parallel monitoring and execution of multiple files.

For commands that require long execution times, you need to either run them in the background within the command itself or launch them as a separate process.

**Methods for non-blocking execution**:
- **Linux/macOS**: Append `&` to the command (e.g., `command = "long_task.sh &"`).
- **Windows**: Prefix the command with `start ` (e.g., `command = "start long_task.bat"`).

### Command Execution Output

The standard output and standard error output of executed commands are displayed in the console **in real-time**:

- **Output Display**: The standard output and standard error output of commands are sequentially displayed in the console during execution. Even for long-running commands, progress can be checked in real-time.
- **On Failure**: If a command fails (exit code other than 0), a message like `Error: Command failed for '<filepath>' with exit code <code_number>` will be displayed.
- **Error Log File**: If `error_log_file` is configured, error messages upon command failure and the executed command will be recorded in the log file.

Foreground commands have a 30-second timeout, after which a timeout error will occur. For commands requiring longer execution, please use background execution (using `&`). Commands executed in the background are not subject to the timeout limit because `subprocess.run()` completes immediately.

## Concepts

Prioritize simple and maintainable TOML descriptions.

## Usage Scenarios

For easy file change monitoring and simple operation, use cat-file-watcher.

For quickly enabling/disabling change monitoring for scattered files, use cat-file-watcher.

If you want to use the unique features available here, use cat-file-watcher.

For more advanced features, consider other applications.

For TypeScript application development, use standard task runners.

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

# Run tests with detailed output
pytest -v
```

- Linux
  - All tests are for Linux.
  - GitHub Copilot Coding Agent generated the test code and performed TDD on GitHub Actions (Linux Runner).

- Windows
  - Running tests without WSL2 on a Windows environment will result in many test failures (red). This is because the tests are designed for Linux.
  - To run tests on Windows, use WSL2.
  - Specifically, install WSL2, then prepare with `wsl pip install -r dev-requirements.txt`, and then run `wsl pytest`.
  - Some tests might still fail in WSL2, which is tolerated. The standard is that if TDD generated by the agent results in green tests, it's acceptable.

## License

MIT License - See the LICENSE file for details

*The English `README.md` is automatically generated by GitHub Actions using Gemini's translation based on `README.ja.md`.*
# cat-file-watcher - Cat is watching your file -

**File Change Monitoring Tool - Detects file changes and executes commands**

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
</p>

*This document is mostly AI-generated. Issues were fed to an agent to generate it. Some parts (concept, use cases, test) were written manually.*

## Quick Links
| Item | Link |
|------|--------|
| 📊 Development Status | [generated-docs/development-status](generated-docs/development-status.md) |

## Overview

This is a file monitoring tool that watches for changes in file timestamps and executes a command when a file is updated.

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

Get started immediately with minimal setup! It works with **just one line in a TOML file**:

1. Create a configuration file (`config.toml`):
```toml
files = [{path = "test.txt", command = "echo ファイルが変更されました"}]
```

2. Create the file to be monitored:
```bash
touch test.txt
```

3. Start the file watcher:
```bash
python -m src --config-filename config.toml
```

With this, it will monitor `test.txt` for changes and execute the command if any are detected!

Try editing the file:
```bash
echo "テスト" >> test.txt
```

You will see "ファイルが変更されました" (File changed) displayed in the console.

**Note**: The single-line format above is a valid TOML notation using inline array syntax. A more readable multi-line format can also be used (see the [Configuration](#configuration) section for details).

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

# Configuration file self-check interval
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

The configuration file requires a `[files]` section where each entry maps a file path or directory path to a command:

- **Key**: The path to the file or directory to monitor (relative or absolute path)
  - For files: The command is executed when the file's modification timestamp changes.
  - For directories: The command is executed when the directory's modification timestamp changes (e.g., adding or deleting files).
- **Value**: An object containing a `command` field, which is the shell command to execute.
  - `command` (required): The shell command to execute when the file or directory changes.
  - `interval` (optional): The monitoring interval for this file or directory. Specify in time format ("1s", "2m", "3h", "0.5s"). Decimal values are also allowed (e.g., "0.5s" is 0.5 seconds). If omitted, `default_interval` will be used.
  - `suppress_if_process` (optional): A regular expression pattern to match against running process names. If a matching process is found, command execution is skipped. This is useful for preventing actions from triggering when specific programs like editors are running.
  - `time_period` (optional): The name of a time period during which the file or directory should be monitored. Specify a time period name defined in the `[time_periods]` section. Monitoring will only occur within the specified time period.
  - `enable_log` (optional): If set to `true`, details of command execution will be recorded in the log file (default: `false`). The `log_file` global setting must be configured.
  - `cwd` (optional): Changes the working directory to the specified path before executing the command. This ensures that relative paths within the command are resolved from the specified directory.
  - `no_focus` (optional): If set to `true`, the command is executed without stealing focus (default: `false`). **Windows Only** - The command is launched asynchronously (the tool does not wait for completion), and the window will be shown but not activated, preventing focus theft. Uses `shell=False` and splits the command by spaces. On non-Windows platforms, a warning will be displayed, and execution will fall back to normal. Note: Shell features like pipes, redirects, and environment variable expansion are not available in this mode.

### Global Settings

- `default_interval` (optional): The default monitoring interval for all files and directories. Specify in time format ("1s", "2m", "3h", "0.5s"). Decimal values are also allowed (e.g., "0.5s" is 0.5 seconds). If omitted, "1s" (1 second) will be used.
- `config_check_interval` (optional): The interval for checking the configuration file itself for changes. Specify in time format ("1s", "2m", "3h", "0.5s"). If the configuration file changes, it will be automatically reloaded. If omitted, "1s" (1 second) will be used.
- `log_file` (optional): The path to a log file where details of command execution will be recorded. If configured, command execution information (timestamp, path, TOML configuration content) for files or directories with `enable_log = true` will be logged to this file.
- `error_log_file` (optional): The path to an error log file where details of command execution failures will be recorded. If configured, detailed information such as error messages, executed commands, standard error output, and stack traces on command failure will be logged to this file.
- `suppression_log_file` (optional): The path to a log file where details of command execution suppression will be recorded. If configured, information (timestamp, file path, process pattern, matched process) when command execution is skipped due to `suppress_if_process` will be logged to this file.

### Time Period Settings

You can define time periods in the `[time_periods]` section (optional):

- Each time period is defined with a name.
- `start`: Start time (HH:MM format, e.g., "09:00")
- `end`: End time (HH:MM format, e.g., "17:00")
- Time periods spanning across midnight are also supported (e.g., `start = "23:00", end = "01:00"`).
- By specifying a time period name with the `time_period` parameter for each file, that file or directory will only be monitored within that specific time period.

Example:
```toml
[time_periods]
business_hours = { start = "09:00", end = "17:00" }  # Regular business hours
night_shift = { start = "23:00", end = "01:00" }     # Time period spanning across midnight
```

### Configuration Example

Refer to `examples/config.example.toml` for a complete example covering various use cases.

```toml
# Set default monitoring interval to 1 second
default_interval = "1s"

# Set configuration file self-check interval to 1 second
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
after_hours = { start = "18:00", end = "08:00" }  # Spanning across midnight

[files]
# Use default interval (checks every 1 second)
"document.txt" = { command = "cp document.txt document.txt.bak" }

# Specify custom interval (checks every 0.5 seconds)
"app.log" = { command = "notify-send 'Log Updated' 'New entries in app.log'", interval = "0.5s" }

# Specify custom interval (checks every 5 seconds)
"config.ini" = { command = "systemctl reload myapp", interval = "5s" }

# Monitor only during business hours
"report.txt" = { command = "python generate_report.py", time_period = "business_hours" }

# Monitor only outside business hours (e.g., for batch processing)
"batch.csv" = { command = "./process_batch.sh", time_period = "after_hours" }

# Enable logging for important files (records timestamp, file path, and configuration details)
"important.txt" = { command = "backup.sh", enable_log = true }
```

## How It Works

1. The tool reads the TOML configuration file.
2. It monitors the modification timestamps of all specified files.
3. When a file's timestamp changes, the associated command is executed.
4. The configuration file itself is also monitored; if it changes, it's automatically reloaded.
5. This process continuously repeats until stopped with Ctrl+C.

### Command Execution Handling

**Important**: Commands are executed **sequentially**.

- When a file change is detected and a command is executed, the next file check will not occur until that command completes (or times out after 30 seconds for foreground execution).
- For example, if a command for one file takes 25 seconds, monitoring of other files will be paused for those 25 seconds.
- Even if other files are updated during this time, they will not be detected until the currently running command completes (they will be detected in the next main loop after the command is done).
- The current implementation does not support parallelizing monitoring and execution for multiple files.

If a command requires a long execution time, it needs to be set up to run in the background within the command itself or launched as a separate process.

**Methods for Non-Blocking Execution**:
- **Linux/macOS**: Append `&` to the end of the command (e.g., `command = "long_task.sh &"`).
- **Windows**: Prefix the command with `start ` (e.g., `command = "start long_task.bat"`).

### Command Execution Output

The standard output and standard error of executed commands are displayed in the console in **real-time**:

- **Output Display**: The standard output and standard error of commands are sequentially displayed in the console during execution. Even for long-running commands, you can monitor their progress in real-time.
- **On Failure**: If a command fails (exit code other than 0), a message `Error: Command failed for '<file_path>' with exit code <code_number>` will be displayed.
- **Error Log File**: If `error_log_file` is configured, the error message and executed command upon failure will be recorded in the log file.

Commands executed in the foreground have a timeout of 30 seconds; exceeding this will result in a timeout error. For commands that require longer execution, please use background execution (using `&`). Commands executed in the background are not subject to the timeout limit, as `subprocess.run()` completes immediately.

## Concept

The priority is to keep TOML descriptions simple and easy to maintain.

## Use Cases

If you want to easily monitor file updates and operate with minimal hassle, use cat-file-watcher.
If you need to quickly toggle update monitoring on/off for scattered files, use cat-file-watcher.
If you want to leverage its unique features, use cat-file-watcher.
For more advanced features, consider other applications.
For TypeScript application development and similar tasks, a standard task runner is typically used.

## Development

### Environment Setup

Setting up the development environment:

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
  - All tests are designed for Linux.
  - The test code was generated and TDD'd by GitHub Copilot Coding Agent on a GitHub Actions (Linux Runner).

- Windows
  - Running tests in a Windows environment without WSL2 will frequently result in "test red" (failures), as the tests are designed for Linux.
  - To run tests in a Windows environment, use WSL2.
  - Specifically, install WSL2, prepare by running `wsl pip install -r dev-requirements.txt`, then execute `wsl pytest`.
  - Some "test red" results might occur with WSL2, which is acceptable. The benchmark is "test green" when TDDing by feeding issues to the agent.

## License

MIT License - See the LICENSE file for details.

*The English version of README.md is automatically generated by GitHub Actions using Gemini's translation based on README.ja.md.*

*Big Brother watched your files. Now the cat does. 🐱*
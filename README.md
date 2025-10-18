# cat-file-watcher

**File Change Monitoring Tool - Detects file changes and executes commands**

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
</p>

*Note: This document is mostly AI-generated. Issues were submitted to an agent to generate it. Some parts (Concept, Usage Scenarios) were written manually.*

## Quick Links
| Item | Link |
|------|--------|
| 📊 Development Status | [generated-docs/development-status](generated-docs/development-status.md) |

## Overview

This is a file monitoring tool that watches for changes in file timestamps and executes commands when a file is updated.

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

## Quick Start

Get started right away with minimal setup! It works with **just a single-line TOML file**:

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

That's it! It will monitor changes to `test.txt` and execute the command if a change is detected!

Try editing the file:
```bash
echo "テスト" >> test.txt
```

You will see "ファイルが変更されました" (File changed) displayed in the console.

**Note**: The single-line format above is a formal TOML notation using inline array tables. A more readable multi-line format is also available (see the [Configuration](#configuration) section for details).

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

# Configuration file change check interval
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

The configuration file requires a `[files]` section where each entry maps a file or directory path to a command:

- **Key**: The path to the file or directory to monitor (relative or absolute path)
  - For files: Executes the command when the file's modification time changes
  - For directories: Executes the command when the directory's modification time changes (e.g., adding or deleting files)
- **Value**: An object containing a `command` field for the shell command to execute
  - `command` (required): The shell command to execute when the file or directory changes
  - `interval` (optional): The monitoring interval for this file or directory. Specify in time format ("1s", "2m", "3h", "0.5s"). Decimal points are allowed (e.g., "0.5s" is 0.5 seconds). If omitted, `default_interval` will be used.
  - `suppress_if_process` (optional): A regular expression pattern to match against running process names. If a matching process is found, command execution is skipped. This is useful for preventing actions from triggering while certain programs, such as editors, are running.
  - `time_period` (optional): The name of the time period during which the file or directory should be monitored. Specify a time period name defined in the `[time_periods]` section. Monitoring will only occur within the specified time period.
  - `enable_log` (optional): If set to `true`, details of command execution will be logged to a file (default: `false`). The `log_file` setting must be configured in the global settings.
  - `cwd` (optional): Changes the working directory to the specified path before executing the command. This ensures that relative paths in the command are resolved from the specified directory.

### Global Settings

- `default_interval` (optional): The default monitoring interval for all files and directories. Specify in time format ("1s", "2m", "3h", "0.5s"). Decimal points are allowed (e.g., "0.5s" is 0.5 seconds). If omitted, "1s" (1 second) will be used.
- `config_check_interval` (optional): The interval for checking changes to the configuration file itself. Specify in time format ("1s", "2m", "3h", "0.5s"). If the configuration file changes, it will be automatically reloaded. If omitted, "1s" (1 second) will be used.
- `log_file` (optional): The path to the log file where details of command execution will be recorded. If set, command execution information (timestamp, path, TOML configuration content) for files or directories with `enable_log = true` will be recorded in this file.
- `error_log_file` (optional): The path to the error log file where details of command execution errors will be recorded. If set, detailed information such as error messages, executed commands, standard error output, and stack traces on command failure will be recorded in this file.
- `suppression_log_file` (optional): The path to the log file where details of command execution suppression will be recorded. If set, information (timestamp, file path, process pattern, matched process) when command execution is skipped due to `suppress_if_process` will be recorded in this file.

### Time Period Configuration

You can define time periods in the `[time_periods]` section (optional):

- Each time period is defined with a name
- `start`: Start time (HH:MM format, e.g., "09:00")
- `end`: End time (HH:MM format, e.g., "17:00")
- Time periods spanning across midnight are also supported (e.g., `start = "23:00", end = "01:00"`)
- By specifying a time period name using the `time_period` parameter for each file, that file or directory will only be monitored within that time period.

Example:
```toml
[time_periods]
business_hours = { start = "09:00", end = "17:00" }  # Regular business hours
night_shift = { start = "23:00", end = "01:00" }     # Time period spanning across midnight
```

### Configuration Example

For a complete example covering various use cases, refer to `examples/config.example.toml`.

```toml
# Set default monitoring interval to 1 second
default_interval = "1s"

# Set configuration file change check interval to 1 second
config_check_interval = "1s"

# Log file for command execution details (optional)
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
# Use default interval (checks every 1 second)
"document.txt" = { command = "cp document.txt document.txt.bak" }

# Specify custom interval (checks every 0.5 seconds)
"app.log" = { command = "notify-send 'Log Updated' 'New entries in app.log'", interval = "0.5s" }

# Specify custom interval (checks every 5 seconds)
"config.ini" = { command = "systemctl reload myapp", interval = "5s" }

# Monitor only during business hours
"report.txt" = { command = "python generate_report.py", time_period = "business_hours" }

# Monitor only after business hours (e.g., for batch processing)
"batch.csv" = { command = "./process_batch.sh", time_period = "after_hours" }

# Enable logging for important files (records timestamp, file path, and configuration content)
"important.txt" = { command = "backup.sh", enable_log = true }
```

## How It Works

1. The tool reads the TOML configuration file.
2. It monitors the modification timestamps of all specified files.
3. When a file's timestamp changes, it executes the associated command.
4. It also monitors the configuration file itself and automatically reloads it if changes are detected.
5. This process continuously repeats until stopped by Ctrl+C.

### Command Execution Handling

**Important**: Commands are executed **sequentially**.

- When a file change is detected and a command is executed, the next file check will not occur until that command completes (or times out after 30 seconds if run in the foreground).
- For example, if a command for one file takes 25 seconds, monitoring of other files will be paused for those 25 seconds.
- Even if other files are updated during this time, they will not be detected until the currently running command completes (they will be detected in the next main loop after the command finishes).
- The current implementation does not support parallelizing monitoring and execution for multiple files.

For commands that require a long execution time, it is necessary to run them in the background within the command itself or launch them as a separate process.

**Methods for Non-Blocking Execution**:
  - **Linux/macOS**: Append `&` to the end of the command (e.g., `command = "long_task.sh &"`)
  - **Windows**: Prefix the command with `start ` (e.g., `command = "start long_task.bat"`)

### Command Output

The standard output and standard error of executed commands are displayed on the console **in real-time**:

- **Output Display**: The standard output and standard error of commands are displayed incrementally on the console during execution. Even for long-running commands, you can see real-time progress.
- **On Failure**: If a command fails (exit code other than 0), a message `Error: Command failed for '<file_path>' with exit code <code_number>` will be displayed.
- **Error Log File**: If `error_log_file` is configured, error messages and executed commands on command failure will be recorded in the log file.

Commands executed in the foreground have a timeout of 30 seconds; exceeding this will result in a timeout error. For commands that require longer execution, please use background execution (using `&`). Commands executed in the background complete `subprocess.run()` immediately and are therefore not subject to the timeout limit.

## Concept

Prioritize simple and maintainable TOML descriptions.

## Usage Scenarios

- For easy file change monitoring and straightforward operation, use cat-file-watcher.
- For quickly toggling monitoring on/off for scattered files, use cat-file-watcher.
- For utilizing its unique features, use cat-file-watcher.
- For more advanced features, consider other applications.
- For TypeScript app development, etc., use a standard task runner.

## Development

### Environment Setup

To set up the development environment:

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

#### Automated Checks in CI/CD

When you create a Pull Request, GitHub Actions will automatically perform the following:

1. **Automatic Code Formatting**:
   - `ruff format src/` - Automatically formats the code (e.g., removes trailing spaces)
   - `ruff check --fix src/` - Fixes auto-fixable lint issues
   - If formatting causes changes, they will be automatically committed and pushed.

2. **Quality Checks**:
   - `ruff check src/` - Linter check for code quality
   - `ruff format --check src/` - Verifies code formatting

If checks fail even after automatic formatting, the PR merge will be blocked. It is recommended to run Ruff locally to format your code beforehand.

### Running Tests

```bash
# Run all tests
pytest

# Run tests with detailed output
pytest -v
```

## License

MIT License - See the LICENSE file for details

*Note: This README.md is automatically generated by GitHub Actions using Gemini's translation based on README.ja.md*
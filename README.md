# cat-file-watcher - Cat is watching your file -

**File Change Monitoring Tool - Detects file changes and executes commands**

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
  <a href="https://deepwiki.com/cat2151/cat-file-watcher"><img src="https://deepwiki.com/badge.svg" alt="Ask DeepWiki"></a>
</p>

*Note: This document is mostly AI-generated. It was produced by submitting issues to an agent. Some parts (Concept, Usage Scenarios, Test) are manually written.*

## Quick Links
| Item | Link |
|------|--------|
| 📊 Development Status | [generated-docs/development-status](generated-docs/development-status.md) |

## Overview

This is a file monitoring tool that watches for changes in file timestamps and executes commands when files are updated.

## Features

- Monitors multiple files simultaneously
- Executes custom commands on file changes
- Configurable via TOML settings file
- Lightweight and easy to use
- On Windows, can be configured to prevent spawned applications from stealing focus (or, more precisely, to immediately regain it).

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
files = [{path = "test.txt", command = "echo File changed!"}]
```

2. Create the file to be monitored:
```bash
touch test.txt
```

3. Start the file watcher:
```bash
python -m src --config-filename config.toml
```

That's all! It will monitor `test.txt` and execute the command when changes occur!

Try editing the file:
```bash
echo "Test" >> test.txt
```

"File changed!" will be displayed in the console.

**Note**: The single-line format above is a valid TOML syntax using inline array notation. A more readable multi-line format is also available (see the [Configuration](#configuration) section for details).

## Usage

Run the file watcher by specifying the configuration file:

```bash
python -m src --config-filename config.toml
```

Arguments:
- `--config-filename`: Path to the TOML configuration file (required)

## Configuration

Create a TOML configuration file to define the files to watch and the commands to execute:

```toml
# Default monitoring interval
# Time format: "1s" (1 second), "2m" (2 minutes), "3h" (3 hours), "0.5s" (0.5 seconds)
default_interval = "1s"

# Interval to check for changes in the configuration file itself
config_check_interval = "1s"

# File path for command execution logs (optional)
log_file = "command_execution.log"

# File path for error logs (optional)
# error_log_file = "error.log"

# File path for command execution suppression logs (optional)
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

The configuration file must contain a `[files]` section where each entry maps a file name to a command:

- **Key**: The path to the file or directory to monitor (relative or absolute path).
  - For files: Executes the command when the file's modification time changes.
  - For directories: Executes the command when the directory's modification time changes (e.g., file added/deleted).
- **Value**: An object with a `command` field containing the shell command to execute (normal mode), or an object with an `argv` field (no_focus mode).
  - `command` (required for normal mode): The shell command to execute when the file or directory changes. **Note**: Cannot be used if `no_focus=true`.
  - `argv` (required for no_focus mode): A required array field when `no_focus=true`. Specifies the executable name and arguments as an array. Example: `argv = ["notepad.exe", "file.txt"]`.
  - `interval` (optional): The monitoring interval for this specific file or directory. Specified in time format ("1s", "2m", "3h", "0.5s"). Decimal values are allowed (e.g., "0.5s" is 0.5 seconds). If omitted, `default_interval` is used.
  - `suppress_if_process` (optional): A regular expression pattern to match against running process names. If a matching process is found, command execution is skipped. Useful for preventing actions from being triggered when specific programs like editors are running.
  - `time_period` (optional): The name of a time period during which to monitor the file or directory. Specifies a time period name defined in the `[time_periods]` section. Monitoring will only occur within the specified time period.
  - `enable_log` (optional): If set to `true`, detailed command execution will be logged to the log file (default: `false`). Requires `log_file` to be configured in the global settings.
  - `cwd` (optional): Changes the working directory to the specified path before executing the command. This ensures that relative paths within the command are resolved from the specified directory.
  - `no_focus` (optional): If set to `true`, the command is executed without stealing focus (default: `false`). **Windows only** - The command is launched asynchronously (the tool does not wait for completion), and the window is displayed but not activated, preventing focus theft. Uses `shell=False`. On non-Windows platforms, it will display a warning and fall back to normal execution. **Important**: If `no_focus=true`, the `command` field cannot be used; instead, the `argv` array field is required. Example: `argv = ["notepad.exe", "file.txt"]`.

### Global Settings

- `default_interval` (optional): The default monitoring interval for all files and directories. Specified in time format ("1s", "2m", "3h", "0.5s"). Decimal values are allowed (e.g., "0.5s" is 0.5 seconds). If omitted, "1s" (1 second) is used.
- `config_check_interval` (optional): The interval for checking changes in the configuration file itself. Specified in time format ("1s", "2m", "3h", "0.5s"). The configuration file is automatically reloaded if it changes. If omitted, "1s" (1 second) is used.
- `log_file` (optional): The path to a log file where detailed command execution information will be recorded. If set, command execution details (timestamp, path, TOML configuration content) for files or directories with `enable_log = true` will be logged to this file.
- `error_log_file` (optional): The path to an error log file where detailed command execution errors will be recorded. If set, detailed information such as error messages, executed commands, standard error output, and stack traces will be logged to this file upon command failure.
- `suppression_log_file` (optional): The path to a log file where details of command execution suppression will be recorded. If set, information (timestamp, file path, process pattern, matched process) when command execution is skipped due to `suppress_if_process` will be logged to this file.
- `color_scheme` (optional): Color scheme for terminal output. Can be `monokai` (default) or `classic`. For custom colors, specify `green`, `yellow`, `red` in the `[color_scheme]` table using `#RRGGBB`, `R,G,B`, `R;G;B`, `38;2;R;G;B`, or ANSI escape sequence format (e.g., `\x1b[38;2;255;60;80m`).

### Auto Update Settings

The `[auto_update]` section (optional) allows you to configure automatic update checks for the git repository. If configured, a background thread will periodically check for updates in the remote repository:

- `enabled` (optional): If set to `true`, `git pull` will be executed and the process will automatically restart if an update is found. Default is `false` (dry-run mode: only notifies of updates but does not actually pull or restart).
- `interval` (optional): The interval for checking updates. Specified in time format ("1s", "2m", "3h", etc.). Default is `"1h"` (1 hour).

If the `[auto_update]` table itself is not present in the configuration file, the background thread for auto-updates will not be started. Also, if the current branch does not have a remote tracking branch (`@{u}`) configured, it will be considered "no updates," and `git pull` will not be executed.

```toml
[auto_update]
enabled = true   # Set to false (default) for dry-run (notification only)
interval = "1h"  # Update check interval (default: 1 hour)
```

### Time Period Configuration

The `[time_periods]` section (optional) allows you to define time periods:

- Each time period is defined with a name.
- `start`: Start time (HH:MM format, e.g., "09:00").
- `end`: End time (HH:MM format, e.g., "17:00").
- Supports time periods spanning across days (e.g., `start = "23:00", end = "01:00"`).
- By specifying a `time_period` parameter per file, that file or directory will only be monitored within that time period.

Example:
```toml
[time_periods]
business_hours = { start = "09:00", end = "17:00" }  # Normal business hours
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

# Command execution suppression log file (optional)
# suppression_log_file = "suppression.log"

# Time period definitions
[time_periods]
business_hours = { start = "09:00", end = "17:00" }
after_hours = { start = "18:00", end = "08:00" }  # Spans across days

[files]
# Uses default interval (checks every 1 second)
"document.txt" = { command = "cp document.txt document.txt.bak" }

# Specifies custom interval (checks every 0.5 seconds)
"app.log" = { command = "notify-send 'Log Updated' 'New entries in app.log'", interval = "0.5s" }

# Specifies custom interval (checks every 5 seconds)
"config.ini" = { command = "systemctl reload myapp", interval = "5s" }

# Monitors only during business hours
"report.txt" = { command = "python generate_report.py", time_period = "business_hours" }

# Monitors only during after-hours (e.g., for batch processing)
"batch.csv" = { command = "./process_batch.sh", time_period = "after_hours" }

# Enables logging for important files (records timestamp, file path, and configuration content)
"important.txt" = { command = "backup.sh", enable_log = true }
```

## How It Works

1. The tool reads the TOML configuration file.
2. It monitors the modification timestamps of all specified files.
3. When a file's timestamp changes, the associated command is executed.
4. The configuration file itself is also monitored and automatically reloaded if it changes.
5. This process continuously repeats until stopped with Ctrl+C.

### Command Execution Mechanism

**Important**: Commands are executed **sequentially**.

- When a file change is detected and a command is executed, the next file check will not occur until that command completes (or times out after 30 seconds for foreground execution).
- For example, if a command for one file takes 25 seconds, monitoring for other files will be temporarily paused during those 25 seconds.
- Even if other files are updated during this time, they will not be detected until the currently running command completes (they will be detected in the next main loop after the command finishes).
- The current implementation does not support parallelizing monitoring and execution for multiple files.

For commands that require long execution times, you need to implement background execution within the command or launch it as a separate process.

**Non-blocking Execution Methods**:
- **Linux/macOS**: Append `&` to the command (e.g., `command = "long_task.sh &"`).
- **Windows**: Prefix the command with `start ` (e.g., `command = "start long_task.bat"`).

### Command Execution Output

The standard output and standard error output of executed commands are displayed in the console **in real-time**:

- **Output Display**: The standard output and standard error output of commands are progressively displayed in the console during execution. You can check the progress of long-running commands in real-time.
- **On Failure**: If a command fails (exit code other than 0), a message like `Error: Command failed for '<file_path>' with exit code <code_>` will be displayed.
- **Error Log File**: If `error_log_file` is configured, detailed error messages and executed commands upon command failure will be logged to this file.

Foreground executed commands have a 30-second timeout. If this is exceeded, a timeout error will occur. For commands that require longer execution, please use background execution (using `&`). Commands executed in the background are not subject to the timeout limit because `subprocess.run()` completes immediately.

## Concept

Prioritizes simple and maintainable TOML descriptions.

## Usage Scenarios

For easy file update monitoring and simple operation, use cat-file-watcher.

When you want to quickly enable/disable monitoring for scattered files, use cat-file-watcher.

When you want to leverage its unique features, use cat-file-watcher.

For more advanced features, use other applications.

For TypeScript app development, etc., use a standard task runner.

## Development

### Environment Setup

Setting up the development environment:

```bash
# Install dependencies (for runtime)
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

# Fix automatically rectifiable issues
ruff check --fix src/

# Check code format
ruff format --check src/

# Apply code format
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
  - The GitHub Copilot Coding Agent generated the test code and performed TDD on GitHub Actions (Linux Runner).

- Windows
  - Running tests in a Windows environment without WSL2 will result in many test failures (red tests) because the tests are designed for Linux.
  - To run tests in a Windows environment, use WSL2.
  - Specifically, install WSL2, then prepare with `wsl pip install -r dev-requirements.txt`, and then run `wsl pytest`.
  - Some tests may still fail (show red) in WSL2, but this is acceptable. The criterion is that if TDD with the agent results in green tests, it's considered okay.

## License

MIT License - Refer to the LICENSE file for details.

*The English README.md is automatically generated by GitHub Actions using Gemini's translation based on README.ja.md.*

*Big Brother watched your files. Now the cat does. 🐱*
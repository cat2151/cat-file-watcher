# cat-file-watcher - Cat is watching your file -

**File Change Monitoring Tool - Detects file changes and executes commands**

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
</p>

*This document is largely AI-generated. It was produced by submitting issues to an agent. Some parts (Concept, Usage Scenarios, Test) were written manually.

## Quick Links
| Item | Link |
|------|--------|
| 📊 Development Status | [generated-docs/development-status](generated-docs/development-status.md) |

## Overview

This is a file monitoring tool that watches for changes in file timestamps and executes commands when files are updated.

## Features

- Monitor multiple files simultaneously
- Execute custom commands on file changes
- Configurable via TOML configuration file
- Lightweight and easy to use
- On Windows, can be configured not to steal focus from the running application (or more accurately, to immediately regain focus)

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

## Quickstart

Get started now with minimal configuration! It works with **just one line in a TOML file**:

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

That's it! It will monitor changes to `test.txt` and execute a command if changes are detected!

Try editing the file:
```bash
echo "Test" >> test.txt
```

"File changed!" will be displayed on the console.

**Note**: The single-line format above is a formal TOML notation using inline array syntax. A more readable multi-line format is also available (see the [Configuration](#configuration) section for details).

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

The configuration file must contain a `[files]` section where each entry maps a file name to a command:

- **Key**: The path to the file or directory to monitor (relative or absolute path)
  - For files: Executes the command when the file's modification timestamp changes.
  - For directories: Executes the command when the directory's modification timestamp changes (e.g., file added/deleted).
- **Value**: An object containing a `command` field to be executed.
  - `command` (required): The shell command to execute when the file or directory changes.
  - `interval` (optional): The monitoring interval for this file or directory. Specify in time format ("1s", "2m", "3h", "0.5s"). Decimal values are allowed (e.g., "0.5s" for 0.5 seconds). If omitted, `default_interval` is used.
  - `suppress_if_process` (optional): A regular expression pattern to match against running process names. If a matching process is found, command execution is skipped. This is useful for preventing actions from triggering while specific programs, such as editors, are running.
  - `time_period` (optional): The name of a time period during which the file or directory should be monitored. Specify a time period name defined in the `[time_periods]` section. Monitoring will only occur within the specified time period.
  - `enable_log` (optional): If set to `true`, detailed command execution information will be recorded in the log file (default: `false`). The `log_file` setting in global configuration is required.
  - `cwd` (optional): Changes the working directory to the specified path before executing the command. This ensures relative paths within the command are resolved from the specified directory.
  - `no_focus` (optional): If set to `true`, the command is executed without stealing focus (default: `false`). **Windows-only** - The command is launched asynchronously (the tool does not wait for it to complete), and its window is displayed but not activated, preventing focus theft. Uses `shell=False` and splits the command by spaces. On non-Windows platforms, it will display a warning and fall back to normal execution. Note: Shell features like pipes, redirects, and environment variable expansion are not available in this mode.

### Global Settings

- `default_interval` (optional): Default monitoring interval for all files and directories. Specify in time format ("1s", "2m", "3h", "0.5s"). Decimal values are allowed (e.g., "0.5s" for 0.5 seconds). If omitted, "1s" (1 second) will be used.
- `config_check_interval` (optional): Interval for checking changes to the configuration file itself. Specify in time format ("1s", "2m", "3h", "0.5s"). The configuration file will be automatically reloaded if it changes. If omitted, "1s" (1 second) will be used.
- `log_file` (optional): Path to the log file where command execution details are recorded. If set, command execution information (timestamp, path, TOML configuration content) for files or directories with `enable_log = true` will be recorded in this file.
- `error_log_file` (optional): Path to the error log file where details of command execution errors are recorded. If set, detailed information such as error messages, executed commands, standard error output, and stack traces when a command fails will be recorded in this file.
- `suppression_log_file` (optional): Path to the log file where details of command execution suppressions are recorded. If set, information (timestamp, file path, process pattern, matched process) when a command execution is skipped due to `suppress_if_process` will be recorded in this file.

### Time Period Settings

You can define time periods in the `[time_periods]` section (optional):

- Each time period is defined with a name.
- `start`: Start time (HH:MM format, e.g., "09:00")
- `end`: End time (HH:MM format, e.g., "17:00")
- Time periods spanning across midnight are also supported (e.g., `start = "23:00", end = "01:00"`).
- If you specify a time period name using the `time_period` parameter for each file, that file or directory will only be monitored within that time period.

Example:
```toml
[time_periods]
business_hours = { start = "09:00", end = "17:00" }  # Normal hours
night_shift = { start = "23:00", end = "01:00" }     # Spans across midnight
```

### Configuration Example

For a complete example of various use cases, please refer to `examples/config.example.toml`.

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

# Monitor only outside business hours (e.g., for batch processing)
"batch.csv" = { command = "./process_batch.sh", time_period = "after_hours" }

# Enable logging for important files (records timestamp, file path, configuration content)
"important.txt" = { command = "backup.sh", enable_log = true }
```

## How It Works

1. The tool loads the TOML configuration file.
2. It monitors the modification timestamps of all specified files.
3. When a file's timestamp changes, the associated command is executed.
4. The configuration file itself is also monitored and automatically reloaded if it changes.
5. This process continuously repeats until stopped by Ctrl+C.

### Command Execution Processing Method

**Important**: Commands are executed **sequentially**.

- When a file change is detected and a command is executed, the next file will not be checked until that command completes (or times out after 30 seconds for foreground execution).
- For example, if a command for one file takes 25 seconds, monitoring of other files will be paused for those 25 seconds.
- If other files are updated during this time, they will not be detected until the current command finishes (they will be detected in the next main loop after the command completes).
- The current implementation does not support parallelizing the monitoring and execution of multiple files.

For commands that require a long execution time, you will need to implement background execution within the command or launch it as a separate process.

**Methods for Non-Blocking Execution**:
- **Linux/macOS**: Append `&` to the end of the command (e.g., `command = "long_task.sh &"`).
- **Windows**: Prepend `start ` to the command (e.g., `command = "start long_task.bat"`).

### Command Execution Output

The standard output and standard error output of the executed command are displayed in the console **in real-time**:

- **Output Display**: The standard output and standard error of the command are displayed sequentially in the console during execution. Even for long-running commands, progress can be monitored in real-time.
- **On Failure**: If a command fails (exit code other than 0), a message `Error: Command failed for '<file_path>' with exit code <code_number>` will be displayed.
- **Error Log File**: If `error_log_file` is configured, the error message and executed command upon failure will be recorded in the log file.

Foreground commands have a timeout of 30 seconds, after which a timeout error will occur. For commands that require longer execution, please use background execution (using `&`). Commands executed in the background will not be subject to timeout limitations as `subprocess.run()` will complete immediately.

## Concept

Prioritize simple and maintainable TOML descriptions.

## Usage Scenarios

Use cat-file-watcher if you want to easily monitor file updates and operate it with minimal effort.

Use cat-file-watcher if you want to quickly enable/disable monitoring for scattered files.

Use cat-file-watcher if you want to leverage its unique features.

For more advanced functionalities, consider other applications.

For TypeScript application development and similar tasks, a standard task runner is typically used.

## Development

### Environment Setup

Setting up the development environment:

```bash
# Install dependencies (for runtime)
pip install -r requirements.txt

# Install development dependencies (including Ruff)
pip install -r dev-requirements.txt
```

### Code Quality Check

This project uses [Ruff](https://docs.astral.sh/ruff/) to maintain code quality.

#### Running Ruff

```bash
# Run linter checks
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
  - All tests are designed for Linux.
  - GitHub Copilot Coding Agent generated the test code and performed TDD on GitHub Actions (Linux Runner).

- Windows
  - Running tests directly on Windows without WSL2 will frequently result in "test red" (failures), as the tests are designed for Linux.
  - To run tests on Windows, use WSL2.
  - Specifically, install WSL2, then prepare by running `wsl pip install -r dev-requirements.txt`, and finally execute `wsl pytest`.
  - Some tests might still be "test red" even with WSL2, but this is acceptable. The criterion is that if TDD resulted in "test green" when an issue was submitted to the agent, it's considered okay.

## License

MIT License - See the LICENSE file for details

*The English README.md is automatically generated by GitHub Actions using Gemini's translation based on README.ja.md*

*Big Brother watched your files. Now the cat does. 🐱*
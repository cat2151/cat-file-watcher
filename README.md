# cat-file-watcher

**File Change Watcher - Detects file changes and executes commands**

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
</p>

※A significant portion of this document is AI-generated, specifically by prompting an agent with issues. Some parts (concept, usage scenarios) are manually written.

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

The configuration file requires a `[files]` section where each entry maps a filename to a command:

- **Key**: Path to the file or directory to monitor (relative or absolute path)
  - For files: The command is executed when the file's modification time changes.
  - For directories: The command is executed when the directory's modification time changes (e.g., files added/deleted).
- **Value**: An object containing a `command` field and other optional parameters:
  - `command` (Required): The shell command to execute when the file or directory changes.
  - `interval` (Optional): The monitoring interval for this specific file or directory. Specified in time format ("1s", "2m", "3h", "0.5s"). Decimals are also supported (e.g., "0.5s" for 0.5 seconds). If omitted, `default_interval` is used.
  - `suppress_if_process` (Optional): A regular expression pattern matching running process names. If a matching process is found, command execution is skipped. This is useful for preventing actions from triggering while specific programs like editors are running.
  - `time_period` (Optional): The name of the time period during which the file or directory should be monitored. Specifies a time period name defined in the `[time_periods]` section. Monitoring only occurs within the specified time period.
  - `enable_log` (Optional): If set to `true`, detailed command execution information is recorded in the log file (default: `false`). The `log_file` setting must be configured in the global settings.
  - `cwd` (Optional): Changes the working directory to the specified path before executing the command. This ensures relative paths within the command are resolved from the specified directory.

### Global Settings

- `default_interval` (Optional): The default monitoring interval for all files and directories. Specified in time format ("1s", "2m", "3h", "0.5s"). Decimals are also supported (e.g., "0.5s" for 0.5 seconds). If omitted, "1s" (1 second) is used.
- `config_check_interval` (Optional): The interval at which the configuration file itself is checked for changes. Specified in time format ("1s", "2m", "3h", "0.5s"). If the configuration file is modified, it will be automatically reloaded. If omitted, "1s" (1 second) is used.
- `log_file` (Optional): Path to the log file for recording detailed command execution information. If configured, command execution details (timestamp, path, TOML configuration content) for files or directories with `enable_log = true` will be recorded in this file.
- `error_log_file` (Optional): Path to the error log file for recording detailed command execution errors. If configured, detailed information such as error messages upon command failure, the executed command, standard error output, and stack traces will be recorded in this file.
- `suppression_log_file` (Optional): Path to the log file for recording detailed command execution suppressions. If configured, information when command execution is skipped due to `suppress_if_process` (timestamp, file path, process pattern, matched process) will be recorded in this file.

### Time Period Settings

You can define time periods in the `[time_periods]` section (optional):

- Each time period is defined with a name.
- `start`: Start time (HH:MM format, e.g., "09:00")
- `end`: End time (HH:MM format, e.g., "17:00")
- Supports time periods that span across days (e.g., `start = "23:00", end = "01:00"`)
- If you specify a time period name with the `time_period` parameter for a file, that file or directory will only be monitored during that specified time period.

Example:
```toml
[time_periods]
business_hours = { start = "09:00", end = "17:00" }  # Normal time period
night_shift = { start = "23:00", end = "01:00" }     # Time period spanning across days
```

### Configuration Example

For a complete example of various use cases, refer to `examples/config.example.toml`.

```toml
# Set default monitoring interval to 1 second
default_interval = "1s"

# Set configuration file change check interval to 1 second
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

# Monitors only outside business hours (e.g., for batch processing)
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

### Command Execution Method

**Important**: Commands are executed **sequentially**.

- When a file change is detected and a command is executed, the next file will not be checked until that command completes (or times out after 30 seconds).
- For example, if a command for one file takes 25 seconds, monitoring for other files will be temporarily paused for those 25 seconds.
- Even if other files are updated during this time, they will not be detected until the currently running command completes (they will be detected in the next main loop after the command finishes).
- The current implementation does not support parallelizing monitoring and execution of multiple files.

For commands that require long execution times, it is necessary to run them in the background or launch them as a separate process within the command itself.

**Methods for non-blocking execution**:
- **Linux/macOS**: Add `&` to the end of the command (e.g., `command = "long_task.sh &"`)
- **Windows**: Add `start ` to the beginning of the command (e.g., `command = "start long_task.bat"`)

### Output During Command Execution

Standard output and standard error output of the executed commands are displayed **in real-time** in the console:

- **Output Display**: The standard output and standard error output of commands are displayed sequentially in the console during execution. Even for long-running commands, you can check the progress in real-time.
- **On Failure**: If a command fails (with a non-zero exit code), a message like `Error: Command failed for '<file path>' with exit code <code_>` will be displayed.
- **Error Log File**: If `error_log_file` is configured, error messages and the executed command upon command failure will be recorded in the log file.

Command execution is set to a timeout of 30 seconds; exceeding this will result in a timeout error.

## Concept

Prioritize simple and maintainable TOML descriptions.

## Usage Scenarios

For easy file change monitoring and straightforward operation, use cat-file-watcher.

If you want to quickly enable/disable monitoring for scattered files, use cat-file-watcher.

If you want to use the various features unique to this tool, use cat-file-watcher.

If you want to use more advanced features, use other applications.

For TypeScript application development, use standard task runners.

## Development

### Environment Setup

Setting up the development environment:

```bash
# Install dependencies for runtime environment
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

# Fix automatically fixable issues
ruff check --fix src/

# Code format check
ruff format --check src/

# Apply code formatting
ruff format src/
```

#### Using Pre-commit Hooks (Optional)

For automated formatting on every commit, you can use pre-commit hooks:

```bash
# Install pre-commit
pip install pre-commit

# Install the git hooks
pre-commit install

# (Optional) Run on all files manually
pre-commit run --all-files
```

Once installed, pre-commit will automatically run `ruff format` and `ruff check --fix` before each commit, ensuring your code is always properly formatted.

**Note**: Pre-commit hooks work in local development environments. GitHub Copilot Agents and other CI/CD bots may not use pre-commit hooks, so always verify formatting before creating a PR.

### Running Tests

```bash
# Run all tests
pytest

# Run tests with detailed output
pytest -v
```

## License

MIT License - See the LICENSE file for details

※This README.md is automatically generated by GitHub Actions using Gemini's translation based on README.ja.md.
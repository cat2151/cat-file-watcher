# cat-file-watcher

**File Change Monitoring Tool - Detects file changes and executes commands**

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
</p>

## Quick Links
| Item | Link |
|------|--------|
| 📊 Development Status | [generated-docs/daily-summaries](generated-docs/daily-summaries) |

## Overview

This is a file monitoring tool that watches for changes in file timestamps and executes a command when a file is updated.

## Features

- Monitor multiple files simultaneously
- Execute custom commands on file changes
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

## Usage

Run the file watcher by specifying a configuration file:

```bash
python src/cat_file_watcher.py --config-filename config.toml
```

Arguments:
- `--config-filename`: Path to the TOML configuration file (required)

## Configuration

Create a TOML configuration file to define the files to watch and the commands to execute:

```toml
# Default monitoring interval (in milliseconds)
default_interval = 1000

# Configuration file self-check interval (in milliseconds)
config_check_interval = 1000

# Time period definitions (optional)
[time_periods]
business_hours = { start = "09:00", end = "17:00" }
night_shift = { start = "23:00", end = "01:00" }

[files]
"myfile.txt" = { command = "echo 'File changed!'" }
"script.py" = { command = "python -m pytest tests/", interval = 2000 }
"src/main.py" = { command = "make build", suppress_if_process = "vim|emacs|code" }
"batch.csv" = { command = "./process.sh", time_period = "night_shift" }
```

### Configuration Format

The configuration file requires a `[files]` section where each entry maps a filename to a command:

- **Key**: Path to the file to monitor (relative or absolute)
- **Value**: An object containing a `command` field, which is the shell command to execute
  - `command` (required): The shell command to execute when the file changes
  - `interval` (optional): Monitoring interval for this file (in milliseconds). If omitted, `default_interval` will be used.
  - `suppress_if_process` (optional): A regular expression pattern to match against running process names. If a matching process is found, the command execution will be skipped. This is useful for preventing actions from being triggered when certain programs, such as editors, are running.
  - `time_period` (optional): Name of the time period during which to monitor this file. References a time period defined in the `[time_periods]` section. The file will only be monitored during the specified time period.

### Global Settings

- `default_interval` (optional): The default monitoring interval for all files (in milliseconds). If omitted, 1000ms (1 second) will be used.
- `config_check_interval` (optional): The self-check interval for the configuration file (in milliseconds). If the configuration file changes, it will be reloaded automatically. If omitted, 1000ms (1 second) will be used.

### Time Period Settings

You can define time periods in the `[time_periods]` section (optional):

- Each time period is defined with a name
- `start`: Start time in HH:MM format (e.g., "09:00")
- `end`: End time in HH:MM format (e.g., "17:00")
- Supports time periods spanning across midnight (e.g., `start = "23:00", end = "01:00"`)
- Files can specify a `time_period` parameter to only be monitored during that time period

Example:
```toml
[time_periods]
business_hours = { start = "09:00", end = "17:00" }  # Normal time period
night_shift = { start = "23:00", end = "01:00" }     # Spans midnight
```

### Configuration Examples

Refer to `config.example.toml` for complete examples of various use cases.

```toml
# Set default monitoring interval to 1 second
default_interval = 1000

# Set configuration file self-check interval to 1 second
config_check_interval = 1000

# Define time periods
[time_periods]
business_hours = { start = "09:00", end = "17:00" }
after_hours = { start = "18:00", end = "08:00" }  # Spans midnight

[files]
# Use default interval (check every 1 second)
"document.txt" = { command = "cp document.txt document.txt.bak" }

# Specify custom interval (check every 500ms)
"app.log" = { command = "notify-send 'Log Updated' 'New entries in app.log'", interval = 500 }

# Specify custom interval (check every 5 seconds)
"config.ini" = { command = "systemctl reload myapp", interval = 5000 }

# Monitor only during business hours
"report.txt" = { command = "python generate_report.py", time_period = "business_hours" }

# Monitor only during after hours (for batch processing)
"batch.csv" = { command = "./process_batch.sh", time_period = "after_hours" }
```

## How it Works

1. The tool reads the TOML configuration file.
2. It monitors the modification timestamps of all specified files.
3. When a file's timestamp changes, it executes the associated command.
4. It also monitors the configuration file itself and reloads it automatically if changes are detected.
5. This process continuously repeats until stopped with Ctrl+C.

## License

MIT License - See the LICENSE file for details

*This README.md is automatically generated by GitHub Actions using Gemini's translation based on README.ja.md.
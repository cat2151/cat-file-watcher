# cat-file-watcher

**A file monitoring tool that watches files for changes and executes commands when their timestamps are updated.**

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
</p>

## Quick Links
| Item | Link |
|------|--------|
| 📊 Development Status | [generated-docs/daily-summaries](generated-docs/daily-summaries) |

## Features

- Monitor multiple files simultaneously
- Execute custom commands when files change
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

## Usage

Run the file watcher with a configuration file:

```bash
python src/cat_file_watcher.py --config-filename config.toml
```

Arguments:
- `--config-filename`: Path to the TOML configuration file (required)

## Configuration

Create a TOML configuration file that defines the files to monitor and commands to execute:

```toml
[files]
"myfile.txt" = { command = "echo 'File changed!'" }
"script.py" = { command = "python -m pytest tests/" }
```

### Configuration Format

The configuration file must contain a `[files]` section where each entry maps a filename to a command:

- **Key**: The path to the file to monitor (can be relative or absolute)
- **Value**: An object with a `command` field containing the shell command to execute

### Example Configuration

See `config.example.toml` for a complete example with various use cases.

```toml
[files]
"document.txt" = { command = "cp document.txt document.txt.bak" }
"app.log" = { command = "notify-send 'Log Updated' 'New entries in app.log'" }
```

## How It Works

1. The tool loads the TOML configuration file
2. It monitors the modification timestamps of all specified files
3. When a file's timestamp changes, it executes the associated command
4. This process repeats continuously until stopped with Ctrl+C

## License

MIT License - see LICENSE file for details
# VSCode Configuration for cat-file-watcher

This directory contains VSCode settings for the cat-file-watcher project.

## Required Extensions

Please install the following extensions for the best development experience:

1. **Python** (ms-python.python)
   - Official Python extension
   - Provides IntelliSense, linting, debugging, and more

2. **Pylance** (ms-python.vscode-pylance)
   - Fast language server for Python
   - Provides advanced type checking and auto-completion

3. **Ruff** (charliermarsh.ruff)
   - Modern, fast Python linter and formatter
   - Replaces flake8, black, and isort

4. **EditorConfig for VS Code** (editorconfig.editorconfig)
   - Applies EditorConfig settings

## Installation

Install all extensions at once using the command palette (Ctrl+Shift+P or Cmd+Shift+P):

```
Extensions: Show Recommended Extensions
```

Or install them individually from the Extensions marketplace.

## Development Dependencies

Install development dependencies:

```bash
pip install -r dev-requirements.txt
```

This will install:
- ruff: Linter and formatter
- mypy: Optional type checker
- types-toml: Type stubs for toml

## Features

### Auto-formatting on Save

Python files are automatically formatted when you save them using Ruff formatter.

### Linting

Code is continuously linted with Ruff. Issues appear in the Problems panel.

### Test Discovery

Tests are automatically discovered and can be run from the Test Explorer.

### Import Organization

Imports are automatically sorted and organized on save.

## Settings Overview

- **Line Length**: 120 characters
- **Indent**: 4 spaces for Python
- **Line Ending**: LF (Unix style)
- **Trailing Whitespace**: Automatically removed
- **Final Newline**: Automatically added

## Manual Commands

### Check code:
```bash
ruff check src/ tests/
```

### Fix issues automatically:
```bash
ruff check --fix src/ tests/
```

### Format code:
```bash
ruff format src/ tests/
```

### Run tests:
```bash
pytest tests/
```

## Troubleshooting

### Extensions not working?

1. Reload VSCode window (Ctrl+Shift+P → "Developer: Reload Window")
2. Check that Python interpreter is selected (bottom-left corner)
3. Verify extensions are installed and enabled

### Linting not showing errors?

1. Open Output panel (View → Output)
2. Select "Python" or "Ruff" from the dropdown
3. Check for error messages

## Learn More

- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [VSCode Python Documentation](https://code.visualstudio.com/docs/python/python-tutorial)
- [EditorConfig Documentation](https://editorconfig.org/)

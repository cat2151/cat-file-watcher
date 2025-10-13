# GitHub Copilot Instructions for cat-file-watcher

## Project Overview

cat-file-watcher is a Python-based file change monitoring tool that watches for file timestamp changes and executes commands when files are updated. It's a lightweight, configurable tool using TOML for configuration.

## Code Style and Standards

### Python Style

- Use Python 3.12+ compatible syntax
- Follow PEP 8 style guidelines
- Use descriptive variable and function names
- Include shebang `#!/usr/bin/env python3` at the top of executable scripts
- Support both relative and absolute imports for maximum compatibility:
  ```python
  try:
      from .module import Class
  except ImportError:
      from module import Class
  ```

### Documentation

- Add docstrings to all classes and public methods
- Use triple-quoted strings with clear descriptions
- Include Args, Returns, and Raises sections in docstrings when applicable
- Example format:
  ```python
  def method_name(self, param):
      """Brief description.

      Args:
          param: Description of parameter

      Returns:
          type: Description of return value

      Raises:
          ErrorType: Description of when error is raised
      """
  ```

### Comments

- Add comments to explain complex logic or non-obvious behavior
- Use inline comments sparingly and only when necessary
- Prefer self-documenting code over excessive comments

## Testing

### Test Framework

- Use Python's built-in `unittest` framework for all tests
- Place all test files in the `tests/` directory
- Name test files with prefix `test_` (e.g., `test_feature.py`)
- Use descriptive test method names starting with `test_`

### Test Structure

- Create a test class inheriting from `unittest.TestCase`
- Use `setUp()` for test fixtures
- Use `tearDown()` for cleanup
- Use `tempfile.mkdtemp()` for temporary test directories
- Clean up temporary files after tests

### Test Coverage

- Write tests for all new features and bug fixes
- Include both positive and negative test cases
- Test edge cases and error conditions
- Validate error messages and exception handling

## Configuration

### TOML Configuration

- Use TOML format for all configuration files
- Configuration should support:
  - `default_interval`: Default monitoring interval in milliseconds
  - `config_check_interval`: Config file self-check interval in milliseconds
  - `[files]` section: File-to-command mappings
- File-specific settings include:
  - `command` (required): Shell command to execute
  - `interval` (optional): Custom interval in milliseconds
  - `suppress_if_process` (optional): Regex pattern for process suppression

### Interval Handling

- All intervals are specified in milliseconds in configuration
- Convert milliseconds to seconds using float division: `interval_ms / 1000.0`
- This ensures proper float results (e.g., 500ms -> 0.5s, 250ms -> 0.25s)

## Architecture

### Module Organization

- `cat_file_watcher.py`: Main FileWatcher class and monitoring logic
- `config_loader.py`: TOML configuration loading and parsing
- `command_executor.py`: Shell command execution with process suppression
- `process_detector.py`: Process detection for command suppression
- `__main__.py`: Entry point for command-line execution

### Design Principles

- Keep modules focused on single responsibilities
- Use static methods for utility functions that don't require instance state
- Handle errors gracefully with informative error messages
- Use `print()` for user-facing output and logging

## Error Handling

### Configuration Errors

- Catch `FileNotFoundError` for missing config files
- Catch `toml.TomlDecodeError` for invalid TOML syntax
- Print clear error messages to users
- Exit with `sys.exit(1)` for fatal errors

### Runtime Errors

- Handle `OSError` for file system operations
- Handle `subprocess.TimeoutExpired` for command timeouts (30 seconds)
- Catch general exceptions and provide helpful error messages
- Continue operation when non-fatal errors occur

## Security

### Command Execution

- Use `subprocess.run()` with appropriate parameters
- Set `shell=True` for shell command execution (required for this tool's purpose)
- Use `timeout=30` to prevent hanging commands
- Capture both stdout and stderr with `capture_output=True`

### Input Validation

- Validate TOML configuration structure
- Handle invalid regex patterns gracefully
- Sanitize file paths appropriately

## Dependencies

### Required Packages

- `toml>=0.10.2`: TOML configuration parsing
- `psutil>=5.9.0`: Process detection and management

### Adding Dependencies

- Update `requirements.txt` with version constraints
- Document new dependencies in README if user-facing
- Ensure cross-platform compatibility

## Compatibility

### Platform Support

- Support Linux, macOS, and Windows
- Use `os.path` for cross-platform file path handling
- Test process detection on multiple platforms

### Python Version

- Maintain compatibility with Python 3.6+
- Use features available in older Python versions when possible
- Document minimum Python version requirements

## Development Workflow

### Issue Tracking

- Use issue notes in `issue-notes/` directory for problem tracking
- Create markdown files named `{issue-number}.md`
- Document conclusions, verification steps, and changes made

### Documentation

- Keep README.md and README.ja.md in sync
- Update examples when configuration format changes
- Document all configuration options clearly
- Note when README.md is auto-generated from README.ja.md

## Code Formatting and Quality

### Before Committing Changes

**IMPORTANT**: Always run the following commands before committing any Python code changes:

```bash
# Format code with Ruff
ruff format src/ tests/

# Fix auto-fixable lint issues
ruff check --fix src/ tests/

# Verify formatting and linting (should pass with no errors)
ruff format --check src/ tests/
ruff check src/ tests/
```

These steps are **mandatory** for all code changes. Failure to format code will result in:
- PR review delays
- Manual formatting required by maintainers
- Potential PR rejection

### Why This Matters

- The project enforces consistent code style using Ruff
- GitHub Actions workflows for auto-formatting were removed due to security concerns (see issue #71)
- Manual formatting before commit is the safest and most efficient approach

## Best Practices

- Write self-documenting code with clear variable names
- Keep functions small and focused
- Avoid premature optimization
- Test changes thoroughly before committing
- **Always run ruff format and ruff check before committing**
- Use meaningful commit messages
- Follow existing code patterns and conventions

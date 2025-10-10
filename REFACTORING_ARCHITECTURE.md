# Refactoring Architecture - Issue #16

## Purpose (目的)
リファクタリング。100行を超えるソースをできるだけ分割する。目的はagentのハルシネーションによるソース破壊を防止することである。

(Refactor source files exceeding 100 lines into smaller modules to prevent source code destruction by AI agent hallucination)

## New Module Architecture

### Core Modules (src/)

```
src/
├── __init__.py              (9 lines)   - Package exports
├── __main__.py              (32 lines)  - CLI entry point
├── cat_file_watcher.py      (95 lines)  - Main FileWatcher class
├── config_loader.py         (61 lines)  - Configuration management
├── command_executor.py      (50 lines)  - Command execution
└── process_detector.py      (48 lines)  - Process detection
```

#### Module Responsibilities

**cat_file_watcher.py**
- Core file monitoring loop
- File timestamp tracking
- Change detection
- Backward compatibility wrappers

**config_loader.py**
- TOML configuration loading
- Interval conversion (milliseconds → seconds)
- Configuration validation

**command_executor.py**
- Shell command execution
- Process-based suppression
- Output handling

**process_detector.py**
- Process pattern matching
- Regex-based process detection
- Error handling for invalid patterns

**__main__.py**
- Command-line argument parsing
- Application initialization
- Entry point for `python -m src`

### Test Suite Architecture

```
test_basics.py               (87 lines)  - Basic functionality
test_intervals.py            (97 lines)  - Interval handling
test_interval_division.py    (70 lines)  - Division calculations
test_process_detection.py    (64 lines)  - Process detection
test_command_suppression.py  (97 lines)  - Command suppression
test_cat_file_watcher.py    (341 lines)  - Original (kept for compatibility)
```

## Design Principles

1. **Single Responsibility**: Each module has one clear purpose
2. **Small File Size**: All files under 100 lines to prevent AI hallucination issues
3. **Backward Compatibility**: Original API preserved through wrapper methods
4. **Import Flexibility**: Supports both relative and absolute imports
5. **Testability**: Each module can be tested independently

## Benefits

1. **Reduced AI Hallucination Risk**: Smaller files are less likely to be corrupted by AI agents
2. **Better Maintainability**: Clear separation of concerns
3. **Easier Testing**: Focused test modules for each component
4. **Code Reusability**: Modules can be used independently
5. **Clearer Architecture**: Explicit dependencies between components

## Usage

### As a Module
```bash
python -m src --config-filename config.toml
```

### As a Script (backward compatible)
```python
from src.cat_file_watcher import FileWatcher
watcher = FileWatcher('config.toml')
watcher.run()
```

### Direct Module Imports
```python
from src.config_loader import ConfigLoader
from src.process_detector import ProcessDetector
from src.command_executor import CommandExecutor
```

## Migration Notes

- All existing tests continue to pass
- No API changes for FileWatcher class
- Original test file still functional
- Module can be imported in multiple ways

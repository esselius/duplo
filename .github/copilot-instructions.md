# Duplo BLE Controller
Duplo is a Python project that provides Bluetooth Low Energy (BLE) interfaces for controlling LEGO Duplo trains and monitoring Oral-B toothbrushes. The main functionality allows controlling train movements, sounds, and lights using toothbrush events as input triggers.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively
- Bootstrap, build, and test the repository:
  - `pip install uv` (if uv is not available)
  - `uv sync` -- installs dependencies and creates virtual environment. Takes 0.03 seconds (initial sync takes 2-3 seconds with 40 packages). NEVER CANCEL. Set timeout to 60+ seconds for first sync.
- Run tests: `uv run pytest` -- takes 0.26 seconds total (test execution 0.02 seconds, 1 test passes). NEVER CANCEL. Set timeout to 30+ seconds.
- Run type checking: `uv run mypy .` -- takes 0.21 seconds for 13 source files. NEVER CANCEL. Set timeout to 30+ seconds.
- Run linting: `uv run ruff check .` -- takes 0.04 seconds. Expected to find 1 unused variable warning in control_train_with_toothbrush.py. NEVER CANCEL. Set timeout to 10+ seconds.
- Run format checking: `uv run ruff format --check .` -- takes 0.04 seconds. NEVER CANCEL. Set timeout to 10+ seconds.
- Auto-fix linting: `uv run ruff check --fix .` -- takes 0.04 seconds. Cannot fix unused variable without --unsafe-fixes. NEVER CANCEL. Set timeout to 10+ seconds.
- Auto-format code: `uv run ruff format .` -- takes 0.04 seconds. NEVER CANCEL. Set timeout to 10+ seconds.

## Project Structure
- `core/config.py` -- Configuration management using Pydantic settings. Contains BLE UUIDs for UART communication.
- `protocols/ble_duplo_train.py` -- BLE protocol definitions for LEGO Duplo train communication using Construct library.
- `protocols/ble_toothbrush.py` -- BLE protocol definitions for Oral-B toothbrush event parsing.
- `scripts/` -- Main executable scripts:
  - `control_train_with_toothbrush.py` -- Primary integration script that controls train based on toothbrush events
  - `make_train_make_sound.py` -- Sends sound commands to train
  - `listen_to_toothbrush_events.py` -- Monitors and logs toothbrush status changes
  - `listen_to_broadcast.py` -- General BLE device discovery
- `tests/test_ble_toothbrush.py` -- Unit test for toothbrush event parsing
- `app/` and `services/` -- Empty modules for future expansion

## Running Scripts
**IMPORTANT**: All scripts require physical BLE hardware (LEGO Duplo trains and/or Oral-B toothbrushes) and will fail with BleakDBusError in environments without Bluetooth support.

Run scripts with: `PYTHONPATH=. uv run python scripts/[script_name].py`

Scripts will attempt to discover and connect to:
- "Train Base" devices for Duplo train control
- "Oral-B Toothbrush" devices for toothbrush monitoring

## Validation
- Always run the full validation suite after making changes:
  - `uv run pytest` -- Must pass (1 test, completes in 0.26 seconds)
  - `uv run mypy .` -- Must pass with no type errors (checks 13 files in 0.21 seconds)
  - `uv run ruff check .` -- Should only show the known unused variable warning (completes in 0.04 seconds)
  - `uv run ruff format --check .` -- Must show all files already formatted (completes in 0.04 seconds)
- **VALIDATION SUITE TOTAL TIME**: Under 1 second - run frequently during development
- **CRITICAL**: You cannot validate actual BLE functionality without physical hardware. The scripts will fail in CI/test environments with bluetooth errors - this is expected and normal.
- For protocol changes, ensure the Construct definitions in `protocols/` parse correctly by running the existing test.
- When modifying BLE protocol definitions, always validate that existing test data still parses correctly.

## Common Tasks
The following are outputs from frequently run commands. Reference them instead of re-running bash commands to save time.

### Repository Root Structure
```
ls -la /home/runner/work/duplo/duplo
.env                    # BLE UUID configuration
.envrc                  # Environment setup
.gitignore              # Python/venv ignore patterns  
.python-version         # Specifies Python 3.12
README.md               # Basic project info
app/                    # Empty application module
core/                   # Configuration management
protocols/              # BLE protocol definitions
pyproject.toml          # UV project configuration
scripts/                # Main executable scripts
services/               # Empty services module  
shell.nix               # Nix shell configuration
tests/                  # Unit tests
uv.lock                 # UV dependency lock file
```

### pyproject.toml Configuration
```toml
[project]
name = "duplo"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "bleak>=0.22.3",           # BLE communication
    "ipython>=8.31.0",         # Interactive Python
    "pydantic-extra-types>=2.10.1",  # Extended Pydantic types
    "pydantic-settings>=2.7.0",      # Settings management
    "pydantic>=2.10.4",              # Data validation
]
[dependency-groups]
dev = [
    "construct>=2.10.68",      # Binary data parsing
    "construct-typing>=0.6.2", # Type hints for Construct
    "mypy>=1.14.0",            # Type checking
    "pytest-asyncio>=0.25.0",  # Async test support
    "pytest-mock>=3.14.0",     # Mocking support
    "pytest-mypy>=0.10.3",     # Pytest mypy integration  
    "pytest-watcher>=0.4.3",   # Test file watching
    "pytest>=8.3.4",           # Testing framework
    "ruff>=0.8.4",             # Linting and formatting
]
```

### Core Dependencies Explained
- **bleak**: Cross-platform BLE library for Python
- **construct**: Binary data structure parsing (used for BLE protocols)
- **pydantic**: Data validation and settings management
- **pytest**: Testing framework with async support
- **mypy**: Static type checking
- **ruff**: Fast Python linter and formatter

## BLE Protocol Details
### Duplo Train Protocol
Uses UART service with UUIDs defined in .env:
- UART_UUID=00001623-1212-efde-1623-785feabcd123
- CHAR_UUID=00001624-1212-efde-1623-785feabcd123

Supports commands for:
- Motor control (speed, direction)
- Speaker sounds (horn, steam, brake, station, water)
- RGB lights
- Color sensor readings
- Speedometer data

### Toothbrush Protocol  
Monitors manufacturer data (ID 220) from Oral-B devices:
- Parses brushing state (idle, running, charging)
- Tracks button presses (power, mode)
- Monitors brush timer and sectors
- Detects pressure levels

## Troubleshooting
- **ImportError for core/protocols modules**: Run scripts with `PYTHONPATH=. uv run python scripts/[script].py`
- **BleakDBusError about org.bluez**: Expected in environments without Bluetooth hardware - scripts require physical BLE devices
- **Unused variable warnings**: Known issue with speeds variable in control_train_with_toothbrush.py - safe to ignore or fix
- **UV command not found**: Install with `pip install uv`
- **Python version issues**: Project requires Python 3.12+ as specified in .python-version

## Development Workflow
1. Always run `uv sync` after pulling changes to ensure dependencies are current
2. Make code changes
3. Run validation suite: `uv run pytest && uv run mypy . && uv run ruff check . && uv run ruff format --check .` -- completes in under 1 second
4. Format code: `uv run ruff format .`
5. Test with physical hardware if available (optional - not required for most development)
6. Commit changes

The validation suite is extremely fast (under 1 second total) and should be run frequently during development.
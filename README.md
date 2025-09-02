# DUPLO Train BLE Control

A Python library and command-line toolkit for controlling DUPLO trains via Bluetooth Low Energy (BLE), with integration for toothbrush-based control.

## Features

- **High-level Python API**: Easy-to-use context managers and convenience functions
- **Command-line Tools**: Full-featured CLI commands with argument parsing and help
- **BLE Protocol Support**: Complete protocol implementation for DUPLO train communication
- **Toothbrush Integration**: Control trains using Oral-B toothbrush events
- **Comprehensive Error Handling**: User-friendly error messages and proper exception handling

## Installation

### Using UV (Recommended)

First, install uv if you don't have it:

```bash
pip install uv
```

Then install the project dependencies:

```bash
uv sync
```

### Using Nix

If you have Nix installed, you can use the provided shell environment which includes all necessary dependencies:

```bash
# Enter Nix shell (includes uv)
nix-shell

# Or with direnv (if you have .envrc support)
direnv allow

# Then sync dependencies
uv sync
```

The Nix shell provides a reproducible development environment with `uv` pre-installed.

## Library Usage

### Simple Context Manager API

The easiest way to control a train:

```python
import asyncio
from duplo import train_connection

async def demo():
    async with train_connection() as train:
        # Set up the train
        await train.quick_setup()
        
        # Control the train
        await train.set_motor_speed(0, 50)  # 50% speed
        await train.play_horn()             # Play horn sound
        await train.set_light_red()         # Set lights to red
        
        await asyncio.sleep(5)              # Run for 5 seconds
        await train.stop_all()              # Stop the train

asyncio.run(demo())
```

### One-liner Demo

For quick testing:

```python
import asyncio
from duplo import simple_train_demo

# Run a complete demo with custom parameters
asyncio.run(simple_train_demo(
    speed=75,
    sound_id=9,  # Horn sound
    run_time=15.0
))
```

### Advanced Usage

For more control, use the TrainController directly:

```python
import asyncio
from duplo import find_train, TrainController
from bleak import BleakClient

async def advanced_demo():
    # Find and connect to train
    train = await find_train("Train Base")
    if not train:
        print("Train not found!")
        return
        
    async with BleakClient(train) as client:
        controller = TrainController(client)
        await controller.setup_notifications()
        
        # Fine-grained control
        await controller.set_motor_speed(port_id=0, speed=50)
        await controller.play_sound(port_id=1, sound_id=5)
        await controller.set_light_color(port_id=17, color_id=3)

asyncio.run(advanced_demo())
```

### Enhanced TrainController Methods

The `EnhancedTrainController` (used by `train_connection`) includes convenience methods:

- `quick_setup()` - Common setup tasks
- `stop_all()` - Stop all motors  
- `emergency_stop()` - Emergency brake
- `play_horn()` - Play horn sound
- `play_station_sound()` - Play station sound
- `set_light_red()`, `set_light_green()`, `set_light_blue()` - Set light colors

## Command Line Usage

After installation, the following CLI commands are available:

### Basic Train Control

```bash
# Run basic demo with default settings
duplo-demo

# Customize the demo
duplo-demo --device-name "My Train" --speed 75 --run-time 15.0 --sound-id 9

# Get help on all options
duplo-demo --help
```

### Toothbrush Control

```bash
# Control train with toothbrush events
duplo-toothbrush

# With custom settings and verbose output
duplo-toothbrush --speed 60 --verbose

# Get help
duplo-toothbrush --help
```

### Event Monitoring

```bash
# Listen to toothbrush events
duplo-listen-toothbrush --verbose

# Scan for BLE devices
duplo-listen-broadcast --timeout 30 --filter "Train"

# Show manufacturer data in scan
duplo-listen-broadcast --manufacturer-data
```

### CLI Command Reference

| Command | Description | Key Options |
|---------|-------------|-------------|
| `duplo-demo` | Basic train control demonstration | `--speed`, `--run-time`, `--device-name` |
| `duplo-toothbrush` | Control train with toothbrush events | `--speed`, `--verbose` |
| `duplo-listen-toothbrush` | Monitor toothbrush events | `--verbose` |
| `duplo-listen-broadcast` | Listen to BLE broadcasts | `--filter`, `--timeout`, `--manufacturer-data` |

All commands support `--help` for complete option details.

## Project Structure

```
duplo/
├── core/                   # Core functionality and utilities
│   ├── config.py          # Configuration settings
│   └── train_controller.py # Low-level train control API
├── duplo/                  # High-level library API and CLI
│   ├── api.py             # High-level convenience functions
│   ├── cli/               # Command-line interface modules
│   │   ├── demo.py        # Demo CLI command
│   │   ├── toothbrush.py  # Toothbrush control CLI
│   │   ├── listen_toothbrush.py # Toothbrush monitoring CLI
│   │   └── broadcast.py   # BLE scanning CLI
│   └── __init__.py        # Main library exports
├── protocols/              # BLE protocol definitions
│   ├── ble_duplo_train.py # DUPLO train protocol
│   └── ble_toothbrush.py  # Toothbrush protocol
├── scripts/                # Original example scripts
├── services/               # Reserved for future service implementations
├── app/                    # Application entry points
└── tests/                  # Comprehensive unit tests
```

## API Reference

### Main Functions

- `train_connection(device_name, timeout)` - Context manager for train connections
- `simple_train_demo(**kwargs)` - One-liner demo function
- `find_train(name, timeout)` - Discover DUPLO train devices

### Classes

- `TrainController` - Low-level train control (from core)
- `EnhancedTrainController` - High-level train control with convenience methods
- `ToothbrushEvent` - Parsed toothbrush event data

## Development

### Running Tests

```bash
uv run pytest tests/ -v
```

### Code Quality

```bash
# Type checking
uv run mypy .

# Linting
uv run ruff check .

# Auto-formatting  
uv run ruff format .
```

## Hardware Requirements

This library requires physical BLE hardware:
- LEGO DUPLO trains with BLE support
- Oral-B toothbrushes for toothbrush integration (optional)
- Bluetooth Low Energy capable device (Raspberry Pi, laptop, etc.)

Scripts will fail with `BleakDBusError` in environments without Bluetooth support.

## Error Handling

The library includes comprehensive error handling:
- `ConnectionError` when devices are not found
- User-friendly CLI error messages
- Proper cleanup on interruption (Ctrl+C)
- Bluetooth errors are properly caught and reported

# DUPLO Train BLE Control

A Python library for controlling DUPLO trains via Bluetooth Low Energy (BLE), with integration for toothbrush-based control.

## Features

- **BLE Protocol Support**: Complete protocol implementation for DUPLO train communication
- **Toothbrush Integration**: Control trains using Oral-B toothbrush events
- **High-level API**: Easy-to-use TrainController class for common operations
- **Multiple Scripts**: Ready-to-use example scripts for various use cases

## Installation

First, install uv if you don't have it:

```bash
pip install uv
```

Then install the project dependencies:

```bash
uv sync
```

## Usage

### Using the TrainController API

```python
import asyncio
from bleak import BleakClient
from core.train_controller import find_train, TrainController

async def demo():
    train = await find_train("Train Base")
    async with BleakClient(train) as client:
        controller = TrainController(client)
        await controller.setup_notifications()
        
        # Control the train
        await controller.set_motor_speed(port_id=0, speed=50)
        await controller.play_sound(port_id=1, sound_id=5)
        await controller.set_light_color(port_id=17, color_id=3)

asyncio.run(demo())
```

### Command Line Scripts

After installation, the following commands are available:

- `duplo-demo` - Basic train control demonstration
- `duplo-toothbrush` - Control train with toothbrush events
- `duplo-listen-toothbrush` - Monitor toothbrush events
- `duplo-listen-broadcast` - Listen to BLE broadcasts

## Project Structure

```
duplo/
├── core/           # Core functionality and utilities
│   ├── config.py           # Configuration settings
│   └── train_controller.py # High-level train control API
├── protocols/      # BLE protocol definitions
│   ├── ble_duplo_train.py  # DUPLO train protocol
│   └── ble_toothbrush.py   # Toothbrush protocol
├── scripts/        # Example and utility scripts
├── services/       # Reserved for future service implementations
├── app/           # Application entry points
└── tests/         # Unit tests
```

## Development

### Running Tests

```bash
uv run pytest tests/ -v
```

### Code Quality

```bash
uv run ruff check .
uv run mypy .
```

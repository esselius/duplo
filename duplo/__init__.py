"""
Duplo BLE Controller - Python library for controlling LEGO Duplo trains via Bluetooth.

This package provides both a high-level Python API and command-line tools for controlling
LEGO Duplo trains using Bluetooth Low Energy (BLE), with optional integration for 
Oral-B toothbrush events.

Basic library usage:
    from duplo import train_connection
    
    async with train_connection() as train:
        await train.set_motor_speed(0, 50)
        await train.play_sound(1, 5)

Command-line tools:
    - duplo-demo: Basic train control demonstration
    - duplo-toothbrush: Control train with toothbrush events  
    - duplo-listen-toothbrush: Monitor toothbrush events
    - duplo-listen-broadcast: Listen to BLE broadcasts
"""

# Import the high-level API for easy library usage
from duplo.api import (
    train_connection,
    simple_train_demo, 
    TrainController,
    EnhancedTrainController,
    find_train
)

# Also make core components available
from core.train_controller import TrainController as CoreTrainController
from protocols.ble_toothbrush import ToothbrushEvent

__version__ = "0.1.0"

__all__ = [
    # High-level API
    'train_connection',
    'simple_train_demo',
    'TrainController', 
    'EnhancedTrainController',
    'find_train',
    
    # Core components
    'CoreTrainController',
    'ToothbrushEvent',
    
    # Version
    '__version__'
]
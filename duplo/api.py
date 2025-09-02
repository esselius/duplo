"""High-level convenience API for DUPLO train control."""

import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any

from bleak import BleakClient
from core.train_controller import find_train, TrainController as BaseTrainController


@asynccontextmanager
async def train_connection(
    device_name: str = "Train Base",
    timeout: float = 30.0
) -> AsyncGenerator['EnhancedTrainController', None]:
    """Context manager for easy train connection and control.
    
    Args:
        device_name: Name of the train device to connect to
        timeout: Timeout in seconds for device discovery
        
    Yields:
        EnhancedTrainController: Ready-to-use train controller with convenience methods
        
    Example:
        async with train_connection() as train:
            await train.set_motor_speed(0, 50)
            await train.play_sound(1, 5)
    """
    device = await find_train(device_name, timeout=timeout)
    if device is None:
        raise ConnectionError(f"Train '{device_name}' not found within {timeout} seconds")
    
    async with BleakClient(device) as client:
        controller = EnhancedTrainController(client)
        await controller.setup_notifications()
        yield controller


async def simple_train_demo(
    device_name: str = "Train Base",
    speed: int = 50,
    sound_id: int = 5,
    color_id: int = 5,
    run_time: float = 10.0
) -> None:
    """Run a simple train demonstration.
    
    Args:
        device_name: Name of the train device
        speed: Motor speed (0-100)
        sound_id: Sound to play
        color_id: Light color
        run_time: How long to run the motor
    """
    async with train_connection(device_name) as train:
        # Setup ports
        await train.setup_port_input_format(port_id=1, mode=1)
        await asyncio.sleep(0.5)
        
        # Play sound and set light
        await train.play_sound(port_id=1, sound_id=sound_id)
        await train.set_light_color(port_id=17, color_id=color_id)
        await asyncio.sleep(1)
        
        # Run motor
        await train.set_motor_speed(port_id=0, speed=speed)
        await asyncio.sleep(run_time)
        
        # Stop
        await train.set_motor_speed(port_id=0, speed=0)


class EnhancedTrainController:
    """Enhanced TrainController with additional convenience methods."""
    
    def __init__(self, client: BleakClient):
        self._controller = BaseTrainController(client)
    
    def __getattr__(self, name: str) -> Any:
        """Delegate to the base controller."""
        return getattr(self._controller, name)
    
    async def quick_setup(self) -> None:
        """Perform common setup tasks."""
        await self.setup_notifications()
        await self.setup_port_input_format(port_id=1, mode=1)  # Speaker
        await asyncio.sleep(0.5)
    
    async def stop_all(self) -> None:
        """Stop all motors."""
        await self.set_motor_speed(port_id=0, speed=0)
    
    async def emergency_stop(self) -> None:
        """Emergency brake (faster stop)."""
        await self.set_motor_speed(port_id=0, speed=127)  # Brake
    
    async def play_horn(self) -> None:
        """Play horn sound."""
        await self.play_sound(port_id=1, sound_id=9)
    
    async def play_station_sound(self) -> None:
        """Play station arrival sound."""
        await self.play_sound(port_id=1, sound_id=5)
    
    async def set_light_red(self) -> None:
        """Set lights to red."""
        await self.set_light_color(port_id=17, color_id=5)
    
    async def set_light_green(self) -> None:
        """Set lights to green."""  
        await self.set_light_color(port_id=17, color_id=7)
    
    async def set_light_blue(self) -> None:
        """Set lights to blue."""
        await self.set_light_color(port_id=17, color_id=3)


# Export the original TrainController and the enhanced one
TrainController = BaseTrainController

# Make functions and classes available at module level  
__all__ = [
    'train_connection', 
    'simple_train_demo', 
    'TrainController', 
    'EnhancedTrainController',
    'find_train'
]
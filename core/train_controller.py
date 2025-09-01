"""Utilities for controlling DUPLO trains via BLE."""

from typing import Optional
from bleak import BleakClient, BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.characteristic import BleakGATTCharacteristic

from core.config import Config
from protocols.ble_duplo_train import (
    common_message_header,
    message_type,
    port_input_format_setup_single_format,
    port_output_command,
    port_output_command_feedback,
    port_value_single,
    hub_attached_io_message_format,
    generic_error_message,
)

config = Config()


def convert_speed_to_val(speed: int) -> int:
    """Map speed of -100 to 100 to a byte range.

    Args:
        speed: Speed value from -100 to 100 (negative means reverse)
                0 is floating, 127 is brake

    Returns:
        Byte value for the speed command
    """
    if speed == 127:
        return 127
    if speed > 100:
        speed = 100
    if speed < 0:
        # Convert to 8-bit unsigned representation
        speed = speed & 255
    return speed


def notification_handler(sender: BleakGATTCharacteristic, data: bytearray) -> None:
    """Handle notifications from the train hub."""
    payload = common_message_header.parse(data)
    match payload.message_type:
        case message_type.hub_attached_io:
            payload = hub_attached_io_message_format.parse(data)
            print("Hub attached IO")
        case message_type.generic_error_message:
            payload = generic_error_message.parse(data)
            print("Error")
        case message_type.port_value_single:
            payload = port_value_single.parse(data)
            print("Port value")
        case message_type.port_input_format_single:
            payload = port_input_format_setup_single_format.parse(data)
            print("Port input format")
        case message_type.port_output_command_feedback:
            payload = port_output_command_feedback.parse(data)
            print("Port output command feedback")


async def find_train(name: str = "Train Base", timeout: float = 30.0) -> Optional[BLEDevice]:
    """Find a DUPLO train by name."""
    device = await BleakScanner().find_device_by_name(name, timeout=timeout)
    return device


class TrainController:
    """High-level controller for DUPLO train operations."""
    
    def __init__(self, client: BleakClient):
        self.client = client
        self.config = config
    
    async def setup_notifications(self) -> None:
        """Setup notification handling for train responses."""
        await self.client.start_notify(self.config.CHAR_UUID, notification_handler)
    
    async def setup_port_input_format(self, port_id: int, mode: int = 1) -> None:
        """Setup input format for a specific port."""
        payload = port_input_format_setup_single_format.build({
            "header": {
                "length": 10,
                "hub_id": 0,
                "message_type": message_type.port_input_format_setup_single,
            },
            "port_id": port_id,
            "mode": mode,
            "delta_interval": 1,
            "notification_enabled": 1,
        })
        await self.client.write_gatt_char(
            self.config.CHAR_UUID, payload, response=False
        )
    
    async def set_motor_speed(self, port_id: int, speed: int) -> None:
        """Set motor speed for a specific port.
        
        Args:
            port_id: Motor port ID (typically 0 for main motor)
            speed: Speed from -100 to 100, or 127 for brake
        """
        payload = port_output_command.build({
            "header": {
                "length": 8,
                "hub_id": 0,
                "message_type": message_type.port_output_command,
            },
            "port_id": port_id,
            "startup_and_completion_information": {
                "startup": 1,
                "completion": 1,
            },
            "sub_command": 0x51,
            "payload": bytes([0, convert_speed_to_val(speed)]),
        })
        await self.client.write_gatt_char(
            self.config.CHAR_UUID, payload, response=False
        )
    
    async def play_sound(self, port_id: int, sound_id: int) -> None:
        """Play a sound on the train speaker.
        
        Args:
            port_id: Speaker port ID (typically 1)
            sound_id: Sound ID to play
        """
        payload = port_output_command.build({
            "header": {
                "length": 8,
                "hub_id": 0,
                "message_type": message_type.port_output_command,
            },
            "port_id": port_id,
            "startup_and_completion_information": {
                "startup": 1,
                "completion": 1,
            },
            "sub_command": 0x51,
            "payload": bytes([1, sound_id]),
        })
        await self.client.write_gatt_char(
            self.config.CHAR_UUID, payload, response=False
        )
    
    async def set_light_color(self, port_id: int, color_id: int) -> None:
        """Set light color on the train.
        
        Args:
            port_id: Light port ID (typically 17)
            color_id: Color ID to set
        """
        payload = port_output_command.build({
            "header": {
                "length": 8,
                "hub_id": 0,
                "message_type": message_type.port_output_command,
            },
            "port_id": port_id,
            "startup_and_completion_information": {
                "startup": 1,
                "completion": 1,
            },
            "sub_command": 0x51,
            "payload": bytes([0, color_id]),
        })
        await self.client.write_gatt_char(
            self.config.CHAR_UUID, payload, response=False
        )
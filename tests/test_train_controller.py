"""Test the TrainController utility."""

import pytest
from unittest.mock import AsyncMock, Mock
from core.train_controller import TrainController, convert_speed_to_val


def test_convert_speed_to_val():
    """Test speed conversion utility."""
    # Normal positive speeds
    assert convert_speed_to_val(0) == 0
    assert convert_speed_to_val(50) == 50
    assert convert_speed_to_val(100) == 100
    
    # Speed clamping
    assert convert_speed_to_val(150) == 100
    
    # Brake
    assert convert_speed_to_val(127) == 127
    
    # Negative speeds (reverse)
    assert convert_speed_to_val(-50) == 206  # 256 - 50
    assert convert_speed_to_val(-100) == 156  # 256 - 100


@pytest.mark.asyncio
async def test_train_controller():
    """Test TrainController basic functionality."""
    # Mock the BLE client
    mock_client = Mock()
    mock_client.write_gatt_char = AsyncMock()
    mock_client.start_notify = AsyncMock()
    
    controller = TrainController(mock_client)
    
    # Test motor speed setting
    await controller.set_motor_speed(port_id=0, speed=50)
    mock_client.write_gatt_char.assert_called()
    
    # Test sound playing
    await controller.play_sound(port_id=1, sound_id=5)
    assert mock_client.write_gatt_char.call_count == 2
    
    # Test light color setting
    await controller.set_light_color(port_id=17, color_id=3)
    assert mock_client.write_gatt_char.call_count == 3
"""Test the enhanced duplo API."""

import pytest
from unittest.mock import AsyncMock, Mock, patch
from duplo.api import train_connection, simple_train_demo, EnhancedTrainController


@pytest.mark.asyncio
async def test_enhanced_train_controller():
    """Test the EnhancedTrainController convenience methods."""
    # Mock the BLE client
    mock_client = Mock()
    mock_client.write_gatt_char = AsyncMock()
    mock_client.start_notify = AsyncMock()

    controller = EnhancedTrainController(mock_client)

    # Test delegation to base controller
    await controller.set_motor_speed(port_id=0, speed=50)
    mock_client.write_gatt_char.assert_called()

    # Test convenience methods
    await controller.play_horn()
    await controller.play_station_sound() 
    await controller.set_light_red()
    await controller.set_light_green()
    await controller.set_light_blue()
    await controller.stop_all()
    await controller.emergency_stop()

    # Verify multiple calls were made
    assert mock_client.write_gatt_char.call_count >= 8


@pytest.mark.asyncio
@patch('duplo.api.find_train')
@patch('duplo.api.BleakClient')
async def test_train_connection_context_manager(mock_bleak_client, mock_find_train):
    """Test the train_connection context manager."""
    # Mock successful device discovery
    mock_device = Mock()
    mock_find_train.return_value = mock_device
    
    # Mock BleakClient
    mock_client_instance = Mock()
    mock_client_instance.write_gatt_char = AsyncMock()
    mock_client_instance.start_notify = AsyncMock()
    mock_bleak_client.return_value.__aenter__ = AsyncMock(return_value=mock_client_instance)
    mock_bleak_client.return_value.__aexit__ = AsyncMock()
    
    # Test successful connection
    async with train_connection("Test Train") as train:
        assert isinstance(train, EnhancedTrainController)
        await train.set_motor_speed(0, 50)
    
    mock_find_train.assert_called_once_with("Test Train", timeout=30.0)
    mock_client_instance.start_notify.assert_called_once()


@pytest.mark.asyncio
@patch('duplo.api.find_train')
async def test_train_connection_device_not_found(mock_find_train):
    """Test train_connection when device is not found."""
    mock_find_train.return_value = None
    
    with pytest.raises(ConnectionError, match="Train 'Test Train' not found"):
        async with train_connection("Test Train"):
            pass


@pytest.mark.asyncio
@patch('duplo.api.train_connection')
async def test_simple_train_demo(mock_train_connection):
    """Test the simple_train_demo convenience function."""
    # Mock the train controller
    mock_train = Mock()
    mock_train.setup_port_input_format = AsyncMock()
    mock_train.play_sound = AsyncMock()
    mock_train.set_light_color = AsyncMock()
    mock_train.set_motor_speed = AsyncMock()
    
    # Mock context manager
    mock_train_connection.return_value.__aenter__ = AsyncMock(return_value=mock_train)
    mock_train_connection.return_value.__aexit__ = AsyncMock()
    
    # Test the demo
    await simple_train_demo(
        device_name="Test Train",
        speed=75,
        sound_id=3,
        color_id=7,
        run_time=5.0
    )
    
    # Verify calls were made
    mock_train.setup_port_input_format.assert_called_once_with(port_id=1, mode=1)
    mock_train.play_sound.assert_called_once_with(port_id=1, sound_id=3)
    mock_train.set_light_color.assert_called_once_with(port_id=17, color_id=7)
    
    # Should be called twice - once to start, once to stop
    assert mock_train.set_motor_speed.call_count == 2
    mock_train.set_motor_speed.assert_any_call(port_id=0, speed=75)
    mock_train.set_motor_speed.assert_any_call(port_id=0, speed=0)
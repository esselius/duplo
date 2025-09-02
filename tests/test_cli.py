"""Test CLI commands."""

import pytest
from unittest.mock import patch, AsyncMock, Mock
from duplo.cli.demo import create_parser as demo_parser, demo_train_control
from duplo.cli.toothbrush import create_parser as toothbrush_parser 


def test_demo_cli_parser():
    """Test the demo command argument parser."""
    parser = demo_parser()
    
    # Test default arguments
    args = parser.parse_args([])
    assert args.device_name == "Train Base"
    assert args.timeout == 30.0
    assert args.speed == 50
    assert args.sound_id == 5
    assert args.color_id == 5
    assert args.run_time == 10.0
    
    # Test custom arguments
    args = parser.parse_args([
        "--device-name", "My Train",
        "--timeout", "60.0", 
        "--speed", "75",
        "--sound-id", "9",
        "--color-id", "3",
        "--run-time", "15.0"
    ])
    assert args.device_name == "My Train"
    assert args.timeout == 60.0
    assert args.speed == 75
    assert args.sound_id == 9
    assert args.color_id == 3
    assert args.run_time == 15.0


def test_toothbrush_cli_parser():
    """Test the toothbrush command argument parser."""
    parser = toothbrush_parser()
    
    # Test default arguments
    args = parser.parse_args([])
    assert args.device_name == "Train Base"
    assert args.timeout == 30.0
    assert args.speed == 50
    assert args.sound_id == 9
    assert args.verbose is False
    
    # Test verbose flag
    args = parser.parse_args(["--verbose"])
    assert args.verbose is True
    
    args = parser.parse_args(["-v"])
    assert args.verbose is True


@pytest.mark.asyncio
@patch('duplo.cli.demo.find_train')
@patch('duplo.cli.demo.BleakClient')
async def test_demo_train_control(mock_bleak_client, mock_find_train):
    """Test the demo train control function."""
    # Mock successful device discovery
    mock_device = Mock()
    mock_find_train.return_value = mock_device
    
    # Mock BleakClient and TrainController
    mock_client_instance = Mock()
    mock_client_instance.write_gatt_char = AsyncMock()
    mock_client_instance.start_notify = AsyncMock()
    mock_bleak_client.return_value.__aenter__ = AsyncMock(return_value=mock_client_instance)
    mock_bleak_client.return_value.__aexit__ = AsyncMock()
    
    # Test the demo function
    await demo_train_control(
        device_name="Test Train",
        timeout=30.0,
        speed=50,
        sound_id=5,
        color_id=3,
        run_time=5.0
    )
    
    # Verify device was found and client was used
    mock_find_train.assert_called_once_with("Test Train", timeout=30.0)
    mock_client_instance.start_notify.assert_called_once()
    # TrainController methods result in write_gatt_char calls
    assert mock_client_instance.write_gatt_char.call_count >= 4


@pytest.mark.asyncio  
@patch('duplo.cli.demo.find_train')
async def test_demo_train_control_device_not_found(mock_find_train):
    """Test demo when device is not found."""
    mock_find_train.return_value = None
    
    with pytest.raises(SystemExit):
        await demo_train_control(
            device_name="Missing Train",
            timeout=30.0,
            speed=50,
            sound_id=5,
            color_id=3,
            run_time=5.0
        )
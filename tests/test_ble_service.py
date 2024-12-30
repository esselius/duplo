from typing import Any
import bleak.backends
import bleak.backends.device
import pytest
from unittest.mock import patch, AsyncMock

import bleak

from services.ble import BLE


@pytest.fixture
def mock_ble_discover() -> Any:
    with patch("bleak.BleakScanner") as mock_bleak_scanner:
        mock_bleak_scanner.discover = AsyncMock()
        mock_bleak_scanner.discover.return_value = [
            bleak.backends.device.BLEDevice(
                address="00:11:22:33:44:55",
                name="Train Base",
                rssi=-60,
                details=None,
            )
        ]
        yield

        mock_bleak_scanner.discover.assert_awaited_once()


@pytest.fixture
def mock_ble_connect() -> Any:
    mock_client = AsyncMock()
    mock_client.connect.return_value = True

    with patch("bleak.BleakClient", return_value=mock_client):
        yield

    mock_client.connect.assert_awaited_once()


async def test_find_train(mock_ble_discover: Any) -> None:
    ble = BLE()

    train = await ble.find_train()

    assert isinstance(train, bleak.backends.device.BLEDevice)
    assert train.address == "00:11:22:33:44:55"
    assert train.name == "Train Base"


async def test_connect_to_train(mock_ble_discover: Any, mock_ble_connect: Any) -> None:
    ble = BLE()

    train = await ble.find_train()
    await ble.connect(train)

import pytest
from unittest.mock import AsyncMock, MagicMock

from bleak import BleakScanner

from services.ble_manager import BLEManager


@pytest.fixture
def mock_ble_scanner():
    scanner = MagicMock(spec=BleakScanner)
    scanner.discover = AsyncMock(return_value=[])
    return scanner


@pytest.fixture
def ble_manager(mock_ble_scanner):
    manager = BLEManager(scanner=mock_ble_scanner)
    return manager


@pytest.mark.asyncio
async def test_scan_for_devices(ble_manager, mock_ble_scanner):
    mock_device = MagicMock()
    mock_device.address = "00:11:22:33:44:55"
    mock_device.name = "Train Base"
    mock_device.rssi = -60

    mock_ble_scanner.discover.return_value = [mock_device]

    devices = await ble_manager.scan_for_devices()

    mock_ble_scanner.discover.assert_called_once()

    assert len(devices) == 1
    assert devices[0].address == "00:11:22:33:44:55"
    assert devices[0].name == "Train Base"
    assert devices[0].rssi == -60

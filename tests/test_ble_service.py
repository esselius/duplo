from typing import Any, List, Optional, Type
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementDataCallback, AdvertisementData

from services.ble import BLE, Device


async def test_find_train() -> None:
    class MockScanner:
        def __init__(
            self,
            detection_callback: AdvertisementDataCallback,
            service_uuids: List[str],
        ) -> None:
            self.detection_callback = detection_callback

        async def __aenter__(self) -> "MockScanner":
            mock_device = BLEDevice(
                address="00:11:22:33:44:55", name="Train Base", rssi=-60, details=None
            )
            mock_adv = AdvertisementData(
                local_name="Train Base",
                manufacturer_data={},
                service_data={},
                service_uuids=[],
                tx_power=0,
                rssi=-60,
                platform_data=("", ""),
            )
            self.detection_callback(mock_device, mock_adv)
            return self

        async def __aexit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_value: Optional[BaseException],
            traceback: Optional[Any],
        ) -> Optional[bool]:
            pass

    ble = BLE(scanner_cls=MockScanner)

    train = await ble.find_train()

    assert isinstance(train, BLEDevice)
    assert train.address == "00:11:22:33:44:55"
    assert train.name == "Train Base"


async def test_device_connect() -> None:
    class MockClient:
        def __init__(self, device: BLEDevice) -> None:
            pass

        async def connect(self) -> None:
            pass

    ble_device = BLEDevice(
        address="00:11:22:33:44:55", name="Train Base", rssi=-60, details=None
    )

    device = Device(ble_device, client_cls=MockClient)

    await device.connect()

import asyncio
from typing import Any

from bleak import BleakClient, BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

from core.config import Config

config = Config()


class Device:
    def __init__(self, ble_device: BLEDevice, client_cls: Any = BleakClient):
        self.client = client_cls(ble_device)

    async def connect(self) -> None:
        await self.client.connect()


class BLE:
    def __init__(self, scanner_cls: Any = BleakScanner) -> None:
        self.scanner_cls = scanner_cls

    async def find_train(self) -> BLEDevice | None:
        stop_event = asyncio.Event()

        devices = []

        def callback(device: BLEDevice, adv: AdvertisementData) -> None:
            devices.append(device)
            stop_event.set()

        async with self.scanner_cls(
            detection_callback=callback, service_uuids=[str(config.UART_UUID)]
        ):
            await stop_event.wait()

        return devices[0]

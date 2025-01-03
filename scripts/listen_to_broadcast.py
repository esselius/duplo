import asyncio
from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData


async def main() -> None:
    scanner = BleakScanner()

    def callback(device: BLEDevice, advertisement_data: AdvertisementData) -> None:
        print(len(scanner.discovered_devices_and_advertisement_data))

    scanner.register_detection_callback(callback)
    await scanner.start()
    await asyncio.sleep(120)
    await scanner.stop()


asyncio.run(main())

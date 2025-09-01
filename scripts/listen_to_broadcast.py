import asyncio
from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData


async def main() -> None:
    def callback(device: BLEDevice, advertisement_data: AdvertisementData) -> None:
        print(f"Found device: {device.name} ({device.address})")
        if advertisement_data.manufacturer_data:
            print(f"  Manufacturer data: {advertisement_data.manufacturer_data}")

    scanner = BleakScanner(detection_callback=callback)
    await scanner.start()
    await asyncio.sleep(120)
    await scanner.stop()


if __name__ == "__main__":
    asyncio.run(main())

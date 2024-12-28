from bleak import BleakScanner


class BLEManager:
    def __init__(self, scanner: BleakScanner):
        self.scanner = scanner

    async def scan_for_devices(self):
        return await self.scanner.discover()

import bleak


class BLE:
    async def find_train(self) -> bleak.backends.device.BLEDevice:
        devices = await bleak.BleakScanner.discover()
        return devices[0]

    async def connect(self, ble_device: bleak.backends.device.BLEDevice) -> None:
        await bleak.BleakClient(ble_device).connect()

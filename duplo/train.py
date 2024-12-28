from asyncio import sleep
import uuid

from bleak import BleakScanner, BleakClient, BLEDevice, AdvertisementData

uart_uuid = uuid.UUID('00001623-1212-efde-1623-785feabcd123')
char_uuid = uuid.UUID('00001624-1212-efde-1623-785feabcd123')

class Train():
    def __init__(self):
        self.device = None

    async def connect(self):
        def find_train_device(device: BLEDevice, adv: AdvertisementData):
            manufacturer_id = next(iter(adv.manufacturer_data.values()))[1]
            if manufacturer_id != 32:
                pass
            self.device = device

        scanner = BleakScanner(detection_callback=find_train_device, service_uuids=[str(uart_uuid)])

        await scanner.start()
        while self.device is None:
            await sleep(1)
        await scanner.stop()

        self.client = BleakClient(self.device)

        await self.client.connect()

    async def send(self, msg):
        await self.client.write_gatt_char(char_uuid, msg)

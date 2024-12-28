import uuid
import asyncio
from asyncio import sleep
from bleak import BleakGATTCharacteristic

from duplo.train import Train
from duplo.decoder import HubAttachedIoMessage, HubAttachedIo

char_uuid = uuid.UUID('00001624-1212-efde-1623-785feabcd123')

async def main():
    print("Looking for train...")
    train = Train()
    await train.connect()
    print("Found train!")

    def train_events(sender: BleakGATTCharacteristic, data: bytes):
        msg = HubAttachedIo(**HubAttachedIoMessage.parse(data))
        print(msg)

    await train.client.start_notify(char_uuid, callback=train_events)

    await sleep(10)


asyncio.run(main())

import asyncio

from services.ble import BLE


async def main() -> None:
    ble = BLE()

    train = await ble.find_train()
    await ble.connect(train)


asyncio.run(main())

import asyncio
from bleak import BleakClient, BleakScanner
from protocols.ble_toothbrush import ToothbrushEvent
from core.train_controller import find_train, TrainController

toothbrush_service_uuid = "0000fe0d-0000-1000-8000-00805f9b34fb"


async def main() -> None:
    """Control train using toothbrush events."""
    train = await find_train("Train Base", timeout=30)
    assert train is not None, "Train not found"
    print(f"Found train: {train}")

    async with BleakClient(train) as client:
        controller = TrainController(client)
        await controller.setup_notifications()
        await controller.setup_port_input_format(port_id=1, mode=1)

        async with BleakScanner(service_uuids=[toothbrush_service_uuid]) as scanner:
            last_state = None
            async for _, adv_data in scanner.advertisement_data():
                data = adv_data.manufacturer_data[220]
                parsed = ToothbrushEvent.parse(data)
                if parsed != last_state:
                    if last_state is not None:
                        if parsed.state == "running" and last_state.state != "running":
                            print("Started brushing - starting train")
                            await controller.set_motor_speed(port_id=0, speed=50)
                        
                        if parsed.state == "idle" and last_state.state == "running":
                            print("Stopped brushing - stopping train")
                            await controller.set_motor_speed(port_id=0, speed=0)
                        
                        if (
                            parsed.pressure.mode_button_pressed
                            and not last_state.pressure.mode_button_pressed
                        ):
                            print("Pressed mode button - playing horn sound")
                            await controller.play_sound(port_id=1, sound_id=9)  # Horn sound
                    
                    last_state = parsed


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
from bleak import BleakClient
from core.train_controller import find_train, TrainController


async def main() -> None:
    """Demo script showing various train control features."""
    train = await find_train("Train Base")
    assert train is not None, "Train not found"
    print(f"Found train: {train}")

    async with BleakClient(train) as client:
        controller = TrainController(client)
        await controller.setup_notifications()

        # Setup speaker port
        await controller.setup_port_input_format(port_id=1, mode=1)
        await asyncio.sleep(1)

        # Play sound
        print("Playing sound...")
        await controller.play_sound(port_id=1, sound_id=5)  # Station sound
        await asyncio.sleep(1)

        # Change light color
        print("Setting light color...")
        await controller.set_light_color(port_id=17, color_id=5)
        await asyncio.sleep(1)

        # Set speed to 50%
        print("Setting motor speed to 50%...")
        await controller.set_motor_speed(port_id=0, speed=50)
        await asyncio.sleep(10)

        # Stop the train
        print("Stopping train...")
        await controller.set_motor_speed(port_id=0, speed=0)


if __name__ == "__main__":
    asyncio.run(main())

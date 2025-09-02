#!/usr/bin/env python3
"""CLI command for basic train control demonstration."""

import argparse
import asyncio
import sys

from bleak import BleakClient
from core.train_controller import find_train, TrainController


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for the demo command."""
    parser = argparse.ArgumentParser(
        description="Demonstrate basic DUPLO train control features",
        prog="duplo-demo"
    )
    parser.add_argument(
        "--device-name", 
        default="Train Base",
        help="Name of the train device to connect to (default: Train Base)"
    )
    parser.add_argument(
        "--timeout", 
        type=float, 
        default=30.0,
        help="Timeout in seconds for device discovery (default: 30.0)"
    )
    parser.add_argument(
        "--speed",
        type=int,
        default=50,
        help="Motor speed to test (0-100, default: 50)"
    )
    parser.add_argument(
        "--sound-id",
        type=int,
        default=5,
        help="Sound ID to play (default: 5 - station sound)"
    )
    parser.add_argument(
        "--color-id",
        type=int,
        default=5,
        help="Color ID for lights (default: 5)"
    )
    parser.add_argument(
        "--run-time",
        type=float,
        default=10.0,
        help="How long to run the motor in seconds (default: 10.0)"
    )
    return parser


async def demo_train_control(
    device_name: str,
    timeout: float,
    speed: int,
    sound_id: int,
    color_id: int,
    run_time: float
) -> None:
    """Run the train control demonstration."""
    print(f"Looking for train: {device_name}")
    train = await find_train(device_name, timeout=timeout)
    if train is None:
        print(f"Error: Train '{device_name}' not found within {timeout} seconds")
        sys.exit(1)
        
    print(f"Found train: {train}")

    async with BleakClient(train) as client:
        controller = TrainController(client)
        await controller.setup_notifications()

        # Setup speaker port
        print("Setting up speaker port...")
        await controller.setup_port_input_format(port_id=1, mode=1)
        await asyncio.sleep(1)

        # Play sound
        print(f"Playing sound ID {sound_id}...")
        await controller.play_sound(port_id=1, sound_id=sound_id)
        await asyncio.sleep(1)

        # Change light color
        print(f"Setting light color to {color_id}...")
        await controller.set_light_color(port_id=17, color_id=color_id)
        await asyncio.sleep(1)

        # Set speed
        print(f"Setting motor speed to {speed}%...")
        await controller.set_motor_speed(port_id=0, speed=speed)
        await asyncio.sleep(run_time)

        # Stop the train
        print("Stopping train...")
        await controller.set_motor_speed(port_id=0, speed=0)

    print("Demo completed successfully!")


def main() -> None:
    """Main entry point for the demo CLI command."""
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        asyncio.run(demo_train_control(
            device_name=args.device_name,
            timeout=args.timeout,
            speed=args.speed,
            sound_id=args.sound_id,
            color_id=args.color_id,
            run_time=args.run_time
        ))
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""CLI command for controlling train with toothbrush events."""

import argparse
import asyncio
import sys

from bleak import BleakClient, BleakScanner
from protocols.ble_toothbrush import ToothbrushEvent
from core.train_controller import find_train, TrainController

TOOTHBRUSH_SERVICE_UUID = "0000fe0d-0000-1000-8000-00805f9b34fb"


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for the toothbrush control command."""
    parser = argparse.ArgumentParser(
        description="Control DUPLO train using Oral-B toothbrush events",
        prog="duplo-toothbrush"
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
        help="Motor speed when brushing starts (0-100, default: 50)"
    )
    parser.add_argument(
        "--sound-id",
        type=int,
        default=9,
        help="Sound ID for mode button press (default: 9 - horn sound)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    return parser


async def control_train_with_toothbrush(
    device_name: str,
    timeout: float,
    speed: int,
    sound_id: int,
    verbose: bool
) -> None:
    """Control train based on toothbrush events."""
    if verbose:
        print(f"Looking for train: {device_name}")
        
    train = await find_train(device_name, timeout=timeout)
    if train is None:
        print(f"Error: Train '{device_name}' not found within {timeout} seconds")
        sys.exit(1)
        
    if verbose:
        print(f"Found train: {train}")

    async with BleakClient(train) as client:
        controller = TrainController(client)
        await controller.setup_notifications()
        await controller.setup_port_input_format(port_id=1, mode=1)
        
        if verbose:
            print("Connected to train. Listening for toothbrush events...")
            print("Start brushing to move the train, press mode button for horn sound")
            print("Press Ctrl+C to stop")

        async with BleakScanner(service_uuids=[TOOTHBRUSH_SERVICE_UUID]) as scanner:
            last_state = None
            try:
                async for _, adv_data in scanner.advertisement_data():
                    if 220 not in adv_data.manufacturer_data:
                        continue
                        
                    data = adv_data.manufacturer_data[220]
                    try:
                        parsed = ToothbrushEvent.parse(data)
                    except Exception as e:
                        if verbose:
                            print(f"Failed to parse toothbrush data: {e}")
                        continue
                        
                    if parsed != last_state:
                        if last_state is not None:
                            if parsed.state == "running" and last_state.state != "running":
                                print("Started brushing - starting train")
                                await controller.set_motor_speed(port_id=0, speed=speed)

                            if parsed.state == "idle" and last_state.state == "running":
                                print("Stopped brushing - stopping train")
                                await controller.set_motor_speed(port_id=0, speed=0)

                            if (
                                parsed.pressure.mode_button_pressed
                                and not last_state.pressure.mode_button_pressed
                            ):
                                print("Mode button pressed - playing horn sound")
                                await controller.play_sound(port_id=1, sound_id=sound_id)

                        last_state = parsed
                        
            except KeyboardInterrupt:
                print("\nStopping train and exiting...")
                await controller.set_motor_speed(port_id=0, speed=0)
                raise


def main() -> None:
    """Main entry point for the toothbrush control CLI command."""
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        asyncio.run(control_train_with_toothbrush(
            device_name=args.device_name,
            timeout=args.timeout,
            speed=args.speed,
            sound_id=args.sound_id,
            verbose=args.verbose
        ))
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
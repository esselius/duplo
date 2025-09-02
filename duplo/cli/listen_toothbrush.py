#!/usr/bin/env python3
"""CLI command for listening to toothbrush events."""

import argparse
import asyncio
import sys

from bleak import BleakScanner
from protocols.ble_toothbrush import ToothbrushEvent

TOOTHBRUSH_SERVICE_UUID = "0000fe0d-0000-1000-8000-00805f9b34fb"


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for the toothbrush listener command."""
    parser = argparse.ArgumentParser(
        description="Listen to and display Oral-B toothbrush events",
        prog="duplo-listen-toothbrush"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output including raw data"
    )
    return parser


async def listen_to_toothbrush_events(verbose: bool) -> None:
    """Listen to toothbrush events and display them."""
    print("Scanning for Oral-B toothbrushes...")
    print("Press Ctrl+C to stop")
    
    async with BleakScanner(service_uuids=[TOOTHBRUSH_SERVICE_UUID]) as scanner:
        last_state = None
        try:
            async for device, adv_data in scanner.advertisement_data():
                if 220 not in adv_data.manufacturer_data:
                    continue
                    
                data = adv_data.manufacturer_data[220]
                if verbose:
                    print(f"Raw data from {device.name}: {data.hex()}")
                    
                try:
                    parsed = ToothbrushEvent.parse(data)
                except Exception as e:
                    if verbose:
                        print(f"Failed to parse data: {e}")
                    continue
                    
                if parsed != last_state:
                    print("Toothbrush state changed:")
                    print(f"  State: {parsed.state}")
                    print(f"  Pressure: {parsed.pressure}")
                    print(f"  Timer: {parsed.timer}")
                    print(f"  Mode: {parsed.mode}")
                    if parsed.pressure.mode_button_pressed:
                        print("  >>> Mode button pressed!")
                    if parsed.pressure.power_button_pressed:
                        print("  >>> Power button pressed!")
                    print()
                    last_state = parsed
                    
        except KeyboardInterrupt:
            print("\nStopping...")
            raise


def main() -> None:
    """Main entry point for the toothbrush listener CLI command."""
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        asyncio.run(listen_to_toothbrush_events(verbose=args.verbose))
    except KeyboardInterrupt:
        print("Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
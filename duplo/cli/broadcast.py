#!/usr/bin/env python3
"""CLI command for listening to BLE broadcasts."""

import argparse
import asyncio
import sys

from bleak import BleakScanner


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for the broadcast listener command."""
    parser = argparse.ArgumentParser(
        description="Listen to BLE device advertisements and broadcasts",
        prog="duplo-listen-broadcast"
    )
    parser.add_argument(
        "--timeout", 
        type=float, 
        default=60.0,
        help="How long to scan in seconds (default: 60.0, 0 for infinite)"
    )
    parser.add_argument(
        "--filter",
        help="Filter devices by name (case-insensitive substring match)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed advertisement data"
    )
    parser.add_argument(
        "--manufacturer-data",
        action="store_true",
        help="Show manufacturer-specific data"
    )
    return parser


async def listen_to_broadcasts(
    timeout: float, 
    name_filter: str,
    verbose: bool,
    show_manufacturer_data: bool
) -> None:
    """Listen to BLE broadcasts."""
    print("Scanning for BLE devices...")
    if name_filter:
        print(f"Filtering by name: {name_filter}")
    if timeout > 0:
        print(f"Scanning for {timeout} seconds")
    else:
        print("Scanning indefinitely (press Ctrl+C to stop)")
    print()
    
    seen_devices = set()
    
    async with BleakScanner() as scanner:
        try:
            start_time = asyncio.get_event_loop().time()
            async for device, adv_data in scanner.advertisement_data():
                # Check timeout
                if timeout > 0 and (asyncio.get_event_loop().time() - start_time) > timeout:
                    break
                    
                # Apply name filter
                if name_filter and (not device.name or name_filter.lower() not in device.name.lower()):
                    continue
                    
                # Avoid duplicates (show each device once)
                device_key = (device.address, device.name)
                if device_key in seen_devices and not verbose:
                    continue
                seen_devices.add(device_key)
                    
                print(f"Device: {device.name or 'Unknown'} ({device.address})")
                print(f"  RSSI: {adv_data.rssi} dBm")
                
                if adv_data.local_name and adv_data.local_name != device.name:
                    print(f"  Local Name: {adv_data.local_name}")
                    
                if adv_data.service_uuids:
                    print(f"  Services: {', '.join(adv_data.service_uuids)}")
                    
                if show_manufacturer_data and adv_data.manufacturer_data:
                    print("  Manufacturer Data:")
                    for manufacturer_id, data in adv_data.manufacturer_data.items():
                        print(f"    ID {manufacturer_id}: {data.hex()}")
                        
                if verbose and adv_data.service_data:
                    print("  Service Data:")
                    for service_uuid, data in adv_data.service_data.items():
                        print(f"    {service_uuid}: {data.hex()}")
                        
                print()
                    
        except KeyboardInterrupt:
            print("Stopping scan...")
            raise
    
    print("Scan completed.")


def main() -> None:
    """Main entry point for the broadcast listener CLI command."""
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        asyncio.run(listen_to_broadcasts(
            timeout=args.timeout,
            name_filter=args.filter,
            verbose=args.verbose,
            show_manufacturer_data=args.manufacturer_data
        ))
    except KeyboardInterrupt:
        print("Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Example script demonstrating the high-level duplo library API.

This script shows different ways to use the duplo library for controlling
DUPLO trains, from simple one-liners to advanced usage patterns.

Run with: python examples/library_usage_demo.py
"""

import asyncio
import sys
from duplo import train_connection, simple_train_demo, find_train, TrainController
from bleak import BleakClient


async def example_1_simplest_usage():
    """Example 1: The simplest possible usage - one line demo."""
    print("=== Example 1: One-liner demo ===")
    try:
        await simple_train_demo(speed=40, run_time=8.0)
        print("✓ One-liner demo completed successfully!")
    except ConnectionError as e:
        print(f"✗ {e}")
    except Exception as e:
        print(f"✗ Error: {e}")
    print()


async def example_2_context_manager():
    """Example 2: Using the context manager for more control."""
    print("=== Example 2: Context manager usage ===")
    try:
        async with train_connection() as train:
            print("Connected to train, running demo sequence...")
            
            # Quick setup
            await train.quick_setup()
            
            # Demo sequence with convenience methods
            print("Playing horn and setting red lights...")
            await train.play_horn()
            await train.set_light_red()
            await asyncio.sleep(1)
            
            print("Starting train at 60% speed...")
            await train.set_motor_speed(0, 60)
            await asyncio.sleep(5)
            
            print("Switching to green lights...")
            await train.set_light_green()
            await asyncio.sleep(3)
            
            print("Emergency stop!")
            await train.emergency_stop()
            await asyncio.sleep(1)
            
            print("Playing station sound...")
            await train.play_station_sound()
            
        print("✓ Context manager demo completed successfully!")
    except ConnectionError as e:
        print(f"✗ {e}")
    except Exception as e:
        print(f"✗ Error: {e}")
    print()


async def example_3_advanced_usage():
    """Example 3: Advanced usage with manual connection management."""
    print("=== Example 3: Advanced manual control ===")
    try:
        # Manual device discovery
        print("Searching for train...")
        device = await find_train("Train Base", timeout=15.0)
        if not device:
            print("✗ No train found")
            return
            
        print(f"Found device: {device.name} ({device.address})")
        
        # Manual connection and control
        async with BleakClient(device) as client:
            controller = TrainController(client)
            await controller.setup_notifications()
            
            # Setup ports manually
            await controller.setup_port_input_format(port_id=1, mode=1)
            await asyncio.sleep(0.5)
            
            print("Running custom sequence...")
            # Custom sound and light sequence
            for sound_id in [5, 9, 3]:  # Station, horn, brake sounds
                await controller.play_sound(port_id=1, sound_id=sound_id)
                await asyncio.sleep(1)
                
            # Color cycling
            colors = [3, 5, 7, 9]  # Blue, red, green, yellow
            for color_id in colors:
                await controller.set_light_color(port_id=17, color_id=color_id)
                await asyncio.sleep(0.5)
                
            # Variable speed sequence
            print("Variable speed sequence...")
            for speed in [20, 40, 60, 40, 20, 0]:
                await controller.set_motor_speed(port_id=0, speed=speed)
                await asyncio.sleep(2)
                
        print("✓ Advanced demo completed successfully!")
    except Exception as e:
        print(f"✗ Error: {e}")
    print()


async def example_4_error_handling():
    """Example 4: Proper error handling patterns."""
    print("=== Example 4: Error handling patterns ===")
    
    # Try to connect to a non-existent train
    try:
        async with train_connection("Non-existent Train", timeout=5.0):
            pass
    except ConnectionError as e:
        print(f"✓ Properly caught connection error: {e}")
    
    # Demonstrate timeout handling
    try:
        device = await find_train("Another Fake Train", timeout=2.0)
        if device is None:
            print("✓ Properly handled device not found (None returned)")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
    print()


async def main():
    """Run all examples."""
    print("DUPLO Library Usage Examples")
    print("=" * 50)
    print("Note: These examples require a physical DUPLO train.")
    print("If no train is available, connection errors are expected.")
    print()
    
    # Run all examples
    await example_1_simplest_usage()
    await example_2_context_manager()
    await example_3_advanced_usage()
    await example_4_error_handling()
    
    print("All examples completed!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExamples interrupted by user")
        sys.exit(0)
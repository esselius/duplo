import asyncio
from itertools import cycle
from bleak import BleakClient, BleakScanner
from protocols.ble_toothbrush import ToothbrushEvent
from core.config import Config
from protocols.ble_duplo_train import (
    port_output_command,
    message_type,
    port_input_format_setup_single_format,
)

toothbrush = "Oral-B Toothbrush"
service_uuid = "0000fe0d-0000-1000-8000-00805f9b34fb"

config = Config()


def convert_speed_to_val(speed):
    """Map speed of -100 to 100 to a byte range

    * -100 to 100 (negative means reverse)
    * 0 is floating
    * 127 is brake

    Returns:
        byte
    """
    if speed == 127:
        return 127
    if speed > 100:
        speed = 100
    if speed < 0:
        # Now, truncate to 8-bits
        speed = speed & 255  # Or I guess I could do 256-abs(s)
    return speed


async def main() -> None:
    train = await BleakScanner().find_device_by_name("Train Base", timeout=30)
    assert train is not None
    print(train)

    speeds = cycle([0, 25, 50, 75, 100])

    async with BleakClient(train) as client:
        payload = port_input_format_setup_single_format.build(
            {
                "header": {
                    "length": 10,
                    "hub_id": 0,
                    "message_type": message_type.port_input_format_setup_single,
                },
                "port_id": 1,
                "mode": 1,
                "delta_interval": 1,
                "notification_enabled": 1,
            }
        )
        await client.write_gatt_char(
            config.CHAR_UUID,
            payload,
            response=False,
        )

        async with BleakScanner(service_uuids=[service_uuid]) as scanner:
            last_state = None
            async for _, adv_data in scanner.advertisement_data():
                data = adv_data.manufacturer_data[220]
                parsed = ToothbrushEvent.parse(data)
                if parsed != last_state:
                    if last_state is not None:
                        if parsed.state == "running" and last_state.state != "running":
                            print("Started brushing")
                            payload = port_output_command.build(
                                {
                                    "header": {
                                        "length": 8,
                                        "hub_id": 0,
                                        "message_type": message_type.port_output_command,
                                    },
                                    "port_id": 0,
                                    "startup_and_completion_information": {
                                        "startup": 1,
                                        "completion": 1,
                                    },
                                    "sub_command": 0x51,
                                    "payload": bytes([0, convert_speed_to_val(50)]),
                                }
                            )
                            await client.write_gatt_char(
                                config.CHAR_UUID, payload, response=False
                            )
                        if parsed.state == "idle" and last_state.state == "running":
                            print("Stopped brushing")
                            payload = port_output_command.build(
                                {
                                    "header": {
                                        "length": 8,
                                        "hub_id": 0,
                                        "message_type": message_type.port_output_command,
                                    },
                                    "port_id": 0,
                                    "startup_and_completion_information": {
                                        "startup": 1,
                                        "completion": 1,
                                    },
                                    "sub_command": 0x51,
                                    "payload": bytes([0, convert_speed_to_val(0)]),
                                }
                            )
                            await client.write_gatt_char(
                                config.CHAR_UUID, payload, response=False
                            )
                        if (
                            parsed.pressure.mode_button_pressed
                            and not last_state.pressure.mode_button_pressed
                        ):
                            print("Pressed mode button")
                            payload = port_output_command.build(
                                {
                                    "header": {
                                        "length": 8,
                                        "hub_id": 0,
                                        "message_type": message_type.port_output_command,
                                    },
                                    "port_id": 1,
                                    "startup_and_completion_information": {
                                        "startup": 1,
                                        "completion": 1,
                                    },
                                    "sub_command": 0x51,
                                    "payload": bytes([1, 9]),
                                }
                            )
                            await client.write_gatt_char(
                                config.CHAR_UUID, payload, response=False
                            )
                    last_state = parsed


asyncio.run(main())

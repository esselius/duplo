import asyncio

from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic

from core.config import Config
from protocols.ble_duplo_train import (
    common_message_header,
    message_type,
    port_input_format_setup_single_format,
    port_output_command,
    port_output_command_feedback,
    port_value_single,
    hub_attached_io_message_format,
    generic_error_message,
)

config = Config()


def notification_handler(sender: BleakGATTCharacteristic, data: bytearray) -> None:
    payload = common_message_header.parse(data)
    match payload.message_type:
        case message_type.hub_attached_io:
            payload = hub_attached_io_message_format.parse(data)
            print("Hub attached IO")
        case message_type.generic_error_message:
            payload = generic_error_message.parse(data)
            print("Error")
        case message_type.port_value_single:
            payload = port_value_single.parse(data)
            print("Port value")
        case message_type.port_input_format_single:
            payload = port_input_format_setup_single_format.parse(data)
            print("Port input format")
        case message_type.port_output_command_feedback:
            payload = port_output_command_feedback.parse(data)
            print("Port output command feedback")
    # print(f"{sender}: {data} == {payload}")


async def main() -> None:
    train = await BleakScanner().find_device_by_name("Train Base")
    assert train is not None
    print(train)

    async with BleakClient(train) as client:
        await client.start_notify(config.CHAR_UUID, notification_handler)

        # Play sound
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
        print(payload)
        await client.write_gatt_char(
            config.CHAR_UUID,
            payload,
            response=False,
        )
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
                "payload": bytes([1, 5]),
            }
        )
        await asyncio.sleep(1)
        print(payload)
        await client.write_gatt_char(config.CHAR_UUID, payload, response=False)

        # Change color
        payload = port_output_command.build(
            {
                "header": {
                    "length": 8,
                    "hub_id": 0,
                    "message_type": message_type.port_output_command,
                },
                "port_id": 17,
                "startup_and_completion_information": {
                    "startup": 1,
                    "completion": 1,
                },
                "sub_command": 0x51,
                "payload": bytes([0, 5]),
            }
        )
        print(payload)
        await client.write_gatt_char(config.CHAR_UUID, payload, response=False)

        await asyncio.sleep(1)

        # Set speed to 50%
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
                "payload": bytes([0, 50]),
            }
        )
        print(payload)
        await client.write_gatt_char(config.CHAR_UUID, payload, response=False)
        await asyncio.sleep(10)


asyncio.run(main())

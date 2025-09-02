import asyncio
from bleak import BleakScanner
from protocols.ble_toothbrush import ToothbrushEvent

toothbrush = "Oral-B Toothbrush"
service_uuid = "0000fe0d-0000-1000-8000-00805f9b34fb"


async def main() -> None:
    async with BleakScanner(service_uuids=[service_uuid]) as scanner:
        last_state = None
        async for ble_device, adv_data in scanner.advertisement_data():
            data = adv_data.manufacturer_data[220]
            # print(data)
            parsed = ToothbrushEvent.parse(data)
            if parsed != last_state:
                if last_state is not None:
                    # if parsed.state == "charging":
                    #     if (
                    #         parsed.pressure.mode_button_pressed
                    #         and not last_state.pressure.mode_button_pressed
                    #     ):
                    #         print("Pressed mode button")
                    #     if (
                    #         parsed.pressure.power_button_pressed
                    #         and not last_state.pressure.power_button_pressed
                    #     ):
                    #         print("Pressed power button")

                    # if (
                    #     parsed.pressure.mode_button_pressed
                    #     and not last_state.pressure.mode_button_pressed
                    # ) and parsed.mode != last_state.mode:
                    #     print("Long pressed mode button")
                    # if (
                    #     parsed.pressure.mode_button_pressed
                    #     == last_state.pressure.mode_button_pressed
                    # ) and parsed.mode != last_state.mode:
                    #     print("Short pressed mode button")
                    # if parsed.state == "running" and last_state.state != "running":
                    #     print("Started brushing")
                    # if parsed.state == "idle" and last_state.state == "running":
                    #     print("Stopped brushing")
                    if parsed.pressure.unknown1 != last_state.pressure.unknown1:
                        print(
                            "#################### Unknown1 changed {}".format(
                                parsed.pressure.unknown1
                            )
                        )
                    if parsed.pressure.unknown2 != last_state.pressure.unknown2:
                        print(
                            "#################### Unknown2 changed {}".format(
                                parsed.pressure.unknown2
                            )
                        )
                    if parsed.pressure.unknown3 != last_state.pressure.unknown3:
                        print(
                            "#################### Unknown3 changed {}".format(
                                parsed.pressure.unknown3
                            )
                        )
                    print(parsed)
                last_state = parsed


if __name__ == "__main__":
    asyncio.run(main())

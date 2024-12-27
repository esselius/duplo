from .decoder import HeaderMessage, Header, HubAttachedIoMessage, HubAttachedIo, IoTypeEnum, EventEnum, MessageTypeEnum

def test_parse_header_msg():
    # Length = 15, Hub ID = 0x00, Message Type = 0x04
    data = b'\x0F\x00\x04'

    parsed = HeaderMessage.parse(data)

    assert parsed.length == 15
    assert parsed.hub_id == 0
    assert parsed.message_type == 0x04

def test_parse_hub_attached_io_msg():
    data = b'\x0f\x00\x04\x14\x01\x14\x00\x01\x00\x00\x00\x01\x00\x00\x00'

    parsed = HubAttachedIoMessage.parse(data)

    assert parsed.header.length == 15
    assert parsed.header.hub_id == 0
    assert parsed.header.message_type == 0x04

    assert parsed.port == 20
    assert parsed.event == 1
    assert parsed.io_type_id == 20
    assert parsed.hardware_revision == 1
    assert parsed.software_revision == 1


def test_parse_hub_attached_io():
    data = b'\x0f\x00\x04\x14\x01\x14\x00\x01\x00\x00\x00\x01\x00\x00\x00'

    model = HubAttachedIo(**HubAttachedIoMessage.parse(data))

    assert model.header.length == 15
    assert model.header.hub_id == 0
    assert model.header.message_type == MessageTypeEnum.HubAttachedIo

    assert model.port == 20
    assert model.event == EventEnum.AttachedIo
    assert model.io_type_id == IoTypeEnum.Voltage
    assert model.hardware_revision == 1
    assert model.software_revision == 1

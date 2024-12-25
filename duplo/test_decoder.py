from .decoder import Header, HubAttachedIO

def test_parse_header():
    # Length = 15, Hub ID = 0x00, Message Type = 0x04
    data = b'\x0F\x00\x04'

    parsed = Header.parse(data)

    assert parsed.length == 15
    assert parsed.hub_id == 0
    assert parsed.message_type == 0x04

def test_parse_hub_attached_io_msg():
    data = b'\x0f\x00\x04\x14\x01\x14\x00\x01\x00\x00\x00\x01\x00\x00\x00'

    parsed = HubAttachedIO.parse(data)

    assert parsed.header.length == 15
    assert parsed.header.hub_id == 0
    assert parsed.header.message_type == 0x04

    assert parsed.port == 20
    assert parsed.event == 1
    assert parsed.io_type_id == 20
    assert parsed.hardware_revision == 1
    assert parsed.software_revision == 1


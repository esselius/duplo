from .decoder import Header

def test_parse_header():
    # Length = 15, Hub ID = 0x00, Message Type = 0x04
    data = b'\x0F\x00\x04'

    parsed = Header.parse(data)

    assert parsed.length == 15
    assert parsed.hub_id == 0
    assert parsed.message_type == 0x04



from protocols.ble_toothbrush import ToothbrushEvent


def test_parse_toothbrush_event():
    event = b"\x062k\x02r\x00\x03\x02\t\x00\x04"
    parsed = ToothbrushEvent.parse(event)
    assert parsed.model == b"\x062k"
    assert parsed.state == "idle"

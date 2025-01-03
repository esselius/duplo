from construct import (
    Struct,
    BitStruct,
    Nibble,
    Enum,
    Flag,
    GreedyBytes,
    Int8ul,
    Int16ul,
    Int32ul,
)

message_type = Enum(
    Int8ul,
    hub_actions=0x02,
    hub_attached_io=0x04,
    generic_error_message=0x05,
    port_information_request=0x21,
    port_input_format_setup_single=0x41,
    port_value_single=0x45,
    port_input_format_single=0x47,
    port_output_command=0x81,
    port_output_command_feedback=0x82,
)

io_type = Enum(
    Int16ul,
    voltage=0x0014,
    rgb_light=0x0017,
    duplo_train_motor=0x0029,
    duplo_train_speaker=0x002A,
    duplo_train_color=0x002B,
    duplo_train_speedometer=0x002C,
)

event = Enum(
    Int8ul,
    detached_io=0x00,
    attached_io=0x01,
    atttached_virtual_io=0x02,
)

duplo_speaker_sounds = Enum(
    Int8ul, station=5, water=7, horn=9, steam=10, **{"break": 3}
)

common_message_header = Struct(
    "length" / Int8ul, "hub_id" / Int8ul, "message_type" / message_type
)

hub_attached_io_message_format = Struct(
    "header" / common_message_header,
    "port_id" / Int8ul,
    "event" / event,
    "io_type" / io_type,
    "hardware_revision" / Int8ul,
    "software_revision" / Int8ul,
)

information_type = Enum(
    Int8ul,
    port_value=0x00,
    mode_info=0x01,
    possible_mode_combinations=0x02,
)

port_information_request_format = Struct(
    "header" / common_message_header,
    "port_id" / Int8ul,
    "information_type" / information_type,
)

port_input_format_setup_single_format = Struct(
    "header" / common_message_header,
    "port_id" / Int8ul,
    "mode" / Int8ul,
    "delta_interval" / Int32ul,
    "notification_enabled" / Flag,
)

port_value_single = Struct(
    "header" / common_message_header,
    "port_id" / Int8ul,
    "value" / GreedyBytes,
)

startup_and_completion_information = BitStruct(
    "startup" / Nibble,
    "completion" / Nibble,
)

port_output_command = Struct(
    "header" / common_message_header,
    "port_id" / Int8ul,
    "startup_and_completion_information" / startup_and_completion_information,
    "sub_command" / Int8ul,
    "payload" / GreedyBytes,
)

port_output_command_feedback = Struct(
    "header" / common_message_header,
    "port_id" / Int8ul,
    "port_feedback_message" / Int8ul,
)

ErrorCode = Enum(
    Int8ul,
    ACK=0x01,
    MACK=0x02,
    BUFFER_OVERFLOW=0x03,
    TIMEOUT=0x04,
    COMMAND_NOT_RECOGNIZED=0x05,
    INVALID_USE=0x06,
    OVERCURRENT=0x07,
    INTERNAL_ERROR=0x08,
)

generic_error_message = Struct(
    "header" / common_message_header, "command_type" / Int8ul, error_code=ErrorCode
)

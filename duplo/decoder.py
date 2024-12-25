from construct import Struct, Int8ul, Int16ul, Int32sl

Header = Struct(
    "length" / Int8ul,
    "hub_id" / Int8ul,
    "message_type" / Int8ul,
)

HubAttachedIO = Struct(
    "header" / Header,
    "port" / Int8ul,
    "event" / Int8ul,
    "io_type_id" / Int16ul,
    "hardware_revision" / Int32sl,
    "software_revision" / Int32sl,
)

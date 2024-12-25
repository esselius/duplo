from construct import Struct, Int8ul

Header = Struct(
    "length" / Int8ul,
    "hub_id" / Int8ul,
    "message_type" / Int8ul,
)

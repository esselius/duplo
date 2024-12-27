from construct import Struct, Int8ul, Int16ul, Int32sl
from enum import IntEnum
from pydantic import BaseModel

HeaderMessage = Struct(
    "length" / Int8ul,
    "hub_id" / Int8ul,
    "message_type" / Int8ul,
)

HubAttachedIoMessage = Struct(
    "header" / HeaderMessage,
    "port" / Int8ul,
    "event" / Int8ul,
    "io_type_id" / Int16ul,
    "hardware_revision" / Int32sl,
    "software_revision" / Int32sl,
)

class MessageTypeEnum(IntEnum):
    HubAttachedIo = 4

class Header(BaseModel):
    length: int
    hub_id: int
    message_type: MessageTypeEnum

class EventEnum(IntEnum):
    DetachedIo = 0
    AttachedIo = 1
    AttachedVirtualIo = 2

class IoTypeEnum(IntEnum):
    Voltage = 20
    RgbLight = 23
    DuploTrainMotor = 41
    DuploTrainSpeaker = 42
    DuploTrainColor = 43
    DuploTrainSpeedometer = 44

class HubAttachedIo(BaseModel):
    header: Header
    port: int
    event: EventEnum
    io_type_id: IoTypeEnum
    hardware_revision: int
    software_revision: int


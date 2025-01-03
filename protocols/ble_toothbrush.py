from construct import (
    Struct,
    BitStruct,
    Enum,
    Byte,
    Bytes,
    Flag,
)

State = Enum(
    Byte,
    unknown=0,
    initializing=1,
    idle=2,
    running=3,
    charging=4,
    setup=5,
    flight_menu=6,
    selection_menu=8,
    off=9,
)

Mode = Enum(
    Byte,
    daily_clean=0,
    sensitive=1,
    gum_care=2,
    whiten=3,
    intense=4,
    super_sensitive=5,
    tongue_clean=6,
    settings=8,
)

Pressure = BitStruct(
    "high_pressure" / Flag,
    "motor_speed" / Flag,
    "unknown1" / Flag,
    "unknown2" / Flag,
    "power_button_pressed" / Flag,
    "mode_button_pressed" / Flag,
    "timer_mode" / Flag,
    "unknown3" / Flag,
)

ToothbrushEvent = Struct(
    "model" / Bytes(3),
    "state" / State,
    "pressure" / Pressure,
    "brush_minutes" / Byte,
    "brush_seconds" / Byte,
    "mode" / Mode,
    "sector" / Byte,
    "sector_timer" / Byte,
    "sector_counter" / Byte,
)

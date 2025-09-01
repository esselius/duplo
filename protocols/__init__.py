"""BLE protocol definitions for DUPLO trains and toothbrush control."""

from .ble_duplo_train import (
    message_type,
    io_type,
    event,
    duplo_speaker_sounds,
    common_message_header,
    hub_attached_io_message_format,
    port_input_format_setup_single_format,
    port_output_command,
    port_output_command_feedback,
    generic_error_message,
    ErrorCode,
)
from .ble_toothbrush import ToothbrushEvent, State, Mode, Pressure

__all__ = [
    "message_type",
    "io_type", 
    "event",
    "duplo_speaker_sounds",
    "common_message_header",
    "hub_attached_io_message_format", 
    "port_input_format_setup_single_format",
    "port_output_command",
    "port_output_command_feedback",
    "generic_error_message",
    "ErrorCode",
    "ToothbrushEvent",
    "State",
    "Mode", 
    "Pressure",
]

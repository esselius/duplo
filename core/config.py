from uuid import UUID

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    UART_UUID: UUID = UUID("00001623-1212-efde-1623-785feabcd123")
    CHAR_UUID: UUID = UUID("00001624-1212-efde-1623-785feabcd123")

from uuid import UUID

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    UART_UUID: UUID
    CHAR_UUID: UUID

    class Config:
        env_file = ".env"

from pydantic import BaseModel

from .settings import (
    RabbitMQSettings,
)


class BaseAppSettings(BaseModel):
    rabbitmq: RabbitMQSettings = RabbitMQSettings()

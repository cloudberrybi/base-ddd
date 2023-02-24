import os

from pydantic import BaseModel


class RabbitMQSettings(BaseModel):
    host: str = os.environ.get('RABBITMQ_HOST', '127.0.0.1')
    port: int = int(os.environ.get('RABBITMQ_PORT', 5672))
    user: str = os.environ.get('RABBITMQ_USER', 'default')
    password: str = os.environ.get('RABBITMQ_PASSWORD', 'default')
    queue_prefix: str = os.environ.get('RABBITMQ_QUEUE_PREFIX', '')
    queue_postfix: str = os.environ.get('RABBITMQ_QUEUE_POSTFIX', '')


    def get_url(self):
        return f'amqp://{self.user}:{self.password}@{self.host}:{self.port}'

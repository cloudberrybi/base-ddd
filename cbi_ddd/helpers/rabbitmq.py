from cbi_ddd.repositories import SettingsRepository


config = SettingsRepository.get_config()

class RabbitMQHelper:
    @classmethod
    def queue_name(cls, name):
        return f'{config.rabbitmq.queue_prefix}{name}{config.rabbitmq.queue_postfix}'
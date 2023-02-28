class RabbitMQHelper:
    @classmethod
    def queue_name(cls, name):
        from cbi_ddd.repositories.settings_repository import SettingsRepository

        config = SettingsRepository.get_config()

        return f'{config.rabbitmq.queue_prefix}{name}{config.rabbitmq.queue_postfix}'
import pytest

from cbi_ddd.interfaces.settings import RabbitMQSettings

from ..interfaces import SampleAppSettings


@pytest.fixture
def empty_settings():
    return SampleAppSettings()

@pytest.fixture
def settings_with_rmq_full_config():
    return SampleAppSettings(
        rabbitmq=RabbitMQSettings(
            host='test',
            port=9999,
            user='test_user',
            password='test_password',
            queue_prefix='test1_',
            queue_postfix='_test2',
        )
    )

@pytest.fixture
def settings_with_rmq_partial_config():
    return SampleAppSettings(
        rabbitmq=RabbitMQSettings(
            host='test',
            user='test_user',
            queue_prefix='test3_',
            queue_postfix='_test4',
        )
    )

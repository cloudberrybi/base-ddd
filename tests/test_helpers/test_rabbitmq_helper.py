from cbi_ddd.helpers.rabbitmq import RabbitMQHelper

from ..fixtures.settings import (
    empty_settings,
    settings_with_rmq_full_config,
)


def test_queue_name(mocker, empty_settings):
    mocker.patch('cbi_ddd.repositories.SettingsRepository.get_config', return_value=empty_settings)

    assert RabbitMQHelper.queue_name('test') == 'test'

def test_queue_name_with_prefix_and_postfix(mocker, settings_with_rmq_full_config):
    mocker.patch('cbi_ddd.repositories.SettingsRepository.get_config', return_value=settings_with_rmq_full_config)

    assert RabbitMQHelper.queue_name('test') == 'test1_test_test2'

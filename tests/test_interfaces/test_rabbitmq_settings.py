from ..fixtures.settings import (
    settings_with_rmq_full_config,
    settings_with_rmq_partial_config,
)


def test_get_url_with_full_config(mocker, settings_with_rmq_full_config):
    mocker.patch('cbi_ddd.repositories.SettingsRepository.get_config', return_value=settings_with_rmq_full_config)

    from cbi_ddd.repositories import SettingsRepository

    assert SettingsRepository.get_config().rabbitmq.get_url() == 'amqp://test_user:test_password@test:9999'

def test_get_url_with_partial_config(mocker, settings_with_rmq_partial_config):
    mocker.patch('cbi_ddd.repositories.SettingsRepository.get_config', return_value=settings_with_rmq_partial_config)

    from cbi_ddd.repositories import SettingsRepository

    assert SettingsRepository.get_config().rabbitmq.get_url() == 'amqp://test_user:default@test:5672'

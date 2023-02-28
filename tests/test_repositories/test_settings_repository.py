from cbi_ddd.repositories import SettingsRepository

from ..interfaces.settings import SampleAppSettings


def test_load_local_config():
    SettingsRepository.settings_model = SampleAppSettings

    config = SettingsRepository.get_config(local_settings_path='./tests/config/empty.toml')

    assert config.test == 321

def test_load_non_existent_config():
    SettingsRepository.settings_model = SampleAppSettings

    config = SettingsRepository.get_config(local_settings_path='./tests/config/wrong.toml')

    assert config.test == 123

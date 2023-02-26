import os
import toml

from typing import Type

from cbi_ddd.interfaces import BaseAppSettings


class SettingsRepository:
    settings_model: Type[BaseAppSettings] = BaseAppSettings

    @classmethod
    def get_config(
        cls,
        env_name = 'CBI_CONFIG_FILE',
        local_settings_path = './config/local.toml',
    ) -> BaseAppSettings:
        config_path = os.environ.get(env_name, local_settings_path)

        if not os.path.exists(config_path):
            print('Not Exists!', config_path)
            return cls.settings_model()

        return cls.settings_model(
            **toml.load(config_path)
        )

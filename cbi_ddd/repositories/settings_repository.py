import os
import toml

from typing import Type

from cbi_ddd.interfaces import BaseAppSettings


class SettingsRepository:
    class opts:
        settings_model: Type[BaseAppSettings]

    @classmethod
    def get_config(
        cls,
        env_name = 'CBI_CONFIG_FILE',
        local_settings_path = './config/local.toml',
    ) -> BaseAppSettings:
        config_path = os.environ.get(env_name, local_settings_path)

        return cls.opts.settings_model(
            **toml.load(config_path)
        )

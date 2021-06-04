"""
This is the YAML configuration parser for Mailrise.
"""

import io
import typing as typ
from dataclasses import dataclass
from logging import Logger

import apprise # type: ignore
import yaml


class ConfigFileError(Exception):
    """Exception raised for invalid configuration files."""
    def __init__(self, message: str) -> None:
        self.message = message


@dataclass
class MailriseConfig:
    """Configuration data for a Mailrise instance."""
    logger: Logger
    listen_host: str
    listen_port: int
    smtp_hostname: typ.Optional[str]
    configs: dict[str, apprise.AppriseConfig]


def load_config(logger: Logger, f: io.TextIOWrapper) -> MailriseConfig:
    """Loads configuration data from a YAML file."""
    yml = yaml.safe_load(f)
    if not isinstance(yml, dict):
        raise ConfigFileError("root node not a mapping")

    yml_listen = yml.get('listen', {})

    yml_smtp = yml.get('smtp', {})

    yml_configs = yml.get('configs', [])
    if not isinstance(yml_configs, dict):
        raise ConfigFileError("'configs' node not a mapping")
    configs = {key: _load_apprise(config) for key, config in yml_configs.items()}

    logger.info('Loaded configuration with %d recipient(s)', len(configs))
    return MailriseConfig(
        logger=logger,
        listen_host=yml_listen.get('host', ''),
        listen_port=yml_listen.get('port', 8025),
        smtp_hostname=yml_smtp.get('hostname', None),
        configs=configs
    )


def _load_apprise(config: dict[str, typ.Any]) -> apprise.AppriseConfig:
    if not isinstance(config, dict):
        raise ConfigFileError("apprise node not a mapping")
    aconfig = apprise.AppriseConfig()
    aconfig.add_config(yaml.safe_dump(config), format='yaml')
    return aconfig

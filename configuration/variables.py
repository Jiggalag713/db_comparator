"""Module intended to store Variables class"""
from dataclasses import dataclass, field

from configuration.default_variables import DefaultValues
from configuration.sql_variables import SqlVariables
from configuration.system_config import SystemConfig


@dataclass
class Variables:
    """Intended to make together different internal variables"""
    default_values: DefaultValues = field(init=False, repr=True)
    system_config: SystemConfig = field(init=False, repr=True)

    def __post_init__(self):
        self.default_values: DefaultValues = DefaultValues()
        self.system_config: SystemConfig = SystemConfig()
        self.logger = self.system_config.logger
        self.sql_variables: SqlVariables = SqlVariables(self.logger)

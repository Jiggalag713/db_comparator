"""Module intended to store Variables class"""
from configuration.default_variables import DefaultValues
from configuration.sql_variables import SqlVariables
from configuration.system_config import SystemConfig


class Variables:
    """Intended to make together different internal variables"""
    def __init__(self):
        self.default_values: DefaultValues = DefaultValues()
        self.system_config: SystemConfig = SystemConfig()
        self.logger = self.system_config.logger
        self.sql_variables: SqlVariables = SqlVariables(self.logger)

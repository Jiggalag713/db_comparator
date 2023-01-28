"""Module intended for storing Configuration class"""
from configuration.sql_variables import SqlVariables
from configuration.ui_config import UIElements
from configuration.default_variables import DefaultValues


class Configuration:
    """Class intended to make together some different variables
    in purposes throwing of this to different methods"""
    def __init__(self, status_bar):
        self.is_toggled = True
        self.ui_elements = UIElements(self.is_toggled, status_bar)
        self.default_values = DefaultValues()
        self.sql_variables = SqlVariables(self.default_values.system_config.logger)

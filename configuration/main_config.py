"""Module intended for storing Configuration class"""
from dataclasses import dataclass, field

from PyQt5.QtWidgets import QStatusBar

from configuration.sql_variables import SqlVariables
from configuration.ui_config import UIElements
from configuration.default_variables import DefaultValues


@dataclass
class Configuration:
    """Class intended to make together some different variables
    in purposes throwing of this to different methods"""
    status_bar: QStatusBar
    is_toggled: bool = True
    default_values: DefaultValues = DefaultValues()
    ui_elements: UIElements = field(init=False, repr=True)

    def __post_init__(self):
        self.ui_elements = UIElements(self.is_toggled, self.status_bar)
        self.sql_variables = SqlVariables(self.default_values.system_config.logger)

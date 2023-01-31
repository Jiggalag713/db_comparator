"""Module intended to store AdvancedSettings class, main class of advanced
settings window"""
from PyQt5.QtWidgets import QDialog

from configuration.advanced_ui_config import UIElements
from ui_logic.advanced_window_logic import AdvancedWindowLogic


class AdvancedSettingsItem(QDialog):
    """Main class of advanced settings window"""
    def __init__(self, configuration):
        super().__init__()
        self.main_ui = UIElements()
        self.setLayout(self.main_ui.positions.grid)
        self.default_values = configuration.default_values
        self.advanced_logic = AdvancedWindowLogic(self, self.main_ui, self.default_values)
        self.main_ui.buttons.get('btn_ok').clicked.connect(self.advanced_logic.ok_pressed)
        self.main_ui.buttons.get('btn_cancel').clicked.connect(self.advanced_logic.cancel_pressed)
        self.main_ui.buttons.get('btn_reset').clicked.connect(self.advanced_logic.set_default)
        self.advanced_logic.set_default()
        self.setWindowTitle('Advanced settings')

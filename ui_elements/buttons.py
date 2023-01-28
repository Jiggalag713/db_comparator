"""Module contains class with buttons of main window"""
from PyQt5.QtWidgets import QPushButton


class Buttons:
    """Class contains buttons of main window"""
    def __init__(self):
        self.btn_set_configuration = QPushButton('       Compare!       ')
        self.btn_set_configuration.setShortcut('Ctrl+G')
        self.btn_set_configuration.setEnabled(False)
        self.btn_clear_all = QPushButton('Clear all')
        self.btn_advanced = QPushButton('Advanced')
        self.btn_check_prod = QPushButton('Check prod')
        self.btn_check_test = QPushButton('Check test')
        self.btn_clear_all.setToolTip('Reset all fields to default values')
        self.btn_set_configuration.setToolTip('Start comparing of dbs')

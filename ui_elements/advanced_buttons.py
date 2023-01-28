"""Module intended to store class Buttons for advanced settings window """
from PyQt5.QtWidgets import QPushButton


class Buttons:
    """Class contained buttons of advanced settings window"""
    def __init__(self):
        self.btn_ok = QPushButton('OK')
        self.btn_cancel = QPushButton('Cancel')
        self.btn_reset = QPushButton('Default settings')

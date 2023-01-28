"""Module intended to store Comboboxes classes for advanced settings window"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox


class Comboboxes:
    """Class intended to store comboboxes for advanced settings window"""
    def __init__(self):
        self.cb_logging_level: QComboBox = QComboBox()
        self.cb_logging_level.addItems(['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'])
        index = self.cb_logging_level.findText('NOTSET', Qt.MatchFixedString)
        if index >= 0:
            self.cb_logging_level.setCurrentIndex(index)
        self.cb_logging_level.setToolTip('Messages with this label and higher '
                                         'will be written to logs')

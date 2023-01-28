"""Module intended for storing UIElements class for advanced settings window"""
from typing import Dict

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QComboBox
from ui_elements.advanced_elements_position import ElementPositions
from ui_elements.advanced_labels import Labels
from ui_elements.advanced_line_edits import LineEdits


class UIElements:
    """Class make together all UI elements for advanced settings window"""
    def __init__(self):
        self.labels: Labels = Labels()
        self.line_edits: LineEdits = LineEdits()
        self.combo_boxes: QComboBox = self.get_comboboxes()
        self.buttons: Dict = {'btn_ok': QPushButton('OK'),
                              'btn_cancel': QPushButton('Cancel'),
                              'btn_reset': QPushButton('Default settings')}
        self.positions: ElementPositions = ElementPositions()
        self.positions.locate_elements(self.labels, self.line_edits, self.combo_boxes, self.buttons)

    def get_comboboxes(self) -> QComboBox:
        """Method intended to get logging_level combobox on advanced settings window"""
        cb_logging_level: QComboBox = QComboBox()
        cb_logging_level.addItems(['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'])
        index = cb_logging_level.findText('NOTSET', Qt.MatchFixedString)
        if index >= 0:
            cb_logging_level.setCurrentIndex(index)
        cb_logging_level.setToolTip('Messages with this label and higher '
                                    'will be written to logs')
        return cb_logging_level

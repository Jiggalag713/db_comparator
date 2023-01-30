"""Module contains custom clickable line edit class"""
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLineEdit


class ClickableLineEdit(QLineEdit):
    """Class implements custom clickable line edit"""
    clicked = pyqtSignal()

    def __init__(self):
        super().__init__()

    def mousePressEvent(self, event):
        """Method returns modal window by click on element"""
        self.clicked.emit()
        QLineEdit.mousePressEvent(self, event)

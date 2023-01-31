"""Module contains custom clickable line edit class"""
from PyQt5.QtCore import pyqtSignal, QEvent
from PyQt5.QtWidgets import QLineEdit


class ClickableLineEdit(QLineEdit):
    """Class implements custom clickable line edit"""
    clicked = pyqtSignal()

    def event(self, event):
        """Implements on click event"""
        if event.type() == QEvent.Type.MouseButtonPress:
            self.clicked.emit()
        return super().event(event)

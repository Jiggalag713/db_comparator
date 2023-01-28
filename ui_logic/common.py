"""Module contains common methods, intended for working with UI elements"""
from PyQt5.QtWidgets import QLineEdit


def set_value(widget: QLineEdit, value: str) -> None:
    """Method sets value to some widget"""
    widget.setText(value)
    widget.setCursorPosition(0)

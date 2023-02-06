"""Module contains common methods, intended for working with UI elements"""
from PyQt5.QtWidgets import QLineEdit

from configuration.main_config import Configuration


def set_ui_value(widget: QLineEdit, value: str) -> None:
    """Method sets value to some widget"""
    widget.setText(value)
    widget.setCursorPosition(0)


def set_value(widget, store, key) -> None:
    """Sets value from widget to some variable"""
    store.update({key: Configuration.transform_text(widget)})

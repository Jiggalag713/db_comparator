import pytest
from PyQt5.QtWidgets import QStatusBar

from main_file import MainUI
from ui_logic.buttons import ButtonsLogic
from ui_logic.config_serialization import ConfigSerialization
from ui_logic.line_edits import LineEditsLogic


@pytest.fixture(scope='session')
def status_bar():
    return QStatusBar()


@pytest.fixture(scope='session')
def main_window(status_bar):
    return MainUI(status_bar)


@pytest.fixture(scope='session')
def common_logic(main_window, status_bar):
    return ButtonsLogic(main_window.configuration, main_window.advanced_settings, status_bar)


@pytest.fixture(scope='session')
def line_edits_logic(main_window, status_bar):
    return LineEditsLogic(main_window.configuration)


@pytest.fixture(scope='session')
def config_serialization(common_logic, main_window):
    return ConfigSerialization(common_logic, main_window.configuration)

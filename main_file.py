#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Main class of application"""
import sys
from typing import NoReturn

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow

from configuration.main_config import Configuration
from custom_ui_elements.advanced_settings import AdvancedSettingsItem
from ui_elements.menu import Menu
from ui_logic.buttons import ButtonsLogic
from ui_logic.config_serialization import ConfigSerialization
from ui_logic.line_edits import LineEditsLogic


class MainUI(QWidget):
    """Class, contained almost all application UI elements"""
    def __init__(self, status_bar):
        super().__init__()
        self.status_bar = status_bar
        self.configuration = Configuration(self.status_bar)
        self.setLayout(self.configuration.ui_elements.positions.grid)
        line_edits = self.configuration.ui_elements.line_edits
        checkboxes = self.configuration.ui_elements.checkboxes
        radio_buttons = self.configuration.ui_elements.radio_buttons
        self.configuration.default_values.set_default_values(line_edits,
                                                             checkboxes,
                                                             radio_buttons)
        self.advanced_settings = AdvancedSettingsItem(self.configuration)
        self.setWindowTitle('dbComparator')
        self.setWindowIcon(QIcon('./resources/slowpoke.png'))
        self.show()

    @staticmethod
    def exit() -> NoReturn:
        """Method intended to exit from application"""
        sys.exit(0)


class MainWindow(QMainWindow):
    """MainWindow class contains all UI elements"""
    def __init__(self):
        super().__init__()

        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Prod disconnected, test disconnected')
        self.main_window = MainUI(self.status_bar)
        self.setCentralWidget(self.main_window)
        self.menubar = self.menuBar()
        self.common_logic = ButtonsLogic(self.main_window.configuration,
                                         self.main_window.advanced_settings,
                                         self.status_bar)
        self.line_edits_logic = LineEditsLogic(self.main_window.configuration)
        self.serialization = ConfigSerialization(self.common_logic, self.main_window.configuration)
        self.menu = Menu(self.main_window, self.common_logic, self.serialization, self.menubar)
        self.add_connects()

        self.setGeometry(300, 300, 900, 600)
        self.setWindowTitle('dbComparator')
        self.setWindowIcon(QIcon('./resources/slowpoke.png'))
        self.show()

    def add_connects(self):
        """Method intended for set connections between UI elements and methods"""
        buttons = self.main_window.configuration.ui_elements.buttons
        buttons.btn_advanced.clicked.connect(self.common_logic.advanced)
        buttons.btn_clear_all.clicked.connect(self.common_logic.clear_all)
        buttons.btn_set_configuration.clicked.connect(self.common_logic.start_work)
        buttons.btn_check_prod.clicked.connect(self.common_logic.check_prod_host)
        buttons.btn_check_test.clicked.connect(self.common_logic.check_test_host)

        line_edits = self.main_window.configuration.ui_elements.line_edits
        line_edits.excluded_tables.clicked.connect(self.line_edits_logic.set_excluded_tables)
        line_edits.excluded_columns.clicked.connect(self.line_edits_logic.set_excluded_columns)
        line_edits.included_tables.clicked.connect(self.line_edits_logic.set_included_tables)
        line_edits.prod.db.clicked.connect(self.line_edits_logic.set_prod_db)
        line_edits.test.db.clicked.connect(self.line_edits_logic.set_test_db)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())

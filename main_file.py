#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Main class of application"""
import sys
from typing import NoReturn

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction, qApp, QMenu, QStatusBar

from configuration.main_config import Configuration
from custom_ui_elements.advanced_settings import AdvancedSettingsItem
from ui_logic.buttons import ButtonsLogic
from ui_logic import config_serialization
from ui_logic.line_edits import LineEditsLogic
from ui_logic.table_calculation import TableCalculation


class MainUI(QWidget):
    """Class, contained almost all application UI elements"""
    def __init__(self, status_bar):
        super().__init__()
        self.status_bar: QStatusBar = status_bar
        self.configuration = Configuration()
        self.setLayout(self.configuration.ui_elements.positions.grid)
        line_edits = self.configuration.ui_elements.line_edits
        checkboxes = self.configuration.ui_elements.checkboxes
        radio_buttons = self.configuration.ui_elements.radio_buttons
        self.configuration.default_values.set_default_values(line_edits,
                                                             checkboxes,
                                                             radio_buttons)
        self.advanced_settings = AdvancedSettingsItem(self.configuration)
        self.setWindowTitle('db_comparator')
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
        table_calculation = TableCalculation(self.main_window.configuration)
        self.common_logic = ButtonsLogic(self.main_window, table_calculation)
        self.line_edits_logic = LineEditsLogic(self.main_window.configuration, table_calculation)
        self.menu: QMenu = self.get_menu()
        self.add_connects()

        self.setGeometry(300, 300, 900, 600)
        self.setWindowTitle('db_comparator')
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
        line_edits.prod.base.clicked.connect(self.line_edits_logic.set_prod_db)
        line_edits.test.base.clicked.connect(self.line_edits_logic.set_test_db)

    def get_menu(self) -> QMenu:
        """Method builds main window menu"""
        open_action: QAction = QAction(QIcon('open.png'), '&Open', self.main_window)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open custom file with cmp_properties')
        open_action.triggered.connect(lambda: config_serialization.load_configuration(self.main_window.configuration,
                                                                                      self.common_logic))

        compare_action: QAction = QAction(QIcon('compare.png'), '&Compare', self.main_window)
        compare_action.setShortcut('Ctrl+F')
        compare_action.setStatusTip('Run comparing')
        compare_action.triggered.connect(self.common_logic.start_work)

        save_action: QAction = QAction(QIcon('save.png'), '&Save', self.main_window)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Save current configuration to file')
        save_action.triggered.connect(lambda: config_serialization.save_configuration(self.main_window.configuration))

        exit_action = QAction(QIcon('exit.png'), '&Exit', self.main_window)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(qApp.quit)

        file_menu = self.menubar.addMenu('&File')
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(compare_action)
        file_menu.addAction(exit_action)
        return file_menu


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())

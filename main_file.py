#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Main class of application"""
import json
import os
import sys
from typing import NoReturn, Any, Union

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction, qApp, QCheckBox
from PyQt5.QtWidgets import QMenu, QStatusBar, QFileDialog

from configuration.main_config import Configuration
from configuration.variables import Variables
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
        self.variables = Variables()
        self.configuration = Configuration(self.variables)
        self.setLayout(self.configuration.ui_elements.positions.grid)
        checkboxes = self.configuration.ui_elements.checkboxes
        radio_buttons = self.configuration.ui_elements.radio_buttons
        self.configuration.variables.default_values.set_default_values(checkboxes,
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
        if self.status_bar is not None:
            self.status_bar.showMessage('Prod disconnected, test disconnected')
        self.main_window = MainUI(self.status_bar)
        self.setCentralWidget(self.main_window)
        self.menubar = self.menuBar()
        table_calculation = TableCalculation(self.main_window.configuration.variables)
        self.logic = ButtonsLogic(self.main_window, table_calculation)
        self.line_edits_logic = LineEditsLogic(self.main_window.configuration.variables)
        self.menu = self.get_menu()
        self.add_connects(table_calculation)

        self.setGeometry(300, 300, 900, 600)
        self.setWindowTitle('db_comparator')
        self.setWindowIcon(QIcon('./resources/slowpoke.png'))
        self.show()

    def add_connects(self, table_calculation):
        """Method intended for set connections between UI elements and methods"""
        buttons = self.main_window.configuration.ui_elements.buttons
        buttons.btn_advanced.clicked.connect(self.logic.advanced)
        buttons.btn_clear_all.clicked.connect(self.logic.clear_all)
        checkboxes = self.main_window.configuration.ui_elements.checkboxes
        check_schema = self.get_state(checkboxes.get('check_schema'))
        buttons.btn_set_configuration.clicked.connect(lambda: self.logic.start_work(check_schema))
        buttons.btn_check_prod.clicked.connect(self.logic.check_prod_host)
        buttons.btn_check_test.clicked.connect(self.logic.check_test_host)

        line_edits = self.main_window.configuration.ui_elements.line_edits
        line_edits.excluded_tables.clicked.connect(lambda:
                                                   self.set_excluded_tables(table_calculation))
        line_edits.excluded_columns.clicked.connect(self.set_excluded_columns)
        line_edits.included_tables.clicked.connect(lambda:
                                                   self.set_included_tables(table_calculation))
        line_edits.prod.base.clicked.connect(lambda: self.logic.set_db('prod'))
        line_edits.test.base.clicked.connect(lambda: self.logic.set_db('test'))

    def get_menu(self) -> Union[QMenu, None, Any]:
        """Method builds main window menu"""
        open_action: QAction = QAction(QIcon('open.png'), '&Open', self.main_window)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open custom file with cmp_properties')
        open_action.triggered.connect(self.load_properties)

        compare_action: QAction = QAction(QIcon('compare.png'), '&Compare', self.main_window)
        compare_action.setShortcut('Ctrl+F')
        compare_action.setStatusTip('Run comparing')
        checkboxes = self.main_window.configuration.ui_elements.checkboxes
        check_schema = self.get_state(checkboxes.get('check_schema'))
        compare_action.triggered.connect(lambda: self.logic.start_work(check_schema))

        save_action: QAction = QAction(QIcon('save.png'), '&Save', self.main_window)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Save current configuration to file')
        save_action.triggered.connect(self.save_properties)

        exit_action = QAction(QIcon('exit.png'), '&Exit', self.main_window)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(qApp.quit)

        if self.menubar is not None:
            file_menu = self.menubar.addMenu('&File')
        if file_menu is not None:
            file_menu.addAction(open_action)
            file_menu.addAction(save_action)
            file_menu.addAction(compare_action)
            file_menu.addAction(exit_action)
        return file_menu

    @staticmethod
    def get_state(checkbox: Any | None) -> bool:
        """Returns current state of checkbox"""
        if isinstance(checkbox, QCheckBox):
            return checkbox.isChecked()
        return True

    def save_properties(self):
        """Runs process for saving property """
        variables = self.main_window.configuration.variables
        config = config_serialization.save_configuration(variables)
        self.write_to_file(config, variables.logger)

    @staticmethod
    def write_to_file(data, logger) -> None:
        """Writes properties, converted to json, to file"""
        file_name, _ = QFileDialog.getSaveFileName(QFileDialog(),
                                                   "QFileDialog.getSaveFileName()", "",
                                                   "All Files (*);;Text Files (*.txt)")
        if file_name:
            with open(file_name, 'w', encoding="utf-8") as file:
                json.dump(data, file, indent=4)
            logger.info(f'Configuration successfully saved to {file_name}')

    def load_properties(self):
        """Runs process for loading properties"""
        self.open_file()
        common = self.logic
        self.main_window.configuration.load_from_internal()
        common.check_host(True, self.main_window.variables.sql_variables.prod)
        common.check_host(False, self.main_window.variables.sql_variables.test)

    def open_file(self):
        """Method loads application configuration from file"""
        file_name = QFileDialog.getOpenFileName(QFileDialog(), 'Open file',
                                                f'{os.getcwd()}/resources/properties/')[0]
        try:
            with open(file_name, 'r', encoding="utf-8") as file:
                data = file.read()
                config_serialization.deserialize_config(self.main_window.variables,
                                                        json.loads(data))
                self.main_window.variables.logger.debug('Configuration from file %s '
                                                        'successfully loaded...', file_name)
        except FileNotFoundError as err:
            self.main_window.variables.logger.warning('File not found, or, probably, '
                                                      'you just pressed cancel. Warn: '
                                                      '%s', err.args[1])

    def set_excluded_tables(self, table_calculation) -> None:
        """Method sets excluded tables"""
        selected_tables = self.line_edits_logic.get_selected_excluded_tables()
        line_edits = self.main_window.configuration.ui_elements.line_edits
        excluded_tables_line_edit = line_edits.excluded_tables
        excluded_tables_line_edit.setText(','.join(selected_tables))
        tables = self.main_window.configuration.variables.sql_variables.tables
        hard_excluded = tables.hard_excluded
        excluded_list = list(set(selected_tables) - set(hard_excluded))
        tables.excluded = table_calculation.get_tables_dict(excluded_list)
        tooltip_text = excluded_tables_line_edit.text().replace(',', ',\n')
        excluded_tables_line_edit.setToolTip(tooltip_text)
        table_calculation.calculate_excluded_columns()

    def set_included_tables(self, table_calculation) -> None:
        """Method sets included tables to UI"""
        selected_tables = self.line_edits_logic.get_selected_included_tables()
        line_edits = self.main_window.configuration.ui_elements.line_edits
        included_tables_line_edit = line_edits.included_tables
        tables = self.main_window.configuration.variables.sql_variables.tables
        tables.included = table_calculation.get_tables_dict(selected_tables)
        included_tables_line_edit.setText(','.join(selected_tables))
        line_edits.included_tables.setToolTip(','.join(selected_tables))

    def set_excluded_columns(self) -> None:
        """Method sets excluded columns"""
        selected_columns = self.line_edits_logic.get_selected_included_columns()
        line_edits = self.main_window.configuration.ui_elements.line_edits
        excluded_columns_line_edit = line_edits.excluded_columns
        columns = self.main_window.configuration.variables.sql_variables.columns
        columns.excluded = selected_columns
        excluded_columns_line_edit.setText(','.join(selected_columns))
        line_edits.excluded_columns.setToolTip(','.join(selected_columns))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())

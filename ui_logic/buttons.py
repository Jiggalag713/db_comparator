"""Module intended to store class with most common application logic"""
import logging

from PyQt5.QtWidgets import QMessageBox, QStatusBar, QLineEdit
from sqlalchemy import exc
from sqlalchemy.engine import Engine

from configuration.ui_config import UIElements
from configuration.variables import Variables
from custom_ui_elements.advanced_settings import AdvancedSettingsItem
from custom_ui_elements.progress_window import ProgressWindow
from helpers.sql_helper import SqlAlchemyHelper
from ui_elements.line_edits import SqlLineEdits
from ui_logic.line_edits import LineEditsLogic


class ButtonsLogic:
    """Class with implementation of most common application logic"""
    def __init__(self, main_window, table_calculation):
        self.advanced_settings: AdvancedSettingsItem = main_window.advanced_settings
        self.main_ui: UIElements = main_window.configuration.ui_elements
        self.status_bar: QStatusBar = main_window.status_bar
        self.logger: logging.Logger = main_window.configuration.logger
        self.variables: Variables = main_window.configuration.variables
        self.table_calculation = table_calculation

    def clear_all(self) -> None:
        """Method clears all inputs"""
        prod = self.main_ui.line_edits.prod
        test = self.main_ui.line_edits.test
        for key in prod.__dict__.keys():
            prod_le = prod.__dict__.get(key)
            test_le = test.__dict__.get(key)
            if isinstance(prod_le, QLineEdit):
                prod_le.clear()
            if isinstance(test_le, QLineEdit):
                test_le.clear()
        self.main_ui.line_edits.send_mail_to.clear()
        self.main_ui.line_edits.included_tables.clear()
        self.main_ui.line_edits.excluded_tables.clear()
        self.main_ui.line_edits.excluded_columns.clear()
        self.variables.default_values.set_default_values(self.main_ui.checkboxes,
                                                         self.main_ui.radio_buttons)
        self.main_ui.labels.prod.base.hide()
        self.main_ui.line_edits.prod.base.hide()
        self.main_ui.labels.test.base.hide()
        self.main_ui.line_edits.test.base.hide()
        self.main_ui.buttons.btn_set_configuration.setEnabled(False)
        self.status_bar.showMessage('Prod disconnected, test disconnected')

    def advanced(self) -> None:
        """Method works after pressing advanced button in main window"""
        self.advanced_settings.exec_()
        logging_level = self.variables.system_config.logging_level
        self.variables.system_config.logger.setLevel(logging_level)

    def start_work(self, schema_checking: bool) -> None:
        """Method starts process of comparing databases"""
        if all([self.variables.sql_variables.prod.tables,
                self.variables.sql_variables.test.tables]):
            self.logger.info('Comparing started!')
            progress = ProgressWindow(self.variables.sql_variables,
                                      schema_checking,
                                      self.variables.default_values.selected_schema_columns,
                                      self.variables.system_config.result_file)
            progress.exec()
        else:
            if not self.variables.sql_variables.prod.tables:
                self.logger.error("Prod tables variable is empty!")
            if not self.variables.sql_variables.test.tables:
                self.logger.error("Test tables variable is empty!")

    def check_prod_host(self) -> None:
        """Method checks connection to prod instance"""
        self.set_sql_credentials(self.variables.sql_variables.prod,
                                 self.main_ui.line_edits.prod)
        self.check_host(self.is_prod('prod'), self.variables.sql_variables.prod)

    def check_test_host(self) -> None:
        """Method checks connection to test instance"""
        self.set_sql_credentials(self.variables.sql_variables.test,
                                 self.main_ui.line_edits.test)
        self.check_host(self.is_prod('test'), self.variables.sql_variables.test)

    @staticmethod
    def set_sql_credentials(sql_instance: SqlAlchemyHelper,
                            line_edits_instance: SqlLineEdits) -> None:
        """Method sets sql credentials to SqlVariables class instance"""
        sql_instance.credentials.host = line_edits_instance.host.text()
        sql_instance.credentials.port = line_edits_instance.port.text()
        sql_instance.credentials.user = line_edits_instance.user.text()
        sql_instance.credentials.password = line_edits_instance.password.text()
        sql_instance.credentials.base = line_edits_instance.base.text()

    @staticmethod
    def is_prod(instance_type: str) -> bool:
        """Method checks is instance prod or test"""
        if instance_type == 'prod':
            return True
        return False

    def check_host(self, is_prod: bool, sql_instance: SqlAlchemyHelper) -> None:
        """Method implements common checking of connection"""
        sql_instance.warming_up()
        try:
            engine = sql_instance.engine
            if is_prod:
                self.main_ui.labels.prod.base.show()
                self.main_ui.line_edits.prod.base.show()
            else:
                self.main_ui.labels.test.base.show()
                self.main_ui.line_edits.test.base.show()
            if isinstance(engine, Engine):
                engine.connect()
                if is_prod:
                    self.main_ui.labels.prod.base.show()
                    self.main_ui.line_edits.prod.base.show()
                else:
                    self.main_ui.labels.test.base.show()
                    self.main_ui.line_edits.test.base.show()
                self.logger.info(f"Connection to {sql_instance.credentials.host}:"
                                 f"{sql_instance.credentials.host} "
                                 f"established successfully!")
                self.change_bar_message(is_prod, True, sql_instance)
            else:
                self.logger.error("Engine type is %s. Expected type is Engine", type(engine))
        except exc.SQLAlchemyError as err:
            self.logger.warning(f"Connection to {sql_instance.credentials.host} "
                                f"failed: {err.args[0]}")
            self.change_bar_message(is_prod, False, sql_instance)
            QMessageBox.warning(QMessageBox(), 'Warning',
                                f"Connection to {sql_instance.credentials.host} "
                                f"failed\n\n{err.args[0]}",
                                QMessageBox.Ok, QMessageBox.Ok)

    def set_db(self, instance_type) -> None:
        """Method sets prod database"""
        is_prod = True
        if instance_type != 'prod':
            is_prod = False
        line_edits = self.main_ui.line_edits
        sql_variables = self.variables.sql_variables.__dict__.get(instance_type)
        if isinstance(sql_variables, SqlAlchemyHelper):
            line_edits_logic = LineEditsLogic(self.variables)
            selected_db = line_edits_logic.set_db(sql_variables.databases,
                                                  sql_variables.credentials.base)
            sql_line_edit = line_edits.__dict__.get(instance_type)
            if isinstance(sql_line_edit, SqlLineEdits):
                sql_line_edit.base.setText(selected_db)
                sql_line_edit.base.setToolTip(selected_db)
            sql_instance = self.variables.sql_variables.__dict__.get(instance_type)
            if isinstance(sql_instance, SqlAlchemyHelper):
                self.logger.info(f"Connection to {sql_instance.credentials.host}:"
                                 f"{sql_instance.credentials.port}/{sql_instance.credentials.base} "
                                 f"established successfully!")
                self.change_bar_message(is_prod, True, sql_instance)
            else:
                self.logger.critical(f'Incompatible types of sql_instance: {type(sql_instance)}')

    def change_bar_message(self, stage_type: bool, value: bool,
                           sql_instance: SqlAlchemyHelper) -> None:
        """Method implements changing of message, displayed in status bar"""
        current_message = self.status_bar.currentMessage().split(', ')
        host_db = f'{sql_instance.credentials.host}:{sql_instance.credentials.base}'
        if stage_type:
            if value:
                self.status_bar.showMessage(f'{host_db} connected, {current_message[1]}')
            else:
                self.status_bar.showMessage(f'{host_db} disconnected, {current_message[1]}')
        else:
            if value:
                self.status_bar.showMessage(f'{current_message[0]}, {host_db} connected')
            else:
                self.status_bar.showMessage(f'{current_message[0]}, {host_db} disconnected')
        sql_instance.warming_up()
        if all([self.variables.sql_variables.prod.tables,
                self.variables.sql_variables.test.tables]):
            self.main_ui.buttons.btn_set_configuration.setEnabled(True)
            self.variables.sql_variables.tables.all = self.table_calculation.calculate_table_list()
            self.variables.sql_variables.tables.get_compare()
            self.table_calculation.calculate_includes_excludes()
            included_tables = self.variables.sql_variables.tables.included
            self.main_ui.line_edits.included_tables.setText(','.join(included_tables))
            self.main_ui.line_edits.included_tables.setToolTip(','.join(included_tables))
            hard_excluded = self.variables.sql_variables.tables.hard_excluded
            common_excluded_tables = self.variables.sql_variables.tables.excluded.copy()
            common_excluded_tables.update(hard_excluded)
            self.main_ui.line_edits.excluded_tables.setText(','.join(common_excluded_tables.keys()))
            self.main_ui.line_edits.excluded_tables.setToolTip(','.join(common_excluded_tables))

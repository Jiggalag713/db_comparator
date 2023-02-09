"""Module intended to store class with most common application logic"""
import logging
import pymysql

from PyQt5.QtWidgets import QMessageBox, QStatusBar

from configuration.main_config import Configuration
from configuration.ui_config import UIElements
from configuration.variables import Variables
from custom_ui_elements.advanced_settings import AdvancedSettingsItem
from custom_ui_elements.progress_window import ProgressWindow
from helpers.sql_helper import SqlAlchemyHelper
from ui_elements.line_edits import SqlLineEdits


class ButtonsLogic:
    """Class with implementation of most common application logic"""
    def __init__(self, main_window, table_calculation):
        self.configuration: Configuration = main_window.configuration
        self.advanced_settings: AdvancedSettingsItem = main_window.advanced_settings
        self.main_ui: UIElements = main_window.configuration.ui_elements
        self.status_bar: QStatusBar = main_window.status_bar
        self.logger: logging.Logger = self.configuration.logger
        self.variables: Variables = self.configuration.variables
        self.table_calculation = table_calculation

    def clear_all(self) -> None:
        """Method clears all inputs"""
        self.main_ui.line_edits.prod.host.clear()
        self.main_ui.line_edits.prod.user.clear()
        self.main_ui.line_edits.prod.password.clear()
        self.main_ui.line_edits.prod.base.clear()
        self.main_ui.line_edits.test.host.clear()
        self.main_ui.line_edits.test.user.clear()
        self.main_ui.line_edits.test.password.clear()
        self.main_ui.line_edits.test.base.clear()
        self.main_ui.line_edits.send_mail_to.clear()
        self.main_ui.line_edits.included_tables.clear()
        self.variables.default_values.set_default_values(self.main_ui.line_edits,
                                                         self.main_ui.checkboxes,
                                                         self.main_ui.radio_buttons)
        self.main_ui.labels.prod.base.hide()
        self.main_ui.line_edits.prod.base.hide()
        self.main_ui.labels.test.base.hide()
        self.main_ui.line_edits.test.base.hide()
        self.status_bar.showMessage('Prod disconnected, test disconnected')

    def advanced(self) -> None:
        """Method works after pressing advanced button in main window"""
        self.advanced_settings.exec_()
        logging_level = self.variables.system_config.logging_level
        self.variables.system_config.logger.setLevel(logging_level)

    def start_work(self) -> None:
        """Method starts process of comparing databases"""
        if all([self.variables.sql_variables.prod.tables,
                self.variables.sql_variables.test.tables]):
            # comparing_info = Info(self.logger)
            # prod_sql_connection = self.sql_variables.prod
            # test_sql_connection = self.sql_variables.test
            # comparing_info.update_table_list("prod", prod_sql_connection.get_tables())
            # comparing_info.update_table_list("test", test_sql_connection.get_tables())
            # mapping = query_constructor.prepare_column_mapping(prod_sql_connection, self.logger)
            # comparing_object = sql_comparing.Object(prod_sql_connection, test_sql_connection,
            #                                         self.configuration.default_values,
            #                                         comparing_info)
            self.logger.info('Comparing started!')
            included_tables = self.variables.sql_variables.tables.included
            if not included_tables:
                for table in self.variables.sql_variables.tables.excluded:
                    if table in self.variables.sql_variables.tables.included:
                        self.variables.sql_variables.tables.included.pop(table)
                        self.logger.debug(f'Deleted table {table} from self.tables list')
            enabled_dfs = self.main_ui.checkboxes.get('use_dataframes').isChecked()
            progress = ProgressWindow(self.configuration, enabled_dfs)
            progress.exec()

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
        try:
            sql_instance.warming_up()
            if is_prod:
                if sql_instance.tables:
                    self.main_ui.labels.prod.base.show()
                    self.main_ui.line_edits.prod.base.show()
            else:
                if sql_instance.tables:
                    self.main_ui.labels.test.base.show()
                    self.main_ui.line_edits.test.base.show()
            self.logger.info(f"Connection to {sql_instance.credentials.host}:"
                             f"{sql_instance.credentials.host} "
                             f"established successfully!")
            self.change_bar_message(is_prod, True, sql_instance)
        except pymysql.OperationalError as err:
            self.logger.warning(f"Connection to {sql_instance.credentials.host} "
                                f"failed\n\n{err.args[1]}")
            QMessageBox.warning(QMessageBox(), 'Warning',
                                f"Connection to {sql_instance.credentials.host} "
                                f"failed\n\n{err.args[1]}",
                                QMessageBox.Ok, QMessageBox.Ok)
        except pymysql.InternalError as err:
            self.logger.warning(f"Connection to {sql_instance.credentials.host} "
                                f"failed\n\n{err.args[1]}")
            QMessageBox.warning(QMessageBox(), 'Warning',
                                f"Connection to {sql_instance.credentials.host} "
                                f"failed\n\n{err.args[1]}", QMessageBox.Ok, QMessageBox.Ok)

    def change_bar_message(self, stage_type: bool, value: bool,
                           sql_instance: SqlAlchemyHelper) -> None:
        """Method implements changing of message, displayed in status bar"""
        current_message = self.status_bar.currentMessage().split(', ')
        host_db = f'{sql_instance.credentials.host}:{sql_instance.credentials.base}'
        if not stage_type:
            if value:
                self.status_bar.showMessage(f'{host_db} connected, {current_message[1]}')
            else:
                self.status_bar.showMessage(f'{host_db} disconnected, {current_message[1]}')
        else:
            if value:
                self.status_bar.showMessage(f'{current_message[0]}, {host_db} connected')
            else:
                self.status_bar.showMessage(f'{current_message[0]}, {host_db} disconnected')
        if all([self.variables.sql_variables.prod.tables,
                self.variables.sql_variables.test.tables]):
            self.configuration.ui_elements.buttons.btn_set_configuration.setEnabled(True)
            self.variables.sql_variables.tables.all = self.table_calculation.calculate_table_list()
            tables = self.variables.sql_variables.tables.all
            self.table_calculation.calculate_includes_excludes(tables)

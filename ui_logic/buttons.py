"""Module intended to store class with most common application logic"""
import logging
import pymysql

from PyQt5.QtWidgets import QMessageBox, QStatusBar, QLineEdit

from configuration.main_config import Configuration
from configuration.default_variables import DefaultValues
from configuration.sql_variables import SqlVariables
from configuration.ui_config import UIElements
from custom_ui_elements.advanced_settings import AdvancedSettingsItem
from custom_ui_elements.progress_window import ProgressWindow
from helpers.sql_helper import SqlAlchemyHelper
from ui_elements.line_edits import SqlLineEdits
from ui_logic.table_calculation import TableCalculation


class ButtonsLogic:
    """Class with implementation of most common application logic"""
    def __init__(self, configuration: Configuration,
                 advanced_settings: AdvancedSettingsItem, status_bar: QStatusBar):
        self.configuration: Configuration = configuration
        self.advanced_settings: AdvancedSettingsItem = advanced_settings
        self.main_ui: UIElements = configuration.ui_elements
        self.status_bar: QStatusBar = status_bar
        self.logger: logging.Logger = self.configuration.default_values.system_config.logger
        self.sql_variables: SqlVariables = self.configuration.sql_variables
        self.default_values: DefaultValues = self.configuration.default_values



    def clear_all(self) -> None:
        """Method clears all inputs"""
        self.main_ui.line_edits.prod.host.clear()
        self.main_ui.line_edits.prod.user.clear()
        self.main_ui.line_edits.prod.password.clear()
        self.main_ui.line_edits.prod.db.clear()
        self.main_ui.line_edits.test.host.clear()
        self.main_ui.line_edits.test.user.clear()
        self.main_ui.line_edits.test.password.clear()
        self.main_ui.line_edits.test.db.clear()
        self.main_ui.line_edits.send_mail_to.clear()
        self.main_ui.line_edits.included_tables.clear()
        self.default_values.set_default_values(self.main_ui.line_edits,
                                               self.main_ui.checkboxes,
                                               self.main_ui.radio_buttons)
        self.main_ui.labels.prod.db.hide()
        self.main_ui.line_edits.prod.db.hide()
        self.main_ui.labels.test.db.hide()
        self.main_ui.line_edits.test.db.hide()
        self.status_bar.showMessage('Prod disconnected, test disconnected')

    def advanced(self) -> None:
        """Method works after pressing advanced button in main window"""
        self.advanced_settings.exec_()
        logging_level = self.configuration.default_values.system_config.logging_level
        self.configuration.default_values.logger.setLevel(logging_level)

    def start_work(self) -> None:
        """Method starts process of comparing databases"""
        if all([self.configuration.sql_variables.prod.tables, self.sql_variables.test.tables]):
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
            included_tables = self.configuration.sql_variables.included_tables
            if included_tables:
                result_tables = {}
                for table in included_tables:
                    value = self.configuration.sql_variables.included_tables.get(table)
                    result_tables.update({table: value})
                self.configuration.sql_variables.included_tables = result_tables
            else:
                for table in self.configuration.default_values.excluded_tables:
                    if table in self.configuration.sql_variables.included_tables:
                        self.configuration.sql_variables.included_tables.pop(table)
                        self.logger.debug(f'Deleted table {table} from self.tables list')
            enabled_dfs = self.main_ui.checkboxes.use_dataframes.isChecked()
            progress = ProgressWindow(self.configuration, enabled_dfs)
            progress.exec()

    def check_prod_host(self) -> None:
        """Method checks connection to prod instance"""
        self.set_sql_credentials(self.sql_variables.prod,
                                 self.configuration.ui_elements.line_edits.prod)
        self.check_host(self.is_prod('prod'), self.sql_variables.prod)

    def check_test_host(self) -> None:
        """Method checks connection to test instance"""
        self.set_sql_credentials(self.sql_variables.test,
                                 self.configuration.ui_elements.line_edits.test)
        self.check_host(self.is_prod('test'), self.sql_variables.test)

    @staticmethod
    def set_sql_credentials(sql_instance: SqlAlchemyHelper,
                            line_edits_instance: SqlLineEdits) -> None:
        """Method sets sql credentials to SqlVariables class instance"""
        sql_instance.host = line_edits_instance.host.text()
        sql_instance.user = line_edits_instance.user.text()
        sql_instance.password = line_edits_instance.password.text()
        sql_instance.db = line_edits_instance.db.text()

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
                    self.main_ui.labels.prod.db.show()
                    self.main_ui.line_edits.prod.db.show()
            else:
                if sql_instance.tables:
                    self.main_ui.labels.test.db.show()
                    self.main_ui.line_edits.test.db.show()
            self.logger.info(f"Connection to {sql_instance.host} established successfully!")
            self.change_bar_message(is_prod, True, sql_instance)
        except pymysql.OperationalError as err:
            self.logger.warning(f"Connection to {sql_instance.host} failed\n\n{err.args[1]}")
            QMessageBox.warning(QMessageBox(), 'Warning',
                                f"Connection to {sql_instance.host} failed\n\n{err.args[1]}",
                                QMessageBox.Ok, QMessageBox.Ok)
        except pymysql.InternalError as err:
            self.logger.warning(f"Connection to {sql_instance.host} failed\n\n{err.args[1]}")
            QMessageBox.warning(QMessageBox(), 'Warning',
                                f"Connection to {sql_instance.host} failed\n\n{err.args[1]}",
                                QMessageBox.Ok, QMessageBox.Ok)

    def change_bar_message(self, stage_type: bool, value: bool,
                           sql_instance: SqlAlchemyHelper) -> None:
        """Method implements changing of message, displayed in status bar"""
        current_message = self.status_bar.currentMessage().split(', ')
        host_db = f'{sql_instance.host}:{sql_instance.db}'
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
        if all([self.configuration.sql_variables.prod.tables,
                self.configuration.sql_variables.test.tables]):
            self.configuration.ui_elements.buttons.btn_set_configuration.setEnabled(True)
            TableCalculation(self.configuration).calculate_table_list()

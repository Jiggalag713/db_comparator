"""Module intended to store logic, worked on advanced settings window"""
import logging
from typing import Any

from PyQt5.QtWidgets import QLineEdit

from configuration.default_variables import DefaultValues
from configuration.advanced_ui_config import UIElements
from custom_ui_elements.clickable_item_view import ClickableItemsView
from helpers.sql_helper import SqlCredentials, SqlAlchemyHelper


class AdvancedWindowLogic:
    """Class intended to store logic, worked on advanced settings window"""
    def __init__(self, advanced_window, main_ui, config):
        self.advanced_window = advanced_window
        self.main_ui: UIElements = main_ui
        self.system_config = config.variables.system_config
        self.variables = config.variables
        self.default_values: DefaultValues = config.variables.default_values
        self.logger: logging.Logger = config.logger

    def ok_pressed(self) -> None:
        """Method saves values on advanced settings window when OK button pressed"""
        logging_level = self.main_ui.combo_boxes.currentText()
        self.system_config.logging_level = self.set_logging_level(logging_level)
        comparing_step = self.main_ui.line_edits.comparing_step.text()
        self.default_values.constants.update({'comparing_step': int(comparing_step)})
        depth_report_check = self.main_ui.line_edits.depth_report_check.text()
        self.default_values.constants.update({'depth_report_check': int(depth_report_check)})
        schema_columns = self.main_ui.line_edits.schema_columns.text().split(',')
        self.default_values.selected_schema_columns = schema_columns
        retry_attempts = self.main_ui.line_edits.retry_attempts.text()
        self.default_values.constants.update({'retry_attempts': int(retry_attempts)})
        path_to_logs = self.main_ui.line_edits.path_to_logs.text()
        self.system_config.path_to_logs = path_to_logs
        table_timeout = self.main_ui.line_edits.table_timeout.text()
        self.default_values.constants.update({'table_timeout': int(table_timeout)})
        string_amount = self.main_ui.line_edits.strings_amount.text()
        self.default_values.constants.update({'strings_amount': int(string_amount)})
        self.advanced_window.close()

    @staticmethod
    def set_logging_level(current_level: str) -> int:
        """Method gets text logging level, transform it to logging format and returns it"""
        logging_levels = {
            'NOTSET': logging.NOTSET,
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARN': logging.WARN,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        return logging_levels.get(current_level, 10)

    def cancel_pressed(self) -> None:
        """Method worked when cancel button pressed"""
        self.advanced_window.close()

    def set_default(self) -> None:
        """Method set default values on advanced settings window"""
        default_values = DefaultValues()
        self.main_ui.combo_boxes.setCurrentIndex(4)
        mapping = [
            (self.main_ui.line_edits.comparing_step,
             default_values.constants.get('comparing_step')),
            (self.main_ui.line_edits.depth_report_check,
             default_values.constants.get('depth_report_check')),
            (self.main_ui.line_edits.schema_columns,
             ','.join(default_values.selected_schema_columns)),
            (self.main_ui.line_edits.retry_attempts,
             default_values.constants.get('retry_attempts')),
            (self.main_ui.line_edits.table_timeout,
             default_values.constants.get('table_timeout')),
            (self.main_ui.line_edits.strings_amount,
             default_values.constants.get('strings_amount')),
            (self.main_ui.line_edits.path_to_logs,
             self.system_config.path_to_logs)
        ]
        for item in mapping:
            self.set_default_value(*item)

    @staticmethod
    def set_default_value(element: QLineEdit, value: Any):
        """Method set given value in given lineedit"""
        element.setText(str(value))
        element.setCursorPosition(0)

    def set_schema_columns(self):
        """Sets schema columns"""
        if not self.default_values.schema_columns:
            self.default_values.schema_columns = self.get_schema_columns()
        if self.default_values.selected_schema_columns:
            selected_schema_columns = self.default_values.selected_schema_columns
        else:
            selected_schema_columns = self.default_values.schema_columns
        schema_columns = ClickableItemsView(self.default_values.schema_columns,
                                            selected_schema_columns)
        schema_columns.exec_()
        text = ','.join(schema_columns.selected_items)
        self.main_ui.line_edits.schema_columns.setText(text)
        self.default_values.selected_schema_columns = schema_columns.selected_items
        tooltip_text = self.main_ui.line_edits.schema_columns.text().replace(',', ',\n')
        self.main_ui.line_edits.schema_columns.setToolTip(tooltip_text)

    def get_schema_columns(self):
        """Returns full list of columns of information_schema for schema comparing"""
        host = self.variables.sql_variables.prod.credentials.host
        user = self.variables.sql_variables.prod.credentials.user
        password = self.variables.sql_variables.prod.credentials.password
        columns = []
        base = 'information_schema'
        info_schema_creds = SqlCredentials(host=host, user=user, password=password, base=base)
        engine = SqlAlchemyHelper(info_schema_creds, self.logger).engine
        result = engine.execute("describe information_schema.columns;")
        raw = result.fetchall()
        for item in raw:
            columns.append(item[0])
        return columns

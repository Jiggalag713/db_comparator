"""Module intended to store logic, worked on advanced settings window"""
import logging
from typing import Any

from PyQt5.QtWidgets import QLineEdit

from configuration.default_variables import DefaultValues
from configuration.advanced_ui_config import UIElements


class AdvancedWindowLogic:
    """Class intended to store logic, worked on advanced settings window"""
    def __init__(self, advanced_window, main_ui, default_values):
        self.advanced_window = advanced_window
        self.main_ui: UIElements = main_ui
        self.default_values: DefaultValues = default_values
        self.logger: logging.Logger = self.default_values.system_config.logger

    def ok_pressed(self) -> None:
        """Method saves values on advanced settings window when OK button pressed"""
        logging_level = self.main_ui.combo_boxes.cb_logging_level.currentText()
        self.default_values.logging_level = self.set_logging_level(logging_level)
        comparing_step = self.main_ui.line_edits.comparing_step.text()
        self.default_values.comparing_step = comparing_step
        depth_report_check = self.main_ui.line_edits.depth_report_check.text()
        self.default_values.depth_report_check = depth_report_check
        schema_columns = self.main_ui.line_edits.schema_columns.text().split(',')
        self.default_values.schema_columns = schema_columns
        retry_attemtps = self.main_ui.line_edits.retry_attempts.text()
        self.default_values.retry_attempts = retry_attemtps
        path_to_logs = self.main_ui.line_edits.path_to_logs.text()
        self.default_values.system_config.path_to_logs = path_to_logs
        table_timeout = self.main_ui.line_edits.table_timeout.text()
        self.default_values.table_timeout = table_timeout
        string_amount = self.main_ui.line_edits.strings_amount.text()
        self.default_values.strings_amount = string_amount
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
        return logging_levels.get(current_level)

    def cancel_pressed(self) -> None:
        """Method worked when cancel button pressed"""
        self.advanced_window.close()

    def set_default(self) -> None:
        """Method set default values on advanced settings window"""
        self.main_ui.combo_boxes.cb_logging_level.setCurrentIndex(4)
        le_comparing_step = self.main_ui.line_edits.comparing_step
        comparing_step = self.default_values.comparing_step
        self.default_values.comparing_step = self.set_default_value(le_comparing_step,
                                                                    comparing_step)
        le_depth_report_check = self.main_ui.line_edits.depth_report_check
        depth_report_check = self.default_values.depth_report_check
        self.default_values.depth_report_check = self.set_default_value(le_depth_report_check,
                                                                        depth_report_check)
        le_schema_columns = self.main_ui.line_edits.schema_columns
        schema_columns = ','.join(self.default_values.schema_columns)
        self.default_values.schema_columns = self.set_default_value(le_schema_columns,
                                                                    schema_columns)
        le_retry_attempts = self.main_ui.line_edits.retry_attempts
        retry_attempts = self.default_values.retry_attempts
        self.default_values.retry_attempts = self.set_default_value(le_retry_attempts,
                                                                    retry_attempts)
        le_table_timeout = self.main_ui.line_edits.table_timeout
        table_timeout = self.default_values.table_timeout
        self.default_values.table_timeout = self.set_default_value(le_table_timeout,
                                                                   table_timeout)
        le_strings_amount = self.main_ui.line_edits.strings_amount
        strings_amount = self.default_values.strings_amount
        self.default_values.strings_amount = self.set_default_value(le_strings_amount,
                                                                    strings_amount)
        le_path_to_logs = self.main_ui.line_edits.path_to_logs
        path_to_logs = f'{self.default_values.system_config.path_to_logs}'
        self.default_values.system_config.path_to_logs = self.set_default_value(le_path_to_logs,
                                                                                path_to_logs)

    @staticmethod
    def set_default_value(element: QLineEdit, value: Any) -> Any:
        """Method set given value in given lineedit"""
        element.setText(str(value))
        element.setCursorPosition(0)
        return value

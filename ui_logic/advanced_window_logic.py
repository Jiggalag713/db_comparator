"""Module intended to store logic, worked on advanced settings window"""
import logging
from typing import Any

from PyQt5.QtWidgets import QLineEdit

from configuration.default_variables import DefaultValues
from configuration.advanced_ui_config import UIElements


# TODO: FIX LINT
class AdvancedWindowLogic:
    """Class intended to store logic, worked on advanced settings window"""
    def __init__(self, advanced_window, main_ui, default_values):
        self.advanced_window = advanced_window
        self.main_ui: UIElements = main_ui
        self.default_values: DefaultValues = default_values
        self.logger: logging.Logger = self.default_values.system_config.logger

    def ok_pressed(self) -> None:
        """Method saves values on advanced settings window when OK button pressed"""
        self.default_values.logging_level = self.set_logging_level(self.main_ui.combo_boxes.cb_logging_level.currentText())
        self.default_values.comparing_step = self.main_ui.line_edits.comparing_step.text()
        self.default_values.depth_report_check = self.main_ui.line_edits.depth_report_check.text()
        self.default_values.schema_columns = self.main_ui.line_edits.schema_columns.text().split(',')
        self.default_values.retry_attempts = self.main_ui.line_edits.retry_attempts.text()
        self.default_values.system_config.path_to_logs = self.main_ui.line_edits.path_to_logs.text()
        self.default_values.table_timeout = self.main_ui.line_edits.table_timeout.text()
        self.default_values.strings_amount = self.main_ui.line_edits.strings_amount.text()
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
        self.default_values.comparing_step = self.set_default_value(self.main_ui.line_edits.comparing_step,
                                                                    self.default_values.comparing_step)
        self.default_values.depth_report_check = self.set_default_value(self.main_ui.line_edits.depth_report_check,
                                                                        self.default_values.depth_report_check)
        self.default_values.schema_columns = self.set_default_value(self.main_ui.line_edits.schema_columns,
                                                                    ','.join(self.default_values.schema_columns))
        self.default_values.retry_attempts = self.set_default_value(self.main_ui.line_edits.retry_attempts,
                                                                    self.default_values.retry_attempts)
        self.default_values.table_timeout = self.set_default_value(self.main_ui.line_edits.table_timeout,
                                                                   self.default_values.table_timeout)
        self.default_values.strings_amount = self.set_default_value(self.main_ui.line_edits.strings_amount,
                                                                    self.default_values.strings_amount)
        self.default_values.system_config.path_to_logs = self.set_default_value(self.main_ui.line_edits.path_to_logs,
                                                                                f'{self.default_values.system_config.path_to_logs}')

    @staticmethod
    def set_default_value(element: QLineEdit, value: Any) -> Any:
        """Method set given value in given lineedit"""
        element.setText(str(value))
        element.setCursorPosition(0)
        return value

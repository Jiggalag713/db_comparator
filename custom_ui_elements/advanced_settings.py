"""Module intended to store AdvancedSettings class, main class of advanced
settings window"""
import logging

from PyQt5.QtWidgets import QDialog, QComboBox, QPushButton, QLineEdit

from configuration.advanced_ui_config import UIElements
from configuration.default_variables import DefaultValues
from configuration.main_config import set_value
from configuration.system_config import SystemConfig
from ui_logic.advanced_window_logic import AdvancedWindowLogic


class AdvancedSettingsItem(QDialog):
    """Main class of advanced settings window"""
    def __init__(self, configuration):
        super().__init__()
        self.main_ui: UIElements = UIElements()
        self.setLayout(self.main_ui.positions.grid)
        self.default_values: DefaultValues = configuration.variables.default_values
        self.system_config: SystemConfig = configuration.variables.system_config
        self.advanced_logic: AdvancedWindowLogic = AdvancedWindowLogic(self, self.main_ui,
                                                                       configuration)
        self.logger = configuration.variables.system_config.logger
        btn_ok = self.main_ui.buttons.get('btn_ok')
        if isinstance(btn_ok, QPushButton):
            btn_ok.clicked.connect(self.advanced_logic.ok_pressed)
        btn_cancel = self.main_ui.buttons.get('btn_cancel')
        if isinstance(btn_cancel, QPushButton):
            btn_cancel.clicked.connect(self.advanced_logic.cancel_pressed)
        btn_reset = self.main_ui.buttons.get('btn_reset')
        if isinstance(btn_reset, QPushButton):
            btn_reset.clicked.connect(self.advanced_logic.set_default)
        schema_columns = self.main_ui.line_edits.schema_columns
        schema_columns.clicked.connect(self.advanced_logic.set_schema_columns)
        self.advanced_logic.set_default()
        self.setWindowTitle('Advanced settings')
        self.set_connects()

    def set_connects(self) -> None:
        """Sets connections between ui elements and internal class attributes"""
        self.set_line_edit_variables()
        self.set_combo_boxes_variables()

    def set_line_edit_variables(self) -> None:
        """Connects line_edits with appropriate variables in
        internal object"""
        line_edits = self.main_ui.line_edits
        comparing_step = line_edits.comparing_step
        comparing_step.textChanged.connect(lambda: self.validate_int_and_set('comparing_step'))
        depth_report_check = line_edits.depth_report_check
        depth_report_check.textChanged.connect(lambda:
                                               self.validate_int_and_set('depth_report_check'))
        retry_attempts = line_edits.retry_attempts
        retry_attempts.textChanged.connect(lambda: self.validate_int_and_set('retry_attempts'))
        table_timeout = line_edits.table_timeout
        table_timeout.textChanged.connect(lambda: self.validate_int_and_set('table_timeout'))
        strings_amount = line_edits.strings_amount
        strings_amount.textChanged.connect(lambda: self.validate_int_and_set('strings_amount'))
        path_to_logs = line_edits.path_to_logs
        system_config = self.system_config.__dict__
        path_to_logs.textChanged.connect(lambda: set_value(path_to_logs,
                                                           system_config,
                                                           'path_to_logs',
                                                           str))
        schema_columns = line_edits.schema_columns
        default_values = self.default_values.__dict__
        schema_columns.textChanged.connect(lambda: set_value(schema_columns,
                                                             default_values,
                                                             'schema_columns',
                                                             list))

    def set_combo_boxes_variables(self) -> None:
        """Connects combo_boxes with appropriate variables in
        internal object"""
        argument = (self.main_ui.combo_boxes, self.system_config, 'logging_level', self.logger)
        self.main_ui.combo_boxes.currentTextChanged.connect(lambda:
                                                            self.set_combo_boxes_value(*argument))

    @staticmethod
    def set_combo_boxes_value(widget: QComboBox, fields: SystemConfig,
                              key: str, logger: logging.Logger) -> None:
        """Sets combo_boxes value from ui to appropriate variable"""
        text = widget.currentText()
        current_level = logger.level
        if logging.__dict__.get(text) != current_level:
            fields.__dict__.update({key: text})
            logger.setLevel(text)
            logger.info(f'Logging level changed to {text}')

    def validate_int_and_set(self, key):
        """Validates and sets comparing_step"""
        line_edit = self.main_ui.line_edits.__dict__.get(key)
        if isinstance(line_edit, QLineEdit):
            text = line_edit.text()
            try:
                value = int(text)
                self.default_values.constants.update({key: value})
                line_edit.setStyleSheet("color: black;")
                self.main_ui.line_edits.set_tooltip()
            except ValueError as exception:
                self.logger.warn(f'{exception}')
                line_edit.setStyleSheet("color: red;")
                line_edit.setToolTip('Please, input integer number')

"""Module intended for storing Configuration class"""
from dataclasses import dataclass, field
from typing import List

from PyQt5.QtWidgets import QStatusBar

from configuration.sql_variables import SqlVariables
from configuration.system_config import SystemConfig
from configuration.ui_config import UIElements
from configuration.default_variables import DefaultValues


@dataclass
class Configuration:
    """Class intended to make together some different variables
    in purposes throwing of this to different methods"""
    status_bar: QStatusBar
    system_config: SystemConfig
    is_toggled: bool = True
    default_values: DefaultValues = DefaultValues()
    ui_elements: UIElements = field(init=False, repr=True)

    def __post_init__(self):
        self.ui_elements = UIElements(self.is_toggled, self.status_bar)
        self.sql_variables = SqlVariables(self.system_config.logger)
        self.set_connects()

    def set_connects(self):
        """Set connection between ui variables and internal logic variables"""
        self.set_line_edit_variables()
        self.set_check_boxes_variables()
        self.set_radio_buttons_variables()

    def set_line_edit_variables(self) -> None:
        """Connects line_edits with appropriate variables in
        sql_variables/default_variables object"""
        for item in self.prepare_mapping():
            item[0].textChanged.connect(lambda: self.set_value(*item))

    def prepare_mapping(self) -> List:
        """Returns mapping for iteration through in to connect line_edits with
        appropriate variables of appropriate object"""
        result = []
        line_edits = self.ui_elements.line_edits
        for instance_type in ['prod', 'test']:
            for param in ['host', 'user', 'password', 'base']:
                widget = line_edits.__dict__.get(instance_type).__dict__.get(param)
                value_store = self.sql_variables.__dict__.get(instance_type).credentials.__dataclass_fields__
                result.append((widget, value_store, param))
        result.extend([
            (line_edits.send_mail_to, self.default_values.__dict__, 'send_mail_to'),
            (line_edits.included_tables, self.sql_variables.inc_exc.__dict__, 'included_tables'),
            (line_edits.excluded_tables, self.sql_variables.inc_exc.__dict__, 'excluded_tables'),
            (line_edits.excluded_columns, self.sql_variables.inc_exc.__dict__, 'excluded_columns'),
        ])
        return result

    @staticmethod
    def set_value(widget, fields, key) -> None:
        """Sets value from widget to some variable"""
        text = widget.text()
        if ',' in text:
            text = text.split(',')
        if isinstance(fields.get(key), list):
            if not isinstance(text, list):
                text = list(text)
        fields.update({key: text})

    def set_check_boxes_variables(self) -> None:
        """Connects check_boxes with appropriate variables in
        sql_variables/default_variables object"""
        for item in self.prepare_check_boxes_mapping():
            item[0].stateChanged.connect(lambda: self.set_check_box_value(*item))

    def prepare_check_boxes_mapping(self) -> List:
        """Returns mapping for iteration through in to connect check_boxes with
        appropriate variables of appropriate object"""
        result = []
        check_boxes = self.ui_elements.checkboxes
        value_store = self.default_values.checks_customization
        for param in ['check_schema', 'check_reports', 'fail_fast', 'check_entities', 'use_dataframes']:
            result.append((check_boxes.get(param), value_store, param))
        return result

    @staticmethod
    def set_check_box_value(widget, fields, key) -> None:
        """Sets checkbox value from ui to appropriate variable"""
        fields.update({key: widget.isChecked()})

    def set_radio_buttons_variables(self) -> None:
        """Connects radio_buttons with appropriate variables in
        sql_variables/default_variables object"""
        radio_buttons = self.ui_elements.radio_buttons
        for key in ['day_summary_mode', 'section_summary_mode', 'detailed_mode']:
            radio_buttons.get(key).toggled.connect(lambda: self.set_radio_button_value(self.ui_elements.radio_buttons.get(key),
                                                                                       self.default_values.__dict__,
                                                                                       key))

    @staticmethod
    def set_radio_button_value(widget, fields, key) -> None:
        """Sets checkbox value from ui to appropriate variable"""
        if widget.isChecked():
            fields.update({fields.get('mode'): key})

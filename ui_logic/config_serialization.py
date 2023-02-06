"""Module contains class implemented serialization of application configuration"""
import json
import os
import logging
from typing import Dict, Any

from PyQt5.QtWidgets import QFileDialog

from configuration.main_config import Configuration
from configuration.system_config import SystemConfig
from helpers.sql_helper import SqlAlchemyHelper
from ui_logic.buttons import ButtonsLogic
from ui_logic.common import set_ui_value


class ConfigSerialization:
    """Class implemented serialization of application configuration"""
    def __init__(self, common: ButtonsLogic, configuration: Configuration):
        self.common: ButtonsLogic = common
        self.configuration: Configuration = configuration
        self.system_config = configuration.system_config
        self.default_values = configuration.default_values
        self.sql_variables = configuration.sql_variables
        self.main_ui = configuration.ui_elements
        self.logger: logging.Logger = self.configuration.system_config.logger

    def save_configuration(self) -> None:
        """Method implements serialization of current application configuration
        to file"""
        config = {}
        line_edits = self.configuration.ui_elements.line_edits
        for key in self.sql_variables.__dict__:
            if key in ['prod', 'test']:
                config.update(self.host_properties_to_json(key,
                                                           self.sql_variables.__dict__.get(key)))
        for key in self.sql_variables.inc_exc.__dict__:
            if key in ['included_tables', 'excluded_tables', 'excluded_columns']:
                value = line_edits.__dict__.get(key).text().split(',')
                if '' in value:
                    value.remove('')
                config.update({key: value})
        config.update(self.variables_to_json())
        config.update(self.serialize_check_customization_state())
        self.write_to_file(config)

    def write_to_file(self, data) -> None:
        """Writes properties, converted to json, to file"""
        file_name, _ = QFileDialog.getSaveFileName(QFileDialog(),
                                                   "QFileDialog.getSaveFileName()",  "",
                                                   "All Files (*);;Text Files (*.txt)")
        if file_name:
            with open(file_name, 'w', encoding="utf-8") as file:
                json.dump(data, file, indent=4)
            self.logger.info(f'Configuration successfully saved to {file_name}')

    def serialize_check_customization_state(self) -> Dict:
        """Method intended for state serialization of main window check_boxes"""
        checkboxes = self.main_ui.checkboxes
        radio_buttons = self.main_ui.radio_buttons
        return {
            'check_entities': checkboxes.get('check_entities').isChecked(),
            'check_reports': checkboxes.get('check_reports').isChecked(),
            'check_schema': checkboxes.get('check_schema').isChecked(),
            'fail_fast': checkboxes.get('fail_fast').isChecked(),
            'use_dataframes': checkboxes.get('use_dataframes').isChecked(),
            'report_check_type': self.get_check_type(radio_buttons)
        }

    @staticmethod
    def get_check_type(radio_buttons: Dict) -> str:
        """Method intended for getting type of report check"""
        if radio_buttons.get('day_summary').isChecked():
            return 'day-sum'
        if radio_buttons.get('detailed').isChecked():
            return 'section-sum'
        return 'detailed'

    @staticmethod
    def host_properties_to_json(instance_type: str, instance: SqlAlchemyHelper) -> Dict:
        """Method intended for serializing part of SqlAlchemyHelper instance
        to config file"""
        return {
            f'{instance_type}.host': instance.credentials.host,
            f'{instance_type}.user': instance.credentials.user,
            f'{instance_type}.password': instance.credentials.password,
            f'{instance_type}.db': instance.credentials.base
        }

    @staticmethod
    def system_variables_to_json(system_config: SystemConfig) -> Dict:
        """Method intended to serialization system variables to config file"""
        return {
            'logging_level': system_config.logging_level,
            'path_to_logs': system_config.path_to_logs,
            'service_dir': system_config.service_dir,
            'test_dir': system_config.test_dir
        }

    def variables_to_json(self) -> Dict:
        """Method intended to serialization of all other variables to config file"""
        system_config = self.configuration.__dict__.get('system_config')
        property_dict = self.system_variables_to_json(system_config)
        property_dict.update({
            'comparing_step': self.default_values.constants.get('comparing_step'),
            'depth_report_check': self.default_values.constants.get('depth_report_check'),
            'retry_attempts': self.default_values.constants.get('retry_attempts'),
            'strings_amount': self.default_values.constants.get('strings_amount'),
            'table_timeout': self.default_values.constants.get('table_timeout'),
            'schema_columns': self.default_values.schema_columns
        })
        return property_dict

    @staticmethod
    def get_value(value: Any) -> str:
        """Method intended to cast value to str type"""
        if isinstance(value, list):
            return ','.join(value)
        return value

    def load_configuration(self) -> None:
        """Method loads application configuration from file"""
        file_name = QFileDialog.getOpenFileName(QFileDialog(), 'Open file',
                                                f'{os.getcwd()}/resources/properties/')[0]
        try:
            with open(file_name, 'r', encoding="utf-8") as file:
                data = file.read()
                self.deserialize_config(json.loads(data))
                self.logger.debug(f'Configuration from file {file_name} successfully loaded...')
        except FileNotFoundError as err:
            self.logger.warning(f'File not found, or, probably, '
                                f'you just pressed cancel. Warn: {err.args[1]}')

    def deserialize_config(self, config: json) -> None:
        """Loads variables from config to UI variables"""
        for key in config:
            value = self.get_value(config.get(key))
            if value:
                lineedit_mapping = {
                    'prod.host': self.main_ui.line_edits.prod.host,
                    'prod.user': self.main_ui.line_edits.prod.user,
                    'prod.password': self.main_ui.line_edits.prod.password,
                    'prod.db': [self.main_ui.labels.prod.base,
                                self.main_ui.line_edits.prod.base],
                    'test.host': self.main_ui.line_edits.test.host,
                    'test.user': self.main_ui.line_edits.test.user,
                    'test.password': self.main_ui.line_edits.test.password,
                    'test.db': [self.main_ui.labels.test.base,
                                self.main_ui.line_edits.test.base],
                    'included_tables': self.main_ui.line_edits.included_tables,
                    'excluded_tables': self.main_ui.line_edits.excluded_tables,
                    'send_mail_to': self.main_ui.line_edits.send_mail_to,
                    'excluded_columns': self.main_ui.line_edits.excluded_columns
                }
                checkbox_mapping = {
                    'check_schema': self.main_ui.checkboxes.get('check_schema'),
                    'fail_fast': self.main_ui.checkboxes.get('fail_fast'),
                    'check_reports': self.main_ui.checkboxes.get('check_reports'),
                    'check_entities': self.main_ui.checkboxes.get('check_entities')
                }
                values = [
                    'comparing_step',
                    'depth_report_check',
                    'retry_attempts',
                    'path_to_logs',
                    'table_timeout'
                ]
                if key in lineedit_mapping:
                    if '.db' in key:
                        for item in lineedit_mapping.get(key):
                            item.show()
                        set_ui_value(lineedit_mapping.get(key)[1], value)
                    else:
                        set_ui_value(lineedit_mapping.get(key), value)
                elif key in checkbox_mapping:
                    checkbox_mapping.get(key).setChecked(value)
                elif key in values:
                    self.default_values.constants.update({key: value})
                elif key == 'logging_level':
                    self.system_config.logging_level = value
                    self.logger.setLevel(value)
                elif 'schema_columns' in key:
                    self.default_values.schema_columns = value.split(',')
                elif 'mode' in key:
                    self.load_radio_buttons_state(self.main_ui.radio_buttons, value)
        self.common.check_prod_host()
        self.common.check_test_host()

    @staticmethod
    def load_radio_buttons_state(radio_buttons, mode) -> None:
        """Method loads state of radio buttons"""
        states = {
            'day-sum': [True, False, False],
            'section-sum': [False, True, False],
            'detailed': [False, False, True]
        }
        actual_state = states.get(mode)
        radio_buttons.get('day_summary').setChecked(actual_state[0])
        radio_buttons.get('section_summary').setChecked(actual_state[1])
        radio_buttons.get('detailed').setChecked(actual_state[2])

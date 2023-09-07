"""Module contains class intended for storing default variables"""
from typing import List


class DefaultValues:
    """Class intended for storing default variables"""
    def __init__(self):
        self.checks_customization = {'check_schema': True,
                                     'fail_fast': False,
                                     'check_reports': True,
                                     'check_entities': True,
                                     'report_check_type': 'detailed'}
        self.constants = {
            'comparing_step': 10000,
            'depth_report_check': 7,
            'retry_attempts': 5,
            'table_timeout': 5,
            'strings_amount': 1000
        }
        self.send_mail_to = ''
        self.schema_columns: List[str] = []
        self.mode = 'detailed'
        self.selected_schema_columns: List[str] = ['TABLE_CATALOG',
                                                   'TABLE_NAME',
                                                   'COLUMN_NAME',
                                                   'ORDINAL_POSITION',
                                                   'COLUMN_DEFAULT',
                                                   'IS_NULLABLE',
                                                   'DATA_TYPE',
                                                   'CHARACTER_MAXIMUM_LENGTH',
                                                   'CHARACTER_OCTET_LENGTH',
                                                   'NUMERIC_PRECISION',
                                                   'NUMERIC_SCALE',
                                                   'DATETIME_PRECISION',
                                                   'CHARACTER_SET_NAME',
                                                   'COLLATION_NAME',
                                                   'COLUMN_TYPE',
                                                   'COLUMN_KEY',
                                                   'EXTRA',
                                                   'COLUMN_COMMENT',
                                                   'GENERATION_EXPRESSION']

    def set_default_values(self, checkboxes, radio_buttons) -> None:
        """Method sets default values to some UI elements on main window."""
        self.check_boxes_default_values(checkboxes)
        self.radio_buttons_default_values(radio_buttons)

    def check_boxes_default_values(self, checkboxes) -> None:
        """Method sets default values for check_boxes"""
        checkboxes.get('check_schema').setChecked(self.checks_customization.get('check_schema'))
        checkboxes.get('fail_fast').setChecked(self.checks_customization.get('fail_fast'))
        checkboxes.get('check_reports').setChecked(self.checks_customization.get('check_reports'))
        checkboxes.get('check_entities').setChecked(self.checks_customization.get('check_entities'))

    @staticmethod
    def radio_buttons_default_values(radio_buttons) -> None:
        """Method sets default values for radio_buttons"""
        radio_buttons.get('day-sum').setChecked(True)
        radio_buttons.get('section-sum').setChecked(False)
        radio_buttons.get('detailed').setChecked(False)

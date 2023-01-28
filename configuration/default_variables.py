"""Module contains class intended for storing default variables"""
from typing import List
from configuration.system_config import SystemConfig


class DefaultValues:
    """Class intended for storing default variables"""
    def __init__(self):
        self.system_config: SystemConfig = SystemConfig()
        self.checks_customization = {'check_schema': True,
                                     'fail_fast': False,
                                     'check_reports': True,
                                     'check_entities': True,
                                     'use_dataframes': True,
                                     'report_check_type': 'detailed'}
        self.default_excluded_tables: List[str] = ['databasechangelog',
                                                   'download',
                                                   'migrationhistory',
                                                   'mntapplog',
                                                   'reportinfo',
                                                   'synchistory',
                                                   'syncstage',
                                                   'synctrace',
                                                   'synctracelink',
                                                   'syncpersistentjob',
                                                   'forecaststatistics',
                                                   'migrationhistory']
        self.default_excluded_columns: List[str] = ['archived',
                                                    'addonFields',
                                                    'hourOfDayS',
                                                    'dayOfWeekS',
                                                    'impCost',
                                                    'id']
        self.comparing_step: int = 10000
        self.depth_report_check: int = 7
        self.retry_attempts: int = 5
        self.table_timeout: int = 5
        self.strings_amount: int = 1000
        self.schema_columns: List[str] = []
        # self.schema_columns: List[str] = ['TABLE_CATALOG',
        #                                   'TABLE_NAME',
        #                                   'COLUMN_NAME',
        #                                   'ORDINAL_POSITION',
        #                                   'COLUMN_DEFAULT',
        #                                   'IS_NULLABLE',
        #                                   'DATA_TYPE',
        #                                   'CHARACTER_MAXIMUM_LENGTH',
        #                                   'CHARACTER_OCTET_LENGTH',
        #                                   'NUMERIC_PRECISION',
        #                                   'NUMERIC_SCALE',
        #                                   'DATETIME_PRECISION',
        #                                   'CHARACTER_SET_NAME',
        #                                   'COLLATION_NAME',
        #                                   'COLUMN_TYPE',
        #                                   'COLUMN_KEY',
        #                                   'EXTRA',
        #                                   'COLUMN_COMMENT',
        #                                   'GENERATION_EXPRESSION']

    def set_default_values(self, line_edits, checkboxes, radio_buttons) -> None:
        """Method sets default values to some UI elements on main window."""
        line_edits.excluded_tables.setText(','.join(self.default_excluded_tables))
        line_edits.excluded_tables.setCursorPosition(0)
        line_edits.excluded_columns.setText(','.join(self.default_excluded_columns))
        line_edits.excluded_columns.setCursorPosition(0)
        checkboxes.get('check_schema').setChecked(self.checks_customization.get('check_schema'))
        checkboxes.get('fail_fast').setChecked(self.checks_customization.get('fail_fast'))
        checkboxes.get('check_reports').setChecked(self.checks_customization.get('check_reports'))
        checkboxes.get('check_entities').setChecked(self.checks_customization.get('check_entities'))
        checkboxes.get('use_dataframes').setChecked(self.checks_customization.get('use_dataframes'))
        radio_buttons.day_summary_mode.setChecked(True)
        radio_buttons.section_summary_mode.setChecked(False)
        radio_buttons.detailed_mode.setChecked(False)

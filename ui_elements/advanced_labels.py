"""Module intended for storing Labels class, which contains labels
from advanced settings window"""
from typing import Dict

from PyQt5.QtWidgets import QLabel


class Labels:
    """Class, which contains labels
    from advanced settings window"""
    def __init__(self):
        self.text_labels: Dict[str, QLabel] = {
            'logging_level_label': QLabel('Logging level'),
            'schema_columns_label': QLabel('Schema columns'),
            'path_to_logs_label': QLabel('Path to logs')
        }
        self.number_labels: Dict[str, QLabel] = {
            'comparing_step_label': QLabel('Comparing step'),
            'depth_report_check_label': QLabel('Days in past'),
            'retry_attempts_label': QLabel('Retry attempts'),
            'table_timeout_label': QLabel('Timeout for single table, min'),
            'strings_amount_label': QLabel('Amount of stored uniq strings')
        }

    def set_text_labels_tooltips(self) -> None:
        """Method sets tooltips to text labels on advanced setting window"""
        if self.text_labels.get('logging_level_label') is not None:
            logging_level_label = self.text_labels.get('logging_level_label')
            logging_level_label.setToolTip('Messages with this label and higher '
                                           'will be written to logs')
        schema_columns_label = self.text_labels.get('schema_columns_label')
        schema_columns_label.setToolTip('List of columns, which should be compared '
                                        'during schema comparing\n' +
                                        'Do not touch this value if you not sure!')
        path_to_logs_label = self.text_labels.get('path_to_logs_label')
        path_to_logs_label.setToolTip('Path, where log file should be created')

    def set_number_labels_tooltips(self) -> None:
        """Method sets tooltips to number labels on advanced setting window"""
        comparing_step_label = self.number_labels.get('comparing_step_label')
        comparing_step_label.setToolTip('Max amount of records which should be '
                                        'requested in single sql-query\n'
                                        'Do not touch this value if you not sure!')
        depth_report_check_label = self.number_labels.get('depth_report_check_label')
        depth_report_check_label.setToolTip('Amount of days in past, which should '
                                            'be compared in case of report tables')
        retry_attempts_label = self.number_labels.get('retry_attempts_label')
        retry_attempts_label.setToolTip('Amount of attempts for reconnecting to dbs in '
                                        'case of connection lost error')
        table_timeout_label = self.number_labels.get('table_timeout_label')
        table_timeout_label.setToolTip('Timeout in minutes for checking any single table')
        strings_amount_label = self.number_labels.get('strings_amount_label')
        strings_amount_label.setToolTip('Maximum amount of uniques for single table.\n'
                                        'When amount of uniques exceeds this threshold, '
                                        'checking of this table\n will be interrupted, '
                                        'and uniques will be stored in file in \n'
                                        '/tmp/comparator directory')

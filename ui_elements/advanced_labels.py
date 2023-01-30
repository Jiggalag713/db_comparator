"""Module intended for storing Labels class, which contains labels
from advanced settings window"""
from PyQt5.QtWidgets import QLabel


class Labels:
    """Class, which contains labels
    from advanced settings window"""
    def __init__(self):
        self.logging_level_label = QLabel('Logging level')
        self.comparing_step_label = QLabel('Comparing step')
        self.depth_report_check_label = QLabel('Days in past')
        self.schema_columns_label = QLabel('Schema columns')
        self.retry_attempts_label = QLabel('Retry attempts')
        self.path_to_logs_label = QLabel('Path to logs')
        self.table_timeout_label = QLabel('Timeout for single table, min')
        self.strings_amount_label = QLabel('Amount of stored uniq strings')
        self.set_tooltips()

    def set_tooltips(self) -> None:
        """Method sets tooltips to labels on advanced setting window"""
        self.logging_level_label.setToolTip('Messages with this label and higher '
                                            'will be written to logs')
        self.comparing_step_label.setToolTip('Max amount of records which should be '
                                             'requested in single sql-query\n'
                                             'Do not touch this value if you not sure!')
        self.depth_report_check_label.setToolTip('Amount of days in past, which should '
                                                 'be compared in case of report tables')
        self.schema_columns_label.setToolTip('List of columns, which should be compared '
                                             'during schema comparing\n' +
                                             'Do not touch this value if you not sure!')
        self.retry_attempts_label.setToolTip('Amount of attempts for reconnecting to dbs in '
                                             'case of connection lost error')
        self.path_to_logs_label.setToolTip('Path, where log file should be created')
        self.table_timeout_label.setToolTip('Timeout in minutes for checking any single table')
        self.strings_amount_label.setToolTip('Maximum amount of uniques for single table.\n'
                                             'When amount of uniques exceeds this threshold, '
                                             'checking of this table\n will be interrupted, '
                                             'and uniques will be stored in file in \n'
                                             '/tmp/comparator directory')

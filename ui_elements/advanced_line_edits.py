"""Module intended to store of LineEdits class for advanced settings window"""
from PyQt5.QtWidgets import QLineEdit


class LineEdits:
    """Class stored line edits for advanced settings window"""
    def __init__(self):
        self.comparing_step: QLineEdit = QLineEdit()
        self.depth_report_check: QLineEdit = QLineEdit()
        self.schema_columns: QLineEdit = QLineEdit()
        self.retry_attempts: QLineEdit = QLineEdit()
        self.path_to_logs: QLineEdit = QLineEdit()
        self.table_timeout: QLineEdit = QLineEdit()
        self.strings_amount: QLineEdit = QLineEdit()

        # set tooltips
    def set_tooltip(self) -> None:
        """Methods sets tooltips to line edits on advanced settings window"""
        self.comparing_step.setToolTip('How much records should be compared in one iteration.\n'
                                       'Parameter may affects performance.')
        self.depth_report_check.setToolTip('How many days in past will be compared in case of \n'
                                           'comparing reports')
        self.schema_columns.setToolTip('Columns, which will be compared during schema comparing')
        self.retry_attempts.setToolTip('Retry attempts in case of some errors.')
        self.path_to_logs.setToolTip('Where comparator logs will be stored')
        self.table_timeout.setToolTip('Stop comparing table if time of comparing '
                                      'more than this timeout')
        self.strings_amount.setToolTip('If amount of different records more than this '
                                       'threshold, another unique \n records will not '
                                       'be stored in result file')

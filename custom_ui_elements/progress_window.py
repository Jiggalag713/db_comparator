"""Module intended to store progress window class"""
import logging

from PyQt5.QtWidgets import QDialog, QProgressBar, QGridLayout, QLabel, QPushButton
from configuration.sql_variables import SqlVariables
from configuration.variables import Variables
from logic.start_comparing import start


class ProgressWindow(QDialog):
    """Class contained implementation of progress window"""
    def __init__(self, variables: Variables, check_schema: bool):
        super().__init__()
        self.setGeometry(50, 50, 500, 300)
        grid: QGridLayout = QGridLayout()
        grid.setSpacing(5)
        self.setLayout(grid)
        self.sql_variables: SqlVariables = variables.sql_variables
        self.progress_schema: QProgressBar = QProgressBar(self)
        self.progress_data: QProgressBar = QProgressBar(self)
        self.schema_label: QLabel = QLabel()
        self.data_label: QLabel = QLabel()
        self.result_label: QLabel = QLabel()
        btn_ok: QPushButton = QPushButton('OK')
        if isinstance(btn_ok, QPushButton):
            btn_ok.clicked.connect(self.ok_pressed)
        self.logger: logging.Logger = variables.sql_variables.logger
        schema_checking: QLabel = QLabel('Schema checking')
        data_checking: QLabel = QLabel('Data checking')
        grid.addWidget(schema_checking, 0, 0, 1, 1)
        grid.addWidget(self.progress_schema, 0, 1, 1, 1)
        grid.addWidget(self.schema_label, 1, 0, 1, 2)
        grid.addWidget(data_checking, 2, 0, 1, 1)
        grid.addWidget(self.progress_data, 2, 1, 1, 1)
        grid.addWidget(self.data_label, 3, 0, 1, 2)
        grid.addWidget(self.result_label, 4, 0, 1, 2)
        grid.addWidget(btn_ok, 5, 1, 1, 2)
        self.visible_schema_progress_bar(check_schema, schema_checking)
        self.show()
        start(variables, progress_window=self)

    def visible_schema_progress_bar(self, check_schema, schema_checking) -> None:
        """Make visible schema label and progress bar"""
        if not check_schema:
            schema_checking.setVisible(False)
            self.progress_schema.setVisible(False)
            self.schema_label.setVisible(False)

    def ok_pressed(self):
        """Method closes progress window by pressing button"""
        self.close()

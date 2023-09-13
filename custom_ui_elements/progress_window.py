"""Module intended to store progress window class"""
import datetime
import logging
from typing import List

from PyQt5.QtWidgets import QDialog, QProgressBar, QGridLayout, QLabel, QApplication, QPushButton
from configuration.sql_variables import SqlVariables


class ProgressWindow(QDialog):
    """Class contained implementation of progress window"""
    def __init__(self, sql_variables: SqlVariables, check_schema: bool,
                 schema_columns: List[str], result_file):
        super().__init__()
        self.setGeometry(50, 50, 500, 300)
        grid: QGridLayout = QGridLayout()
        grid.setSpacing(5)
        self.setLayout(grid)
        self.sql_variables: SqlVariables = sql_variables
        self.progress_schema: QProgressBar = QProgressBar(self)
        self.progress_data: QProgressBar = QProgressBar(self)
        self.schema_label: QLabel = QLabel()
        self.data_label: QLabel = QLabel()
        btn_ok: QPushButton = QPushButton('OK')
        if isinstance(btn_ok, QPushButton):
            btn_ok.clicked.connect(self.ok_pressed)
        self.logger: logging.Logger = sql_variables.logger
        self.result_file = result_file
        schema_checking: QLabel = QLabel('Schema checking')
        data_checking: QLabel = QLabel('Data checking')
        grid.addWidget(schema_checking, 0, 0, 1, 1)
        grid.addWidget(self.progress_schema, 0, 1, 1, 1)
        grid.addWidget(self.schema_label, 1, 0, 1, 2)
        grid.addWidget(data_checking, 2, 0, 1, 1)
        grid.addWidget(self.progress_data, 2, 1, 1, 1)
        grid.addWidget(self.data_label, 3, 0, 1, 2)
        grid.addWidget(btn_ok, 4, 1, 1, 2)
        self.visible_schema_progress_bar(check_schema, schema_checking)
        self.show()
        self.start(self.sql_variables.tables.get_compare(), check_schema, schema_columns)

    def start(self, tables, check_schema, schema_columns) -> None:
        """Method implements changing of progress on progress window"""
        part = 100 // len(tables)
        if check_schema:
            start_time = datetime.datetime.now()
            self.setWindowTitle("Comparing metadata...")
            for table in tables:
                completed = part * (tables.index(table) + 1)
                if tables.index(table) + 1 == len(tables):
                    completed = 100
                self.progress_schema.setValue(completed)
                self.schema_label.setText(f'Processing of {table} table...')
                result = self.sql_variables.compare_table_metadata(table, schema_columns,
                                                                   self.result_file)
                print(result)
                QApplication.processEvents()
            comparing_time = datetime.datetime.now() - start_time
            self.logger.info(f'Comparing of schemas finished in {comparing_time}')
            self.schema_label.setText(f'Schemas successfully compared in {comparing_time}...')
        else:
            self.logger.info("Schema checking disabled...")
        self.setWindowTitle("Comparing data...")
        start_time = datetime.datetime.now()
        for table in tables:
            completed = part * (tables.index(table) + 1)
            if tables.index(table) + 1 == len(tables):
                completed = 100
            self.progress_data.setValue(completed)
            self.data_label.setText(f'Processing of {table} table...')
            self.sql_variables.compare_data(table)
            QApplication.processEvents()
        data_comparing_time = datetime.datetime.now() - start_time
        self.logger.info(f'Data compared in {data_comparing_time}')
        self.data_label.setText(f'Data successfully compared in {data_comparing_time}...')

    def visible_schema_progress_bar(self, check_schema, schema_checking) -> None:
        """Make visible schema label and progress bar"""
        if not check_schema:
            schema_checking.setVisible(False)
            self.progress_schema.setVisible(False)
            self.schema_label.setVisible(False)

    def ok_pressed(self):
        """Method closes progress window by pressing button"""
        self.close()

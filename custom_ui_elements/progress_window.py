"""Module intended to store progress window class"""
import datetime
import logging
from typing import List

from PyQt5.QtWidgets import QDialog, QProgressBar, QGridLayout, QLabel, QApplication
from configuration.main_config import Configuration


class ProgressWindow(QDialog):
    """Class contained implementation of progress window"""
    def __init__(self, configuration: Configuration, dataframes_enabled: bool):
        super().__init__()
        self.setGeometry(50, 50, 500, 300)
        grid: QGridLayout = QGridLayout()
        grid.setSpacing(5)
        self.setLayout(grid)
        self.configuration: Configuration = configuration
        self.progress_schema: QProgressBar = QProgressBar(self)
        self.progress_data: QProgressBar = QProgressBar(self)
        self.schema_label: QLabel = QLabel()
        self.data_label: QLabel = QLabel()
        self.logger: logging.Logger = configuration.variables.system_config.logger
        check_schema = self.configuration.ui_elements.checkboxes.get('check_schema')
        schema_checking: QLabel = QLabel('Schema checking')
        data_checking: QLabel = QLabel('Data checking')
        grid.addWidget(schema_checking, 0, 0, 1, 1)
        grid.addWidget(self.progress_schema, 0, 1, 1, 1)
        grid.addWidget(self.schema_label, 1, 0, 1, 2)
        grid.addWidget(data_checking, 2, 0, 1, 1)
        grid.addWidget(self.progress_data, 2, 1, 1, 1)
        grid.addWidget(self.data_label, 3, 0, 1, 2)
        self.visible_schema_progress_bar(check_schema, schema_checking)
        self.show()
        self.start(check_schema, dataframes_enabled)

    def start(self, check_schema, dataframes_enabled) -> None:
        """Method implements changing of progress on progress window"""
        start_time = datetime.datetime.now()
        tables = self.get_table_list()
        sql_variables = self.configuration.variables.sql_variables
        part = 100 // len(tables)
        if check_schema.isChecked():
            self.setWindowTitle("Comparing metadata...")
            schema_start_time = datetime.datetime.now()
            for table in tables:
                completed = part * (tables.index(table) + 1)

                self.progress_schema.setValue(completed)
                self.schema_label.setText(f'Processing of {table} table...')
                if dataframes_enabled:
                    result = sql_variables.compare_table_metadata(table)
                    print(result)
                else:
                    result = sql_variables.compare_table_metadata(table)
                    print(result)
                QApplication.processEvents()
            comparing_time = datetime.datetime.now() - schema_start_time
            self.logger.info(f'Comparing of schemas finished in {comparing_time}')
            self.schema_label.setText('Schemas successfully compared...')
        else:
            self.logger.info("Schema checking disabled...")
        self.setWindowTitle("Comparing data...")
        schema_checking_time = datetime.datetime.now() - start_time
        for table in tables:
            completed = part * (tables.index(table) + 1)
            self.progress_data.setValue(completed)
            self.data_label.setText(f'Processing of {table} table...')
            # is_report = tables.get(table).get('is_report')
            if dataframes_enabled:
                sql_variables.compare_data(table)
            else:
                sql_variables.compare_data(table)
            QApplication.processEvents()
        self.data_label.setText('Data successfully compared...')
        data_comparing_time = datetime.datetime.now() - schema_checking_time
        self.logger.info(f'Data compared in {data_comparing_time}')

    def get_table_list(self) -> List:
        """Calculates final list of tables, which will be compared"""
        sql_variables = self.configuration.variables.sql_variables
        if sql_variables.tables.included:
            return list(sql_variables.tables.included.keys())
        if sql_variables.tables.excluded:
            tables: List = []
            for table in sql_variables.tables.all:
                if table not in sql_variables.tables.excluded:
                    tables.append(table)
            return tables
        return list(sql_variables.tables.all.keys())

    def visible_schema_progress_bar(self, check_schema, schema_checking) -> None:
        """Make visible schema label and progress bar"""
        if not check_schema.isChecked():
            schema_checking.setVisible(False)
            self.progress_schema.setVisible(False)
            self.schema_label.setVisible(False)

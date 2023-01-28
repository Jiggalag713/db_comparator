"""Module intended to store progress window class"""
import datetime
import logging
from typing import Dict

from PyQt5.QtWidgets import QDialog, QProgressBar, QGridLayout, QLabel, QApplication
from configuration.main_config import Configuration
from helpers.sql_helper import SqlAlchemyHelper


class ProgressWindow(QDialog):
    """Class contained implementation of progress window"""
    def __init__(self, configuration: Configuration, dataframes_enabled: bool):
        super(ProgressWindow, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        grid: QGridLayout = QGridLayout()
        grid.setSpacing(5)
        self.setLayout(grid)
        self.configuration: Configuration = configuration
        self.prod: SqlAlchemyHelper = self.configuration.sql_variables.prod
        self.test: SqlAlchemyHelper = self.configuration.sql_variables.test
        self.tables: Dict = configuration.sql_variables.included_tables
        self.check_schema: bool = self.configuration.ui_elements.checkboxes.check_schema.isChecked()
        self.progress_schema: QProgressBar = QProgressBar(self)
        self.progress_data: QProgressBar = QProgressBar(self)
        self.schema_label: QLabel = QLabel()
        self.data_label: QLabel = QLabel()
        self.start_time: datetime = datetime.datetime.now()
        self.logger: logging.Logger = configuration.default_values.system_config.logger
        self.dataframes_enabled = dataframes_enabled
        self.completed: int = 0
        schema_checking: QLabel = QLabel('Schema checking')
        data_checking: QLabel = QLabel('Data checking')
        grid.addWidget(schema_checking, 0, 0, 1, 1)
        grid.addWidget(self.progress_schema, 0, 1, 1, 1)
        grid.addWidget(self.schema_label, 1, 0, 1, 2)
        grid.addWidget(data_checking, 2, 0, 1, 1)
        grid.addWidget(self.progress_data, 2, 1, 1, 1)
        grid.addWidget(self.data_label, 3, 0, 1, 2)
        if not self.configuration.ui_elements.checkboxes.check_schema.isChecked():
            schema_checking.setVisible(False)
            self.progress_schema.setVisible(False)
            self.schema_label.setVisible(False)
        self.show()
        self.start()

    def start(self) -> None:
        """Method implements changing of progress on progress window"""
        part = 100 // len(self.tables)
        if self.check_schema:
            self.setWindowTitle("Comparing metadata...")
            schema_start_time = datetime.datetime.now()
            for table in self.tables:
                self.completed = part * (list(self.tables.keys()).index(table) + 1)

                self.progress_schema.setValue(self.completed)
                self.schema_label.setText(f'Processing of {table} table...')
                if self.dataframes_enabled:
                    self.configuration.sql_variables.compare_table_metadata()
                else:
                    self.configuration.sql_variables.compare_table_metadata()
                QApplication.processEvents()
            comparing_time = datetime.datetime.now() - schema_start_time
            self.logger.info(f'Comparing of schemas finished in {comparing_time}')
            self.schema_label.setText('Schemas successfully compared...')
        else:
            self.logger.info("Schema checking disabled...")
        self.setWindowTitle("Comparing data...")
        schema_checking_time = datetime.datetime.now() - self.start_time
        for table in self.tables:
            self.completed = part * (list(self.tables.keys()).index(table) + 1)
            self.progress_data.setValue(self.completed)
            self.data_label.setText(f'Processing of {table} table...')
            # is_report = self.tables.get(table).get('is_report')
            if self.dataframes_enabled:
                service_dir = self.configuration.default_values.system_config.service_dir
                self.configuration.sql_variables.compare_data(service_dir, table)
            else:
                service_dir = self.configuration.default_values.system_config.service_dir
                self.configuration.sql_variables.compare_data(service_dir, table)
            QApplication.processEvents()
        self.data_label.setText('Data successfully compared...')
        data_comparing_time = datetime.datetime.now() - schema_checking_time
        print(data_comparing_time)
        self.logger.info(f'Data compared in {data_comparing_time}')

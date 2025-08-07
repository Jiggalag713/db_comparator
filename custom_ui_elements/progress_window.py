"""Module intended to store progress window class"""
import datetime
import logging

from PyQt5.QtWidgets import QDialog, QProgressBar, QGridLayout, QLabel, QApplication, QPushButton
from configuration.sql_variables import SqlVariables
from configuration.variables import Variables
from helpers.helper import write_to_file
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

    def start(self, variables) -> None:
        """Method implements changing of progress on progress window"""
        tables = variables.sql_variables.tables.get_compare()
        check_schema = variables.default_values.checks_customization.get('check_schema')
        if check_schema:
            metadata_comparing_time = self.check_tables_metadata(variables, tables)
        else:
            metadata_comparing_time = 0
            self.logger.info("Schema checking disabled...")
        data_comparing_time = self.check_tables_data(variables, tables)
        self.logger.info(f"Comparing task finished takes {metadata_comparing_time + data_comparing_time}")

    def check_tables_metadata(self, variables, tables):
        """Method compare table's metadata"""
        schema_start_time = datetime.datetime.now()
        self.setWindowTitle("Comparing metadata...")
        for table in tables:
            self.check_table_metadata(table, tables, variables)
        schema_comparing_time = datetime.datetime.now() - schema_start_time
        self.logger.info(f'Comparing of schemas finished in {schema_comparing_time}')
        self.schema_label.setText(f'Schemas successfully compared in {schema_comparing_time}...')
        return schema_comparing_time

    def check_table_metadata(self, table, tables, variables):
        """Method compare metadata of one table"""
        schema_columns = variables.default_values.selected_schema_columns
        result = variables.sql_variables.compare_table_metadata(table, schema_columns)
        metadata_dir = variables.system_config.metadata_dir
        write_to_file(result, table, metadata_dir, self.logger)
        completed = (100 // len(tables)) * (tables.index(table) + 1)
        if tables.index(table) + 1 == len(tables):
            completed = 100
        self.progress_schema.setValue(completed)
        self.schema_label.setText(f'Processing of {table} table...')
        result = self.sql_variables.compare_table_metadata(table, schema_columns)
        if write_to_file(result, table, metadata_dir, self.logger):
            self.result_label.setOpenExternalLinks(True)
            link = f'<a href={metadata_dir}{table}.html>{metadata_dir}{table}.html</a>'
            self.result_label.setText(f' Result of comparing wrote to {link}')
        QApplication.processEvents()
        self.logger.info(f'Checked table {table}, {completed}% of total tables')

    def check_tables_data(self, variables, tables):
        data_start_time = datetime.datetime.now()
        self.setWindowTitle("Comparing data...")
        for table in tables:
            self.check_table_data(table, tables, variables)
        data_comparing_time = datetime.datetime.now() - data_start_time
        self.logger.info(f'Data compared in {data_comparing_time}')
        self.data_label.setText(f'Data successfully compared in {data_comparing_time}...')
        return data_comparing_time

    def check_table_data(self, table, tables, variables):
        result = self.sql_variables.compare_data(table)
        data_dir = variables.system_config.data_dir
        write_to_file(result, table, data_dir, self.logger)
        completed = (100 // len(tables)) * (tables.index(table) + 1)
        if tables.index(table) + 1 == len(tables):
            completed = 100
        self.progress_data.setValue(completed)
        self.data_label.setText(f'Processing of {table} table...')
        result = self.sql_variables.compare_data(table)
        if write_to_file(result, table, data_dir, self.logger):
            self.result_label.setOpenExternalLinks(True)
            link = f'<a href={data_dir}{table}.html>{data_dir}{table}.html</a>'
            self.result_label.setText(f' Result of comparing wrote to {link}')
        QApplication.processEvents()

    def visible_schema_progress_bar(self, check_schema, schema_checking) -> None:
        """Make visible schema label and progress bar"""
        if not check_schema:
            schema_checking.setVisible(False)
            self.progress_schema.setVisible(False)
            self.schema_label.setVisible(False)

    def ok_pressed(self):
        """Method closes progress window by pressing button"""
        self.close()

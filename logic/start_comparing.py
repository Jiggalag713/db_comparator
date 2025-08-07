"""Stores logic for comparing"""
import datetime
import logging

from PyQt5.QtWidgets import QApplication

from helpers.helper import write_to_file


def start(variables, progress_window=None) -> None:
    """Starts headless comparing"""
    logger: logging.Logger = variables.sql_variables.logger
    tables = variables.sql_variables.tables.get_compare()
    check_schema = variables.default_values.checks_customization.get('check_schema')
    if check_schema:
        metadata_comparing_time = check_tables_metadata(variables, tables, progress_window)
    else:
        logger.info("Schema checking disabled...")
        metadata_comparing_time = datetime.timedelta(0)
    data_comparing_time = check_tables_data(variables, tables, progress_window)
    logger.info(f"Comparing task finished takes {metadata_comparing_time + data_comparing_time}")


def check_tables_metadata(variables, tables, progress_window):
    """Method compare table's metadata"""
    schema_start_time = datetime.datetime.now()
    logger: logging.Logger = variables.sql_variables.logger
    if progress_window is not None:
        progress_window.setWindowTitle("Comparing metadata...")
    for table in tables:
        check_table_metadata(table, tables, variables, progress_window)
    schema_comparing_time = datetime.datetime.now() - schema_start_time
    logger.info(f'Comparing of schemas finished in {schema_comparing_time}')
    if progress_window is not None:
        progress_window.schema_label.setText(f'Schemas successfully compared in {schema_comparing_time}...')
    return schema_comparing_time


def check_table_metadata(table, tables, variables, progress_window):
    schema_columns = variables.default_values.selected_schema_columns
    result = variables.sql_variables.compare_table_metadata(table, schema_columns)
    metadata_dir = variables.system_config.directories.metadata_dir
    logger: logging.Logger = variables.sql_variables.logger
    write_to_file(result, table, metadata_dir, logger)
    completed = (100 // len(tables)) * (tables.index(table) + 1)
    if tables.index(table) + 1 == len(tables):
        completed = 100
    if progress_window is not None:
        progress_window.progress_schema.setValue(completed)
        progress_window.schema_label.setText(f'Processing of {table} table...')
    logger.info(f'Checked table {table}, {completed}% of total tables')
    if progress_window is not None:
        if write_to_file(result, table, metadata_dir, logger):
            progress_window.result_label.setOpenExternalLinks(True)
            link = f'<a href={metadata_dir}{table}.html>{metadata_dir}{table}.html</a>'
            progress_window.result_label.setText(f' Result of comparing wrote to {link}')
        QApplication.processEvents()
    logger.info(f'Checked table {table}, {completed}% of total tables')


def check_tables_data(variables, tables, progress_window):
    """Method compares table's data"""
    data_start_time = datetime.datetime.now()
    logger: logging.Logger = variables.sql_variables.logger
    if progress_window is not None:
        progress_window.setWindowTitle("Comparing data...")
    for table in tables:
        check_table_data(table, tables, variables, progress_window)
    data_comparing_time = datetime.datetime.now() - data_start_time
    logger.info(f'Comparing of data finished in {data_comparing_time}')
    if progress_window is not None:
        progress_window.data_label.setText(f'Data successfully compared in {data_comparing_time}...')
    return data_comparing_time


def check_table_data(table, tables, variables, progress_window):
    """Method compares data in one proper table"""
    result = variables.sql_variables.compare_data(table)
    data_dir = variables.system_config.directories.data_dir
    logger: logging.Logger = variables.sql_variables.logger
    write_to_file(result, table, data_dir, logger)
    completed = (100 // len(tables)) * (tables.index(table) + 1)
    if tables.index(table) + 1 == len(tables):
        completed = 100
    if progress_window is not None:
        progress_window.progress_data.setValue(completed)
        progress_window.data_label.setText(f'Processing of {table} table...')
    result = variables.sql_variables.compare_data(table)
    if write_to_file(result, table, data_dir, logger):
        if progress_window is not None:
            progress_window.result_label.setOpenExternalLinks(True)
            link = f'<a href={data_dir}{table}.html>{data_dir}{table}.html</a>'
            progress_window.result_label.setText(f' Result of comparing wrote to {link}')
        QApplication.processEvents()
    logger.info(f'Checked table {table}, {completed}% of total tables')

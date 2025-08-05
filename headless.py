"""Stores logic for headless comparing"""
import argparse
import datetime
import json
import logging

from configuration.variables import Variables
from helpers.helper import write_to_file
from ui_logic import config_serialization
from ui_logic.table_calculation import TableCalculation


def get_args() -> argparse.Namespace:
    """Returns script arguments"""
    parser = argparse.ArgumentParser(description='Console db_comparator')
    parser.add_argument('--config', type=str, help='Path to config (/home/user/Desktop/1.txt)',
                        required=True)
    return parser.parse_args()


def open_file(file_name, sql_variables, logger):
    """Method loads application configuration from file"""
    try:
        with open(file_name, 'r', encoding="utf-8") as file:
            data = file.read()
            config_serialization.deserialize_config(sql_variables,
                                                    json.loads(data))
            logger.debug('Configuration from file %s successfully loaded...', file_name)
    except FileNotFoundError as err:
        logger.warning('File not found, or, probably, you just pressed cancel. '
                       'Warn: %s', err.args[1])


def start(variables) -> None:
    # TODO: method should be refactored
    """Starts headless comparing"""
    start_time = datetime.datetime.now()
    sql_variables = variables.sql_variables
    logger: logging.Logger = variables.sql_variables.logger
    check_schema = variables.default_values.checks_customization.get('check_schema')
    data_dir = variables.system_config.data_dir
    tables = sql_variables.tables.get_compare()
    part = 100 // len(tables)
    if check_schema:
        schema_checking_time = check_tables_metadata(variables, tables, part)
    else:
        logger.info("Schema checking disabled...")
        schema_checking_time = datetime.timedelta(0)
    check_tables_data(variables, tables, part)
    data_comparing_time = datetime.datetime.now() - schema_checking_time
    logger.info(f'Data compared in {data_comparing_time}')


def check_tables_metadata(variables, tables, part):
    """Method compare table's metadata"""
    schema_start_time = datetime.datetime.now()
    sql_variables = variables.sql_variables
    logger: logging.Logger = variables.sql_variables.logger
    schema_columns = common_variables.default_values.selected_schema_columns
    metadata_dir = variables.system_config.metadata_dir
    for table in tables:
        result = sql_variables.compare_table_metadata(table, schema_columns)
        write_to_file(result, table, metadata_dir, logger)
        completed = part * (tables.index(table) + 1)
        if tables.index(table) + 1 == len(tables):
            completed = 100
        logger.info(f'Checked table {table}, {completed}% of total tables')
    comparing_time = datetime.datetime.now() - schema_start_time
    logger.info(f'Comparing of schemas finished in {comparing_time}')
    return comparing_time


def check_tables_data(variables, tables, part):
    """Method compares table's data"""
    for table in tables:
        result = variables.sql_variables.compare_data(table)
        data_dir = variables.system_config.data_dir
        logger: logging.Logger = variables.sql_variables.logger
        write_to_file(result, table, data_dir, logger)
        completed = part * (tables.index(table) + 1)
        if tables.index(table) + 1 == len(tables):
            completed = 100
        logger.info(f'Checked table {table}, {completed}% of total tables')



def update_variables(variables) -> None:
    """Checks connections"""
    if all([variables.sql_variables.prod.tables,
            variables.sql_variables.test.tables]):
        table_calculation = TableCalculation(variables)
        variables.sql_variables.tables.all = table_calculation.calculate_table_list()
        variables.sql_variables.tables.get_compare()
        table_calculation.calculate_includes_excludes()
        hard_excluded = variables.sql_variables.tables.hard_excluded
        common_excluded_tables = variables.sql_variables.tables.excluded.copy()
        common_excluded_tables.update(hard_excluded)


args = get_args()
config_name = args.config
common_variables = Variables()
console_logger = common_variables.system_config.logger
open_file(config_name, common_variables, console_logger)
schema_columns = common_variables.default_values.selected_schema_columns
common_variables.sql_variables.prod.warming_up()
common_variables.sql_variables.test.warming_up()
update_variables(common_variables)
start(common_variables)

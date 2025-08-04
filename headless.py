"""Stores logic for headless comparing"""
import argparse
import datetime
import json

from configuration.variables import Variables
from helpers.helper import write_to_file
from ui_logic import config_serialization
from ui_logic.table_calculation import TableCalculation


def get_args() -> argparse.Namespace:
    """Returns script arguments"""
    parser = argparse.ArgumentParser(description='Console db_comparator')
    parser.add_argument('--config', type=str, help='Path to config (/home/user/Desktop/1.txt)',
                        required=True)
    parser.add_argument('--check_schema', type=bool, help='Check schema if true', default=True)
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


def start(variables, schema, columns, logger) -> None:
    """Starts headless comparing"""
    start_time = datetime.datetime.now()
    sql_variables = variables.sql_variables
    metadata_dir = variables.system_config.metadata_dir
    data_dir = variables.system_config.data_dir
    tables = sql_variables.tables.get_compare()
    part = 100 // len(tables)
    if schema:
        schema_start_time = datetime.datetime.now()
        for table in tables:
            result = sql_variables.compare_table_metadata(table, columns)
            write_to_file(result, table, metadata_dir, logger)
            completed = part * (tables.index(table) + 1)
            if tables.index(table) + 1 == len(tables):
                completed = 100
            logger.info(f'Checked table {table}, {completed}% of total tables')
        comparing_time = datetime.datetime.now() - schema_start_time
        logger.info(f'Comparing of schemas finished in {comparing_time}')
    else:
        logger.info("Schema checking disabled...")
    schema_checking_time = datetime.datetime.now() - start_time
    for table in tables:
        sql_variables.compare_data(table)
        completed = part * (tables.index(table) + 1)
        if tables.index(table) + 1 == len(tables):
            completed = 100
        logger.info(f'Checked table {table}, {completed}% of total tables')
    data_comparing_time = datetime.datetime.now() - schema_checking_time
    logger.info(f'Data compared in {data_comparing_time}')


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
check_schema = args.check_schema
common_variables = Variables()
console_logger = common_variables.system_config.logger
open_file(config_name, common_variables, console_logger)
schema_columns = common_variables.default_values.selected_schema_columns
common_variables.sql_variables.prod.warming_up()
common_variables.sql_variables.test.warming_up()
update_variables(common_variables)
start(common_variables, check_schema, schema_columns, console_logger)

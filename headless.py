"""Stores logic for headless comparing"""
import argparse
import json

from configuration.variables import Variables
from logic.start_comparing import start
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

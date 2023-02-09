"""Module contains implementation of TableCalculation class, intended
 for calculating table lists"""
from typing import Dict, List

from configuration.main_config import Configuration
from configuration.variables import Variables
from ui_logic.common import set_ui_value


class TableCalculation:
    """Class intended for calculating different table lists"""
    def __init__(self, configuration: Configuration):
        self.configuration: Configuration = configuration
        self.variables: Variables = configuration.variables
        self.logger = configuration.logger

    def calculate_table_list(self) -> None:
        """Method calculates of tables, which exists in both databases"""
        prod = self.variables.sql_variables.prod
        test = self.variables.sql_variables.test
        tables = self.variables.sql_variables.tables.all
        if all([prod.tables, test.tables]):
            prod_tables = set(prod.tables.keys())
            test_tables = set(test.tables.keys())
            self.get_unique_tables(prod_tables, test_tables, self.variables.sql_variables.prod)
            self.get_unique_tables(test_tables, prod_tables, self.variables.sql_variables.test)
            common_tables = list(prod_tables & test_tables)
            tables.extend(common_tables)
            tables.sort()
        return tables

    def get_unique_tables(self, first, second, instance) -> None:
        """Calculates unique tables for first instance"""
        unique = first - second
        if unique:
            host = instance.credentials.host
            base = instance.credentials.base
            self.logger.warning(f'There is some unique tables for {host}:{base} - {", ".join(unique)}'
                                f'excluded from any comparing')

    def calculate_includes_excludes(self, tables) -> None:
        """Calculates included and excluded tables"""
        prod = self.variables.sql_variables.prod
        test = self.variables.sql_variables.test
        # line_edits = self.configuration.ui_elements.line_edits
        if self.variables.sql_variables.tables.included.keys():
            pass
        for table in tables:
            prod_columns = prod.tables.get(table)
            test_columns = test.tables.get(table)
            if prod_columns == test_columns:
                if table not in self.variables.sql_variables.tables.included:
                    self.variables.sql_variables.tables.included.update({table: prod_columns})
            else:
                prod_reason = self.unique_table_columns(table, prod_columns, test_columns, prod.credentials)
                test_reason = self.unique_table_columns(table, test_columns, prod_columns, test.credentials)
                reason = self.get_reason(prod_reason, test_reason)
                self.logger.error(f"There is different columns for table {table}.")
                self.variables.sql_variables.tables.hard_excluded.update({table: reason})
                self.logger.warning(f'Table {table} was added to hard_excluded'
                                    f' tables and excluded from comparing')
                if table in self.variables.sql_variables.tables.included.keys():
                    self.variables.sql_variables.tables.included.pop(table)
        self.calculate_excluded_columns()

    def unique_table_columns(self, table, first, second, credentials) -> str:
        """Returns reason of excluding some table from comparing"""
        unique_columns = set(first) - set(second)
        """Returns unique columns of first table"""
        if unique_columns:
            host = credentials.host
            base = credentials.base
            message = (f"Uniq columns for table {table} on "
                       f"{host}:{base} - {','.join(unique_columns)}")
            self.logger.info(message)
            return message

    @staticmethod
    def get_reason(prod, test) -> str:
        """Returns reason of hard excluding some table"""
        reason = []
        if prod:
            reason.append(prod)
        if test:
            reason.append(test)
        return ','.join(reason)

    def calculate_excluded_columns(self) -> None:
        """Method calculates list of excluded column"""
        line_edits = self.configuration.ui_elements.line_edits
        set_ui_value(line_edits.excluded_tables, line_edits.excluded_tables.text())
        set_ui_value(line_edits.excluded_columns, line_edits.excluded_columns.text())
        for table in self.variables.sql_variables.tables.all:
            if table in self.variables.sql_variables.tables.excluded:
                # TODO: fix this
                columns = self.variables.sql_variables.tables.all
                for column in columns:
                    excluded_columns = self.variables.sql_variables.columns.excluded
                    if column not in excluded_columns:
                        excluded_columns.append(f'{table}.{column}')
        self.variables.sql_variables.columns.excluded.sort()

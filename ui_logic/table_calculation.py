"""Module contains implementation of TableCalculation class, intended
 for calculating table lists"""
from typing import Dict

from configuration.variables import Variables


class TableCalculation:
    """Class intended for calculating different table lists"""
    def __init__(self, variables: Variables):
        self.variables: Variables = variables
        self.logger = variables.logger

    def calculate_table_list(self) -> None:
        """Method calculates of tables, which exists in both databases"""
        prod = self.variables.sql_variables.prod
        test = self.variables.sql_variables.test
        tables = self.variables.sql_variables.tables.all
        if all([prod.tables, test.tables]):
            tables = self.get_common_tables(prod.tables, test.tables)
        return tables

    def get_common_tables(self, prod, test) -> Dict:
        """Returns dictionary of common tables with columns"""
        prod_tables = set(prod.keys())
        test_tables = set(test.keys())
        self.find_unique_tables(prod_tables, test_tables, self.variables.sql_variables.prod)
        self.find_unique_tables(test_tables, prod_tables, self.variables.sql_variables.test)
        common_tables = {}
        for table in list(prod_tables & test_tables):
            common_tables.update({table: prod.get(table)})
        return common_tables

    def find_unique_tables(self, first, second, instance) -> None:
        """Calculates unique tables for first instance"""
        unique = first - second
        if unique:
            host = instance.credentials.host
            base = instance.credentials.base
            self.logger.warning(f'There is some unique tables for {host}:{base} - '
                                f'{", ".join(unique)} excluded from any comparing')

    def calculate_includes_excludes(self) -> None:
        """Calculates included and excluded tables"""
        if not self.variables.sql_variables.tables.included:
            self.fulfill_include_tables()
            self.calculate_excluded_columns()

    def fulfill_include_tables(self) -> None:
        """Fulfills included_tables variable"""
        prod = self.variables.sql_variables.prod
        test = self.variables.sql_variables.test
        tables = self.variables.sql_variables.tables.all
        for table in tables:
            prod_columns = prod.tables.get(table)
            test_columns = test.tables.get(table)
            if prod_columns == test_columns:
                if table not in self.variables.sql_variables.tables.included:
                    self.variables.sql_variables.tables.included.update({table: prod_columns})
            else:
                reason = self.get_hard_excluded_reason(table, prod, test)
                self.variables.sql_variables.tables.hard_excluded.update({table: reason})
                self.logger.warning(f'Table {table} was added to hard_excluded '
                                    f'with reason: {reason}'
                                    f'tables and excluded from comparing')
                if table in self.variables.sql_variables.tables.included.keys():
                    self.variables.sql_variables.tables.included.pop(table)

    def get_hard_excluded_reason(self, table, prod, test) -> str:
        """Returns reason for hard excluding of some table with different columns for same
        named tables in different databases"""
        prod_columns = prod.tables.get(table)
        test_columns = test.tables.get(table)
        prod_reason = self.unique_table_columns(table, prod_columns, test_columns,
                                                prod.credentials)
        test_reason = self.unique_table_columns(table, test_columns, prod_columns,
                                                test.credentials)
        reason = self.get_reason(prod_reason, test_reason)
        self.logger.error(f"There is different columns for table {table}.")
        return reason

    def unique_table_columns(self, table, first, second, credentials) -> str:
        """Returns reason of excluding some table from comparing"""
        unique_columns = set(first) - set(second)
        if unique_columns:
            host = credentials.host
            base = credentials.base
            message = (f"Uniq columns for table {table} on "
                       f"{host}:{base} - {','.join(unique_columns)}")
            self.logger.info(message)
            return message
        return ''

    def get_tables_dict(self, table_list) -> Dict:
        """Returns included tables dict"""
        result = {}
        prod_tables = self.variables.sql_variables.prod.tables
        for table in table_list:
            result.update({table: prod_tables.get(table)})
        return result

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
        for table in self.variables.sql_variables.tables.all:
            if table in self.variables.sql_variables.tables.excluded:
                columns = self.variables.sql_variables.tables.all
                for column in columns:
                    excluded_columns = self.variables.sql_variables.columns.excluded
                    if column not in excluded_columns:
                        excluded_columns.append(f'{table}.{column}')
        self.variables.sql_variables.columns.excluded.sort()

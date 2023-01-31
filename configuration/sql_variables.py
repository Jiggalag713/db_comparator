"""Module contains class with some sql-related data which would
be useful during comparing of databases"""
import datetime
import logging
from typing import List
from dataclasses import dataclass, field
from helpers import df_compare_helper
from helpers.sql_helper import SqlAlchemyHelper, SqlCredentials


class SqlVariables:
    """Class contains some sql-related data which would be useful during comparing of databases"""
    def __init__(self, logger):
        default_connection = SqlCredentials()
        self.prod: SqlAlchemyHelper = SqlAlchemyHelper(default_connection, logger)
        self.test: SqlAlchemyHelper = SqlAlchemyHelper(default_connection, logger)
        self.inc_exc = IncludeExclude()
        self.tables_for_ui: List = []
        self.columns: List = []
        self.logger: logging.Logger = logger

    # TODO: [improve] strongly refactor this
    def compare_table_metadata(self, table) -> bool:
        """Method intended to compare metadata of two tables"""
        start_time = datetime.datetime.now()
        self.logger.info(f"Compare schema for table {table}...")
        if self.is_columns_list_differs(table):
            return False
        else:
            diff_df = df_compare_helper.get_metadata_dataframe_diff(self.prod, self.test,
                                                                    table, self.logger)
        if not diff_df.empty:
            self.logger.error(f"Schema of tables {table} differs!")
        schema_comparing_time = datetime.datetime.now() - start_time
        self.logger.debug(f"Schema of table {table} compared in {schema_comparing_time}")
        return True

    def is_columns_list_differs(self, table) -> bool:
        """Method intended to check if column lists of some table in two
        databases equals"""
        prod_columns = set(self.prod.tables.get(table))
        test_columns = set(self.test.tables.get(table))
        unique_prod = prod_columns - test_columns
        unique_test = test_columns - prod_columns
        if unique_prod:
            self.warn_columns_differs(table, unique_prod)
        if unique_test:
            self.warn_columns_differs(table, unique_test)
        if any([unique_prod, unique_test]):
            return True
        return False

    def warn_columns_differs(self, table, uniques) -> None:
        """Print warning logs about differs columns"""
        host = self.prod.credentials.host
        base = self.prod.credentials.base
        self.logger.warning(f"There is some unique columns in {host / base} "
                            f"table {table}: {','.join(uniques)}")

    def compare_data(self, table: str) -> bool:
        """Method intended to compare data of two tables"""
        start_time = datetime.datetime.now()
        start_table_check_time = datetime.datetime.now()
        self.logger.info(f"Table {table} processing started now...")
        global_break = True
        checking_time = datetime.datetime.now() - start_table_check_time
        self.logger.info(f"Table {table} checked in {checking_time}...")
        if global_break:
            data_comparing_time = datetime.datetime.now() - start_time
            self.logger.warning(f'Global breaking is True. Comparing interrupted. '
                                f'Comparing finished in {data_comparing_time}')
            return False
        data_comparing_time = datetime.datetime.now() - start_time
        self.logger.info(f'Comparing finished in {data_comparing_time}')
        return True


@dataclass
class IncludeExclude:
    """Class intended for included and excluded tables and columns"""
    included_tables: List = field(default_factory=lambda: [])
    excluded_tables: List = field(default_factory=lambda: [])
    excluded_columns: List = field(default_factory=lambda: [])

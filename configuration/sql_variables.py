"""Module contains class with some sql-related data which would
be useful during comparing of databases"""
import datetime
import logging
from typing import List
from helpers import df_compare_helper
from helpers.sql_helper import SqlAlchemyHelper


# TODO: potentially should be merged with table_data.Info
class SqlVariables:
    """Class contains some sql-related data which would be useful during comparing of databases"""
    def __init__(self, logger):
        self.prod: SqlAlchemyHelper = SqlAlchemyHelper('', '', '', '', logger)
        self.test: SqlAlchemyHelper = SqlAlchemyHelper('', '', '', '', logger)
        self.included_tables: List = []
        self.tables_for_ui: List = []
        self.columns: List = []
        self.excluded_tables: List = []
        self.excluded_columns: List = []
        self.logger: logging.Logger = logger

    def compare_table_metadata(self) -> bool:
        """Method intended to compare metadata of two tables"""
        start_time = datetime.datetime.now()
        prod_table = self.prod.tables
        test_table = self.test.tables
        self.logger.info(f"Compare schema for table {prod_table}...")
        if prod_table == test_table:
            pass
        diff_df = df_compare_helper.get_metadata_dataframe_diff(prod_table, test_table,
                                                                self.logger)
        if not diff_df.empty:
            self.logger.error(f"Schema of tables {prod_table} differs!")
            # TODO: [improve] adding serializing to html file on disc
        schema_comparing_time = datetime.datetime.now() - start_time
        self.logger.debug(f"Schema of table {prod_table} compared in {schema_comparing_time}")
        return True

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

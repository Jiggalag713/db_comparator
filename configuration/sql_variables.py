"""Module contains class with some sql-related data which would
be useful during comparing of databases"""
import logging
from datetime import datetime, timezone
from typing import List, Dict
from dataclasses import dataclass, field

import pandas as pd  # type: ignore

from helpers import df_compare_helper
from helpers.sql_helper import SqlAlchemyHelper, SqlCredentials


class SqlVariables:
    """Class contains some sql-related data which would be useful during comparing of databases"""
    def __init__(self, logger):
        self.prod: SqlAlchemyHelper = SqlAlchemyHelper(SqlCredentials(), logger)
        self.test: SqlAlchemyHelper = SqlAlchemyHelper(SqlCredentials(), logger)
        self.tables = Tables()
        self.columns = Columns()
        self.logger: logging.Logger = logger

    def compare_table_metadata(self, table, columns) -> pd.DataFrame:
        """Method intended to compare metadata of two tables"""
        start_time = datetime.now(timezone.utc)
        self.logger.info(f"Compare schema for table {table}...")
        diff_df = df_compare_helper.get_metadata_dataframe_diff(self.prod, self.test,
                                                                table, columns, self.logger)
        schema_comparing_time = datetime.now(timezone.utc) - start_time
        self.logger.debug(f"Schema of table {table} compared in {schema_comparing_time}")
        return diff_df

    def warn_columns_differs(self, table, uniques) -> None:
        """Print warning logs about differs columns"""
        host = self.prod.credentials.host
        base = self.prod.credentials.base
        self.logger.warning(f"There is some unique columns in {host / base} "
                            f"table {table}: {','.join(uniques)}")

    def compare_data(self, table: str) -> pd.DataFrame:
        """Method intended to compare data of two tables"""
        start_time = datetime.now(timezone.utc)
        start_table_check_time = datetime.now(timezone.utc)
        self.logger.info(f"Table {table} processing started now...")
        checking_time = datetime.now(timezone.utc) - start_table_check_time
        self.logger.info(f"Table {table} checked in {checking_time}...")
        data_comparing_time = datetime.now(timezone.utc) - start_time
        self.logger.info(f'Comparing finished in {data_comparing_time}')
        return pd.DataFrame()


@dataclass
class Tables:
    """Class intended for included and excluded tables"""
    included: Dict = field(default_factory=lambda: {})
    excluded: Dict = field(default_factory=lambda: {})
    hard_excluded: Dict = field(default_factory=lambda: {})
    all: Dict = field(default_factory=lambda: {})
    to_compare: List = field(default_factory=lambda: [])

    def get_compare(self) -> List[str]:
        """Calculates list of tables to compare"""
        if self.included:
            self.to_compare = list(self.included.keys())
        elif self.excluded:
            tables: List = []
            for table in self.all:
                if table not in self.excluded:
                    tables.append(table)
            self.to_compare = tables
        else:
            self.to_compare = list(self.all.keys())
        if self.hard_excluded:
            for table in self.hard_excluded:
                if table in self.to_compare:
                    self.to_compare.remove(table)
        return self.to_compare


@dataclass
class Columns:
    """Class intended for included and excluded columns"""
    excluded: List = field(default_factory=lambda: [])
    included: List = field(default_factory=lambda: [])
    all: List = field(default_factory=lambda: [])

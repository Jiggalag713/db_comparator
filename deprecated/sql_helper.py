import logging
from multiprocessing.dummy import Pool
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from typing import Optional, List, Dict


class SqlAlchemyHelper:
    def __init__(self, host, user, password, db, logger):
        self.meta = sqlalchemy.schema.MetaData()
        self.read_timeout = None  # TODO: check if it useful
        self.host: str = host
        self.user: str = user
        self.password: str = password
        self.db: str = db
        self.db_not_found: bool = False  # TODO: check if it useful
        self.logger: logging.Logger = logger
        self.engine: sqlalchemy.engine.Engine = self.get_engine()
        self.connection: Optional[sqlalchemy.engine.Connection] = self.get_connection()
        # TODO: rename db_list -> databases
        self.db_list: Optional[List[str]] = self.get_databases()
        self.tables = self.get_tables()

    def get_engine(self) -> Optional[sqlalchemy.engine.Engine]:
        if all([self.host, self.user, self.password, self.db]):
            self.logger.debug(f'Engine to {self.host}/{self.db} successfully generated with credentials...')
            return create_engine(f'mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.db}')
        if all([self.host, self.user, self.password]):
            self.logger.debug(f'Engine to {self.host} successfully generated with credentials...')
            return create_engine(f'mysql+pymysql://{self.user}:{self.password}@{self.host}')
        else:
            self.logger.debug('There is no some connection parameters, engine is not generated...')
            self.logger.debug(f'host is {self.host}, user is {self.user}, password is ********, db is {self.db}')
            return None

    def get_connection(self) -> Optional[sqlalchemy.engine.Connection]:
        if self.engine:
            return self.engine.connect()
        else:
            return None

    def get_databases(self) -> Optional[List[str]]:
        if self.engine:
            try:
                inspection = sqlalchemy.inspect(self.engine)
                db_list = inspection.get_schema_names()
                if self.db is not None and db_list:
                    if self.db not in db_list:
                        self.logger.error(f'Database {self.db} is not found in database list!')
                        self.db_not_found = True
                return db_list
            except sqlalchemy.exc.OperationalError as e:
                self.logger.error(e)
                return None

    def get_tables(self) -> Dict[str, List[str]]:
        if all([self.engine, self.db_list]):
            self.meta.reflect(bind=self.engine)
            result_tables = {}
            tables = self.meta.tables
            for table in tables:
                columns = []
                for column in tables.get(table).columns:
                    columns.append(column.name)
                result_tables.update({table: columns})
            return result_tables

    def warming_up(self) -> None:
        self.engine = self.get_engine()
        self.connection = self.get_connection()
        self.db_list = self.get_databases()
        self.tables = self.get_tables()

    def select(self, query: str) -> Optional[List]:
        if self.connection is not None:
            error_count = 0
            while error_count < self.attempts:
                sql_query = query.replace('DBNAME', self.db)
                self.logger.debug(sql_query)
                result = []
                for item in self.engine.execute(sql_query):
                    result.append(item)
                return result
        else:
            return None

    # TODO: potentially deprecated, should be deleted
    def set_keyvalues(self, **kwargs):
        for key in list(kwargs.keys()):
            if 'hideColumns' in key:
                self.hide_columns = kwargs.get(key)
            if 'attempts' in key:
                self.attempts = int(kwargs.get(key))
            if 'mode' in key:
                self.mode = kwargs.get(key)
            if 'comparingStep' in key:
                self.comparing_step = kwargs.get(key)
            if 'excludedTables' in key:
                self.excluded_tables = kwargs.get(key)  # TODO: add split?
            if 'clientIgnoredTables' in key:
                self.client_ignored_tables = kwargs.get(key)  # TODO: add split?
            if 'enableSchemaChecking' in key:
                self.check_schema = kwargs.get(key)
            if 'depthReportCheck' in key:
                self.check_depth = kwargs.get(key)
            if 'failWithFirstError' in key:
                self.quick_fall = kwargs.get(key)
            if 'schemaColumns' in key:
                self.schema_columns = kwargs.get(key)  # TODO: add split?
            if 'separateChecking' in key:
                self.separate_checking = kwargs.get(key)
            if 'read_timeout' in key:
                self.read_timeout = int(kwargs.get(key))
            return self

    def get_column_list(self, table):
        if self.connection is not None:
            query = (f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{table}' "
                     f"AND table_schema = '{self.db}';")
            self.logger.debug(query)
            columns = []
            for i in self.connection.execute(query):
                element = i[0].lower()  # TODO: get rid of this hack
                columns.append(element)
            for column in self.hide_columns:
                # TODO: get rid of this hack
                if column.replace('_', '') in columns:
                    columns.remove(column)
            if not columns:
                return ""
            column_string = ','.join(columns)
            return column_string.lower().split(',')
        else:
            return None

    @staticmethod
    def parallel_select(connection_list, query):
        pool = Pool(2)  # TODO: remove hardcode, change to dynamically defining amount of threads
        result = pool.map((lambda x: pd.read_sql(query.replace('DBNAME', x.url.database), x)), connection_list)
        pool.close()
        pool.join()
        return result


def get_amount_records(table, dates, sql_connection_list):
    if dates is None:
        query = f"SELECT COUNT(*) FROM `{table}`;"
    else:
        query = f"SELECT COUNT(*) FROM `{table}` WHERE dt >= '{dates[0]}';"
    result = get_comparable_objects(sql_connection_list, query)
    return result[0].values[0][0], result[1].values[0][0]


# TODO: strongly refactor this code!
def get_raw_objects(connection_list, query):
    result = SqlAlchemyHelper.parallel_select(connection_list, query)
    if (result[0] is None) or (result[1] is None):
        return None, None
    else:
        return result[0], result[1]


def get_raw_object(connection, query):
    return pd.read_sql(query.replace('DBNAME', connection.url.database), connection)


# returns list for easy convertation to set
# TODO: remove this interlayer
def get_comparable_objects(connection_list, query):
    result = get_raw_objects(connection_list, query)
    if len(result[0].index) != len(result[1].index):
        return result[0], result[1]
    result[0].sort_index(axis=1)
    result[1].sort_index(axis=1)
    return result[0], result[1]


def get_column_list_for_sum(set_column_list):
    column_list_with_sums = []
    for item in set_column_list.split(","):
        if "clicks" in item or "impressions" in item:
            column_list_with_sums.append("sum(" + item + ")")
        else:
            column_list_with_sums.append(item)
    return column_list_with_sums

"""Module contains implementation of class, intended to work with sql"""
import logging
from typing import Optional, List, Dict
import sqlalchemy
from sqlalchemy import create_engine


class SqlAlchemyHelper:
    """Class implements work with sql"""
    def __init__(self, host, user, password, database, logger):
        self.meta = sqlalchemy.schema.MetaData()
        self.host: str = host
        self.user: str = user
        self.password: str = password
        self.db: str = database
        self.logger: logging.Logger = logger
        self.engine: sqlalchemy.engine.Engine = self.get_engine()
        self.connection: Optional[sqlalchemy.engine.Connection] = self.get_connection()
        self.databases: Optional[List[str]] = self.get_databases()
        self.tables = self.get_tables()

    def get_engine(self) -> Optional[sqlalchemy.engine.Engine]:
        """Method returns engine or None"""
        if all([self.host, self.user, self.password, self.db]):
            self.logger.debug(f'Engine to {self.host}/{self.db} successfully '
                              f'generated with credentials...')
            return create_engine(f'mysql+pymysql://{self.user}:{self.password}@'
                                 f'{self.host}/{self.db}')
        if all([self.host, self.user, self.password]):
            self.logger.debug(f'Engine to {self.host} successfully generated with credentials...')
            return create_engine(f'mysql+pymysql://{self.user}:{self.password}@{self.host}')
        self.logger.debug('There is no some connection parameters, engine is not generated...')
        self.logger.debug(f'host is {self.host}, user is {self.user}, '
                          f'password is ********, db is {self.db}')
        return None

    def get_connection(self) -> Optional[sqlalchemy.engine.Connection]:
        """Method returns connection to engine or None"""
        if self.engine:
            return self.engine.connect()
        return None

    def get_databases(self) -> Optional[List[str]]:
        """Method gets database list"""
        if self.engine:
            try:
                inspection = sqlalchemy.inspect(self.engine)
                db_list = inspection.get_schema_names()
                if self.db is not None and db_list:
                    if self.db not in db_list:
                        self.logger.error(f'Database {self.db} is not found in database list!')
                return db_list
            except sqlalchemy.exc.OperationalError as exception:
                self.logger.error(exception)
                return None
        return None

    def get_tables(self) -> Optional[Dict[str, List[str]]]:
        """Method gets table list for proper database"""
        if all([self.engine, self.databases]):
            self.meta.reflect(bind=self.engine)
            result_tables = {}
            tables = self.meta.tables
            for table in tables:
                columns = []
                for column in tables.get(table).columns:
                    columns.append(column.name)
                result_tables.update({table: columns})
            return result_tables
        return None

    def warming_up(self) -> None:
        """Method gets engine, connection, database list and table list for checked database"""
        self.engine = self.get_engine()
        self.connection = self.get_connection()
        self.databases = self.get_databases()
        self.tables = self.get_tables()

"""Module contains implementation of class, intended to work with sql"""
import logging
from dataclasses import dataclass, field
from typing import Optional, List, Dict
import sqlalchemy
from sqlalchemy import create_engine


class SqlAlchemyHelper:
    """Class implements work with sql"""
    def __init__(self, credentials, logger):
        self.meta = sqlalchemy.schema.MetaData()
        self.credentials = credentials
        self.logger: logging.Logger = logger
        self.engine: sqlalchemy.engine.Engine = self.get_engine()
        self.databases: Optional[List[str]] = self.get_databases()
        self.tables = self.get_tables()

    def get_engine(self) -> Optional[sqlalchemy.engine.Engine]:
        """Method returns engine or None"""
        if all([self.credentials.host, self.credentials.user,
               self.credentials.password, self.credentials.base]):
            self.logger.debug(f'Engine to {self.credentials.host}/{self.credentials.base} '
                              f'successfully generated with credentials...')
            return create_engine(f'mysql+pymysql://{self.credentials.user}:'
                                 f'{self.credentials.password}@'
                                 f'{self.credentials.host}/{self.credentials.base}')
        if all([self.credentials.host, self.credentials.user, self.credentials.password]):
            self.logger.debug(f'Engine to {self.credentials.host} successfully '
                              f'generated with credentials...')
            return create_engine(f'mysql+pymysql://{self.credentials.user}:'
                                 f'{self.credentials.password}@{self.credentials.host}')
        self.logger.debug('There is no some connection parameters, engine is not generated...')
        self.logger.debug(f'host is {self.credentials.host}, user is {self.credentials.user}, '
                          f'password is ********, db is {self.credentials.base}')
        return None

    def get_databases(self) -> Optional[List[str]]:
        """Method gets database list"""
        if self.engine:
            self.engine.connect()
            try:
                inspection = sqlalchemy.inspect(self.engine)
                db_list = inspection.get_schema_names()
                if self.credentials.base is not None and db_list:
                    if self.credentials.base not in db_list:
                        self.logger.error(f'Database {self.credentials.basebase} '
                                          f'is not found in database list!')
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
        self.databases = self.get_databases()
        self.tables = self.get_tables()


@dataclass
class SqlCredentials:
    """Class intended for storing sql credentials"""
    host: str = ''
    user: str = ''
    password: str = ''
    base: str = ''

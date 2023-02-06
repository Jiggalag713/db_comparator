"""Module contains implementation of TableCalculation class, intended
 for calculating table lists"""
from typing import Dict, List

from configuration.main_config import Configuration
from ui_logic.common import set_ui_value


class TableCalculation:
    """Class intended for calculating different table lists"""
    def __init__(self, configuration: Configuration):
        self.configuration: Configuration = configuration
        self.logger = configuration.system_config.logger

    def calculate_table_list(self) -> None:
        """Method calculates of tables, which exists in both databases"""
        prod = self.configuration.sql_variables.prod
        test = self.configuration.sql_variables.test
        line_edits = self.configuration.ui_elements.line_edits
        if all([prod.tables, test.tables]):
            self.configuration.sql_variables.inc_exc.included_tables = []
            tables = list(set(prod.tables.keys()) & set(test.tables.keys()))
            tables.sort()
            for table in tables:
                prod_columns = prod.tables.get(table)
                test_columns = test.tables.get(table)
                if prod_columns == test_columns:
                    self.configuration.sql_variables.inc_exc.included_tables.append(table)
                else:
                    self.logger.error(f"There is different columns for table {table}.")
                    self.logger.warning(f"Table {table} excluded from comparing")
                    included_tables = line_edits.included_tables.text().split(',')
                    if '' in included_tables:
                        included_tables.remove('')
                    if table in included_tables:
                        included_tables.remove(table)
                        line_edits.included_tables.setText(','.join(included_tables))
                    excluded_table = line_edits.excluded_tables.text().split(',')
                    if '' in excluded_table:
                        excluded_table.remove('')
                    if table not in excluded_table:
                        excluded_table.append(table)
                        line_edits.excluded_tables.setText(','.join(excluded_table))
                    prod_uniq_columns = set(prod_columns) - set(test_columns)
                    test_uniq_columns = set(test_columns) - set(prod_columns)
                    if prod_uniq_columns:
                        self.logger.info(f"Uniq columns for prod {table}: {prod_uniq_columns}")
                    if test_uniq_columns:
                        self.logger.info(f"Uniq columns for test {table}: {test_uniq_columns}")
            copy = self.configuration.sql_variables.inc_exc.included_tables.copy()
            self.configuration.sql_variables.tables_for_ui = copy
            self.configuration.sql_variables.columns = self.calculate_column_list()
            self.calculate_excluded_columns()

    def get_tables_for_ui(self) -> Dict:
        """Method returns dictionary in format {table_name: [column_list]}"""
        result = {}
        for table in self.configuration.sql_variables.inc_exc.included_tables:
            result.update({table: self.configuration.sql_variables.prod.tables})
        return result

    def calculate_column_list(self) -> List[str]:
        """Methods calculates column list"""
        columns = []
        tables = self.configuration.sql_variables.tables_for_ui
        for table in tables:
            for column in self.configuration.sql_variables.prod.tables.get(table):
                columns.append(f'{table}.{column}')
        columns.sort()
        return columns

    def calculate_excluded_columns(self) -> None:
        """Method calculates list of excluded column"""
        line_edits = self.configuration.ui_elements.line_edits
        set_ui_value(line_edits.excluded_tables, line_edits.excluded_tables.text())
        set_ui_value(line_edits.excluded_columns, line_edits.excluded_columns.text())
        for table in self.configuration.sql_variables.tables_for_ui:
            if table in self.configuration.sql_variables.inc_exc.excluded_tables:
                columns = self.configuration.sql_variables.tables_for_ui.get(table)
                for column in columns:
                    excluded_columns = self.configuration.sql_variables.inc_exc.excluded_column
                    if column not in excluded_columns:
                        excluded_columns.append(f'{table}.{column}')
        self.configuration.sql_variables.inc_exc.excluded_columns.sort()

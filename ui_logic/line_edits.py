"""Module contains LineEditsLogic with implementation line_edits logic"""
from typing import List

from custom_ui_elements.clickable_item_view import ClickableItemsView
from custom_ui_elements.radiobutton_items_view import RadiobuttonItemsView


class LineEditsLogic:
    """Class line_edits logic"""
    def __init__(self, variables):
        self.variables = variables

    def get_selected_excluded_tables(self) -> List[str]:
        """Method sets excluded tables"""
        if all([self.variables.sql_variables.prod.tables,
                self.variables.sql_variables.test.tables]):
            tables = self.variables.sql_variables.tables.all
            excluded_tables = self.variables.sql_variables.tables.excluded
            hard_excluded = self.variables.sql_variables.tables.hard_excluded
            excluded_tables_view = ClickableItemsView(tables, excluded_tables,
                                                      hard_excluded, False)
            excluded_tables_view.exec_()
            return excluded_tables_view.selected_items
        return []

    def get_selected_included_columns(self) -> List[str]:
        """Method sets excluded columns"""
        excluded_columns = self.variables.sql_variables.columns.excluded
        all_columns = self.get_all_columns()
        excluded_columns = ClickableItemsView(all_columns, excluded_columns)
        excluded_columns.exec_()
        return excluded_columns.selected_items

    def get_selected_included_tables(self) -> List[str]:
        """Method sets included tables to UI"""
        if all([self.variables.sql_variables.prod.tables,
                self.variables.sql_variables.test.tables]):
            tables = self.variables.sql_variables.tables.all
            included_tables = self.variables.sql_variables.tables.included
            hard_excluded = self.variables.sql_variables.tables.hard_excluded
            included_tables = ClickableItemsView(tables, included_tables, hard_excluded, True)
            included_tables.exec_()
            return included_tables.selected_items
        return []

    @staticmethod
    def set_db(db_list: List[str], database: str) -> str:
        """Method implements common approach of setting database"""
        if db_list:
            select_db_view = RadiobuttonItemsView(db_list, database)
            select_db_view.exec_()
            return select_db_view.selected_db
        return ''

    def get_all_columns(self) -> List:
        """Returns full list of table columns (without columns of hardly excluded tables)"""
        columns = []
        if self.variables.sql_variables.tables.included:
            tables = self.variables.sql_variables.tables.included
        else:
            tables = self.variables.sql_variables.tables.all.copy()
            for table in self.variables.sql_variables.tables.excluded:
                if table in tables:
                    tables.pop(table)
        for table in tables:
            for column in tables.get(table):
                columns.append(f'{table}.{column}')
        columns.sort()
        return columns

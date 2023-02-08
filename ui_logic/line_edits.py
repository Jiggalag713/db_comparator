"""Module contains LineEditsLogic with implementation line_edits logic"""
from typing import List

from PyQt5.QtWidgets import QLineEdit

from configuration.main_config import Configuration
from custom_ui_elements.clickable_items_view import ClickableItemsView
from custom_ui_elements.radiobutton_items_view import RadiobuttonItemsView


class LineEditsLogic:
    """Class line_edits logic"""
    def __init__(self, configuration, table_calculation):
        self.configuration: Configuration = configuration
        self.variables = configuration.variables
        self.main_ui = configuration.ui_elements
        self.table_calculation = table_calculation

    def set_excluded_tables(self) -> None:
        """Method sets excluded tables"""
        if all([self.variables.sql_variables.prod.tables,
                self.variables.sql_variables.test.tables]):
            excluded_tables = self.configuration.ui_elements.line_edits.excluded_tables
            tables_to_skip = excluded_tables.text().split(',')
            tables_for_ui = self.variables.sql_variables.tables_for_ui
            excluded_tables_view = ClickableItemsView(tables_for_ui, tables_to_skip)
            excluded_tables_view.exec_()
            text = ','.join(excluded_tables_view.selected_items)
            self.main_ui.line_edits.excluded_tables.setText(text)
            tooltip_text = self.main_ui.line_edits.excluded_tables.text().replace(',', ',\n')
            self.main_ui.line_edits.excluded_tables.setToolTip(tooltip_text)
            self.table_calculation.calculate_excluded_columns()

    def set_excluded_columns(self) -> None:
        """Method sets excluded columns"""
        exc_columns = self.variables.sql_variables.inc_exc.excluded_columns
        excluded_columns = ClickableItemsView(self.variables.sql_variables.columns,
                                              exc_columns)
        excluded_columns.exec_()
        self.main_ui.line_edits.excluded_columns.setText(','.join(excluded_columns.selected_items))
        text = self.main_ui.line_edits.excluded_columns.text().replace(',', ',\n')
        self.main_ui.line_edits.excluded_columns.setToolTip(text)

    def set_included_tables(self) -> None:
        """Method sets included tables to UI"""
        if all([self.variables.sql_variables.prod.tables,
                self.variables.sql_variables.test.tables]):
            tables_to_include = self.main_ui.line_edits.included_tables.text().split(',')
            included_tables = ClickableItemsView(self.variables.sql_variables.tables_for_ui,
                                                 tables_to_include)
            included_tables.exec_()
            text = ','.join(included_tables.selected_items)
            self.main_ui.line_edits.included_tables.setText(text)
            included_tables_text = self.main_ui.line_edits.included_tables.text()
            included_tables_text = included_tables_text.replace(',', ',\n')
            self.main_ui.line_edits.included_tables.setToolTip(included_tables_text)

    def set_prod_db(self) -> None:
        """Method sets prod database"""
        self.set_db(self.main_ui.line_edits.prod.base,
                    self.variables.sql_variables.prod.databases)

    def set_test_db(self) -> None:
        """Method sets test database"""
        self.set_db(self.main_ui.line_edits.test.base,
                    self.variables.sql_variables.test.databases)

    @staticmethod
    def set_db(line_edit: QLineEdit, db_list: List[str]) -> None:
        """Method implements common approach of setting database"""
        if db_list:
            database = line_edit.text()
            select_db_view = RadiobuttonItemsView(db_list, database)
            select_db_view.exec_()
            line_edit.setText(select_db_view.selected_db)
            line_edit.setToolTip(line_edit.text())

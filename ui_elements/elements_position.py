"""Module contains class intended for positioning main window UI elements"""
from PyQt5.QtWidgets import QGridLayout


class ElementPositions:
    """Class for positioning UI elements of main window"""
    def __init__(self):
        self.grid: QGridLayout = QGridLayout()
        self.grid.setSpacing(10)

    def locate_elements(self, labels, line_edits, checkboxes, buttons, radio_buttons) -> None:
        """Method locates elements of main window on a grid"""
        self.grid.addWidget(labels.prod.host, 0, 0)
        self.grid.addWidget(line_edits.prod.host, 0, 1)
        self.grid.addWidget(labels.prod.user, 1, 0)
        self.grid.addWidget(line_edits.prod.user, 1, 1)
        self.grid.addWidget(labels.prod.password, 2, 0)
        self.grid.addWidget(line_edits.prod.password, 2, 1)
        self.grid.addWidget(labels.prod.db, 3, 0)
        self.grid.addWidget(line_edits.prod.db, 3, 1)
        self.grid.addWidget(buttons.btn_check_prod, 4, 1)
        self.grid.addWidget(labels.test.host, 0, 2)
        self.grid.addWidget(line_edits.test.host, 0, 3)
        self.grid.addWidget(labels.test.user, 1, 2)
        self.grid.addWidget(line_edits.test.user, 1, 3)
        self.grid.addWidget(labels.test.password, 2, 2)
        self.grid.addWidget(line_edits.test.password, 2, 3)
        self.grid.addWidget(labels.test.db, 3, 2)
        self.grid.addWidget(line_edits.test.db, 3, 3)
        self.grid.addWidget(buttons.btn_check_test, 4, 3)
        self.grid.addWidget(labels.send_mail_to, 6, 0)
        self.grid.addWidget(line_edits.send_mail_to, 6, 1)
        self.grid.addWidget(labels.included_tables, 7, 0)
        self.grid.addWidget(line_edits.included_tables, 7, 1)
        self.grid.addWidget(labels.excluded_tables, 8, 0)
        self.grid.addWidget(line_edits.excluded_tables, 8, 1)
        self.grid.addWidget(labels.excluded_columns, 9, 0)
        self.grid.addWidget(line_edits.excluded_columns, 9, 1)
        self.grid.addWidget(checkboxes.get('check_schema'), 10, 0)
        self.grid.addWidget(checkboxes.get('fail_fast'), 11, 0)
        self.grid.addWidget(checkboxes.get('check_reports'), 10, 1)
        self.grid.addWidget(checkboxes.get('check_entities'), 11, 1)
        self.grid.addWidget(checkboxes.get('use_dataframes'), 10, 2)
        self.grid.addWidget(labels.checking_mode, 6, 3)
        self.grid.addWidget(radio_buttons.day_summary_mode, 7, 3)
        self.grid.addWidget(radio_buttons.section_summary_mode, 8, 3)
        self.grid.addWidget(radio_buttons.detailed_mode, 9, 3)
        self.grid.addWidget(buttons.btn_clear_all, 5, 1)
        self.grid.addWidget(buttons.btn_advanced, 10, 3)
        self.grid.addWidget(buttons.btn_set_configuration, 11, 3)

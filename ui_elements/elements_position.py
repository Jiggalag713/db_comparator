"""Module contains class intended for positioning main window UI elements"""
from PyQt5.QtWidgets import QGridLayout


class ElementPositions:
    """Class for positioning UI elements of main window"""
    def __init__(self):
        self.grid: QGridLayout = QGridLayout()
        self.grid.setSpacing(10)
        self.grid.setColumnStretch(0, 0)

    def locate_labels_line_edits(self, labels, line_edits) -> None:
        """Method locates elements of main window on a grid"""
        self.grid.addWidget(labels.prod.host, 0, 0)
        self.grid.addWidget(line_edits.prod.host, 0, 1)
        self.grid.addWidget(labels.prod.port, 1, 0)
        self.grid.addWidget(line_edits.prod.port, 1, 1)
        self.grid.addWidget(labels.prod.user, 2, 0)
        self.grid.addWidget(line_edits.prod.user, 2, 1)
        self.grid.addWidget(labels.prod.password, 3, 0)
        self.grid.addWidget(line_edits.prod.password, 3, 1)
        self.grid.addWidget(labels.prod.base, 4, 0)
        self.grid.addWidget(line_edits.prod.base, 4, 1)
        self.grid.addWidget(labels.test.host, 0, 2)
        self.grid.addWidget(line_edits.test.host, 0, 3)
        self.grid.addWidget(labels.test.port, 1, 2)
        self.grid.addWidget(line_edits.test.port, 1, 3)
        self.grid.addWidget(labels.test.user, 2, 2)
        self.grid.addWidget(line_edits.test.user, 2, 3)
        self.grid.addWidget(labels.test.password, 3, 2)
        self.grid.addWidget(line_edits.test.password, 3, 3)
        self.grid.addWidget(labels.test.base, 4, 2)
        self.grid.addWidget(line_edits.test.base, 4, 3)
        self.grid.addWidget(labels.send_mail_to, 7, 0)
        self.grid.addWidget(line_edits.send_mail_to, 7, 1)
        self.grid.addWidget(labels.included_tables, 8, 0)
        self.grid.addWidget(line_edits.included_tables, 8, 1)
        self.grid.addWidget(labels.excluded_tables, 9, 0)
        self.grid.addWidget(line_edits.excluded_tables, 9, 1)
        self.grid.addWidget(labels.excluded_columns, 10, 0)
        self.grid.addWidget(line_edits.excluded_columns, 10, 1)

    def locate_other(self, checkboxes, buttons, radio_buttons) -> None:
        """Method locates checkboxes, buttons and radio_buttons
         of main window on a grid"""
        self.grid.addWidget(buttons.btn_check_prod, 5, 1)
        self.grid.addWidget(buttons.btn_check_test, 5, 3)
        self.grid.addWidget(checkboxes.get('check_schema'), 11, 0)
        self.grid.addWidget(checkboxes.get('fail_fast'), 12, 0)
        self.grid.addWidget(checkboxes.get('check_reports'), 11, 1)
        self.grid.addWidget(checkboxes.get('check_entities'), 12, 1)
        self.grid.addWidget(checkboxes.get('use_dataframes'), 11, 2)
        self.grid.addWidget(radio_buttons.get('day-sum'), 8, 3)
        self.grid.addWidget(radio_buttons.get('section-sum'), 9, 3)
        self.grid.addWidget(radio_buttons.get('detailed'), 10, 3)
        self.grid.addWidget(buttons.btn_clear_all, 6, 1)
        self.grid.addWidget(buttons.btn_advanced, 11, 3)
        self.grid.addWidget(buttons.btn_set_configuration, 12, 3)

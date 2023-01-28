"""Module intended to store ElementPosition class for advanced
settings window"""
from PyQt5.QtWidgets import QGridLayout


class ElementPositions:
    """Class intended ti store positions of elements for advanced
    settings window"""
    def __init__(self):
        self.grid: QGridLayout = QGridLayout()
        self.grid.setSpacing(10)

    def locate_elements(self, labels, line_edits, combo_box, buttons) -> None:
        """Method locates elements on a grid"""
        self.grid.addWidget(labels.logging_level_label, 0, 0)
        self.grid.addWidget(combo_box, 0, 1)
        self.grid.addWidget(labels.comparing_step_label, 1, 0)
        self.grid.addWidget(line_edits.comparing_step, 1, 1)
        self.grid.addWidget(labels.depth_report_check_label, 2, 0)
        self.grid.addWidget(line_edits.depth_report_check, 2, 1)
        self.grid.addWidget(labels.schema_columns_label, 3, 0)
        self.grid.addWidget(line_edits.schema_columns, 3, 1)
        self.grid.addWidget(labels.retry_attempts_label, 4, 0)
        self.grid.addWidget(line_edits.retry_attempts, 4, 1)
        self.grid.addWidget(labels.path_to_logs_label, 5, 0)
        self.grid.addWidget(line_edits.path_to_logs, 5, 1)
        self.grid.addWidget(labels.table_timeout_label, 6, 0)
        self.grid.addWidget(line_edits.table_timeout, 6, 1)
        self.grid.addWidget(labels.strings_amount_label, 7, 0)
        self.grid.addWidget(line_edits.strings_amount, 7, 1)
        self.grid.addWidget(buttons.get('btn_ok'), 8, 0)
        self.grid.addWidget(buttons.get('btn_cancel'), 8, 1)
        self.grid.addWidget(buttons.get('btn_reset'), 9, 0)

"""Module contains class with implementation checkboxes of main window"""
from PyQt5.QtWidgets import QCheckBox
from ui_logic.checkboxes import toggle


class Checkboxes:
    """Class contains implementation checkboxes of main window"""
    def __init__(self, is_toggled):
        self.check_schema = QCheckBox('Compare schema')
        self.check_reports = QCheckBox('Reports')
        self.fail_fast = QCheckBox('Only first error')
        self.check_entities = QCheckBox('Entities and others')
        self.use_dataframes = QCheckBox('Enable dataframes')
        self.check_schema.setChecked(is_toggled)
        self.check_reports.setChecked(is_toggled)
        self.check_entities.setChecked(is_toggled)
        self.use_dataframes.setChecked(is_toggled)
        self.check_schema.setToolTip('If you set this option, program '
                                     'will compare also schemas of dbs')
        self.fail_fast.setToolTip('If you set this option, comparing '
                                  'will be finished after first error')
        self.check_entities.setToolTip('Check entity tables')
        self.check_reports.setToolTip('Check report tables')
        self.use_dataframes.setToolTip('Use dataframes during comparing')
        toggle(self)

"""Module intended for storing UIElements class"""
from typing import Dict

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QRadioButton
from ui_elements.buttons import Buttons
from ui_elements.elements_position import ElementPositions
from ui_elements.labels import Labels
from ui_elements.line_edits import LineEdits


class UIElements:
    """Class make together all UI elements"""
    def __init__(self):
        self.labels: Labels = Labels()
        self.line_edits: LineEdits = LineEdits()
        self.checkboxes: Dict = {
            'check_schema': QCheckBox('Compare schema'),
            'check_reports': QCheckBox('Reports'),
            'fail_fast': QCheckBox('Only first error'),
            'check_entities': QCheckBox('Entities and others'),
            'use_dataframes': QCheckBox('Enable dataframes')
        }
        self.checkboxes_states(True)

        toggle(self.checkboxes)

        self.buttons: Buttons = Buttons()
        self.radio_buttons: Dict = {
            'day-sum': QRadioButton('Day summary'),
            'section-sum': QRadioButton('Section summary'),
            'detailed': QRadioButton('Detailed')
        }
        self.positions: ElementPositions = ElementPositions()
        self.positions.locate_labels_line_edits(self.labels, self.line_edits)
        self.positions.locate_other(self.checkboxes, self.buttons, self.radio_buttons)

    def checkboxes_states(self, is_toggled) -> None:
        """Method intended for setting checkboxes states"""
        for key in ['check_schema', 'check_reports', 'check_entities', 'use_dataframes']:
            check_box = self.checkboxes.get(key)
            if isinstance(check_box, QCheckBox):
                check_box.setChecked(is_toggled)

    def radio_buttons_states(self) -> None:
        """Method intended for setting radio_buttons states"""
        for key in ['day-sum', 'section-sum', 'detailed']:
            radio_button = self.radio_buttons.get(key)
            if isinstance(radio_button, QRadioButton):
                if 'day-sum' in key:
                    radio_button.setChecked(True)
                else:
                    radio_button.setChecked(False)

    def set_radio_buttons_tooltips(self) -> None:
        """Method intended for setting tooltips to radio_buttons"""
        day_summary = self.radio_buttons.get('day_summary')
        if isinstance(day_summary, QRadioButton):
            day_summary.setToolTip('Compare sums of impressions for each date')
        section_summary = self.radio_buttons.get('section_summary')
        if isinstance(section_summary, QRadioButton):
            section_summary.setToolTip('Compare sums of impressions for each date and each section')
        detailed = self.radio_buttons.get('detailed')
        if isinstance(detailed, QRadioButton):
            detailed.setToolTip('Compare all records from table for set period')

    def set_checkboxes_tooltips(self) -> None:
        """Method intended for setting tooltips to checkboxes"""
        check_schema = self.checkboxes.get('check_schema')
        if isinstance(check_schema, QCheckBox):
            check_schema.setToolTip('If you set this option, program '
                                    'will compare also schemas of dbs')
        fail_fast = self.checkboxes.get('fail_fast')
        if isinstance(fail_fast, QCheckBox):
            fail_fast.setToolTip('If you set this option, comparing '
                                 'will be finished after first error')
        check_entities = self.checkboxes.get('check_entities')
        if isinstance(check_entities, QCheckBox):
            check_entities.setToolTip('Check entity tables')
        check_reports = self.checkboxes.get('check_reports')
        if isinstance(check_reports, QCheckBox):
            check_reports.setToolTip('Check report tables')
        use_dataframes = self.checkboxes.get('use_dataframes')
        if isinstance(use_dataframes, QCheckBox):
            use_dataframes.setToolTip('Use dataframes during comparing')


@pyqtSlot()
def toggle(checkboxes):
    """Method consistently changes checkboxes states"""
    if all([checkboxes.get('check_entities').isChecked(),
            checkboxes.get('check_reports').isChecked()]):
        checkboxes.get('check_entities').setEnabled(True)
        checkboxes.get('check_reports').setEnabled(True)
    elif checkboxes.get('check_entities').isChecked():
        checkboxes.get('check_entities').setEnabled(False)
    elif checkboxes.get('check_reports').isChecked():
        checkboxes.get('check_reports').setEnabled(False)

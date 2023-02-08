"""Module intended for storing UIElements class"""
from typing import Dict

from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QRadioButton
from ui_elements.buttons import Buttons
from ui_elements.elements_position import ElementPositions
from ui_elements.labels import Labels
from ui_elements.line_edits import LineEdits
from ui_logic.checkboxes import toggle


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
        self.checkboxes.get('check_schema').setChecked(is_toggled)
        self.checkboxes.get('check_reports').setChecked(is_toggled)
        self.checkboxes.get('check_entities').setChecked(is_toggled)
        self.checkboxes.get('use_dataframes').setChecked(is_toggled)

    def radio_buttons_states(self) -> None:
        """Method intended for setting radio_buttons states"""
        self.radio_buttons.get('day-sum').setChecked(True)
        self.radio_buttons.get('section-sum').setChecked(False)
        self.radio_buttons.get('detailed').setChecked(False)

    def set_radio_buttons_tooltips(self) -> None:
        """Method intended for setting tooltips to radio_buttons"""
        day_summary = self.radio_buttons.get('day_summary')
        day_summary.setToolTip('Compare sums of impressions for each date')
        section_summary = self.radio_buttons.get('section_summary')
        section_summary.setToolTip('Compare sums of impressions for each date and each section')
        detailed = self.radio_buttons.get('detailed')
        detailed.setToolTip('Compare all records from table for set period')

    def set_checkboxes_tooltips(self) -> None:
        """Method intended for setting tooltips to checkboxes"""
        self.checkboxes.get('check_schema').setToolTip('If you set this option, program '
                                                       'will compare also schemas of dbs')
        self.checkboxes.get('fail_fast').setToolTip('If you set this option, comparing '
                                                    'will be finished after first error')
        self.checkboxes.get('check_entities').setToolTip('Check entity tables')
        self.checkboxes.get('check_reports').setToolTip('Check report tables')
        self.checkboxes.get('use_dataframes').setToolTip('Use dataframes during comparing')

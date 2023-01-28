"""Module contains class with implementation of radio buttons of
main window"""
from PyQt5.QtWidgets import QRadioButton


class RadioButtons:
    """Class contains implementation of radio buttons of main window"""
    def __init__(self):
        self.day_summary_mode: QRadioButton = QRadioButton('Day summary')
        self.day_summary_mode.setChecked(True)
        self.section_summary_mode: QRadioButton = QRadioButton('Section summary')
        self.section_summary_mode.setChecked(False)
        self.detailed_mode: QRadioButton = QRadioButton('Detailed')
        self.detailed_mode.setChecked(False)
        self.day_summary_mode.setToolTip('Compare sums of impressions for each date')
        self.section_summary_mode.setToolTip('Compare sums of impressions '
                                             'for each date and each section')
        self.detailed_mode.setToolTip('Compare all records from table for set period')

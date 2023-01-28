"""Module have single method for checkboxes and should be removed"""
from PyQt5.QtCore import pyqtSlot

@pyqtSlot()
def toggle(checkboxes):
    """Method consistently changes checkboxes states"""
    if all([checkboxes.check_entities.isChecked(), checkboxes.check_reports.isChecked()]):
        checkboxes.check_entities.setEnabled(True)
        checkboxes.check_reports.setEnabled(True)
        # TODO: here bug, reports not checked after first load
        # TODO: here bug, entities not checked after first load
        # TODO: radio buttons should be changed in some another module
        # radio_buttons.day_summary_mode.setEnabled(True)
        # radio_buttons.section_summary_mode.setEnabled(True)
        # radio_buttons.detailed_mode.setEnabled(True)
        # TODO: table list should be generated in some another module
        # radio_buttons.tables_for_ui = self.tables.copy()
    elif checkboxes.check_entities.isChecked():
        checkboxes.check_entities.setEnabled(False)
        # TODO: radio buttons should be changed in some another module
        # radio_buttons.day_summary_mode.setEnabled(False)
        # radio_buttons.section_summary_mode.setEnabled(False)
        # radio_buttons.detailed_mode.setEnabled(False)
        # TODO: table list should be generated in some another module
        # radio_buttons.tables_for_ui = self.get_only_entities()
    elif checkboxes.check_reports.isChecked():
        checkboxes.check_reports.setEnabled(False)
        # TODO: radio buttons should be changed in some another module
        # radio_buttons.day_summary_mode.setEnabled(True)
        # radio_buttons.section_summary_mode.setEnabled(True)
        # radio_buttons.detailed_mode.setEnabled(True)
        # TODO: table list should be generated in some another module
        # radio_buttons.tables_for_ui = self.get_only_reports()

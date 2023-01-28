"""Module have single method for checkboxes and should be removed"""
from PyQt5.QtCore import pyqtSlot


@pyqtSlot()
def toggle(checkboxes):
    """Method consistently changes checkboxes states"""
    if all([checkboxes.check_entities.isChecked(),
            checkboxes.check_reports.isChecked()]):
        checkboxes.check_entities.setEnabled(True)
        checkboxes.check_reports.setEnabled(True)
    elif checkboxes.check_entities.isChecked():
        checkboxes.check_entities.setEnabled(False)
    elif checkboxes.check_reports.isChecked():
        checkboxes.check_reports.setEnabled(False)

"""Module have single method for checkboxes and should be removed"""
from PyQt5.QtCore import pyqtSlot


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

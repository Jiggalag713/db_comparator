"""Module intended to store LineEdits class for main window"""
from PyQt5.QtWidgets import QLineEdit
from custom_ui_elements.clickable_lineedit import ClickableLineEdit


class LineEdits:
    """Class intended for line edits of main window"""
    def __init__(self):
        self.prod: SqlLineEdits = SqlLineEdits()
        self.test: SqlLineEdits = SqlLineEdits()
        self.send_mail_to: QLineEdit = QLineEdit()
        self.excluded_tables: ClickableLineEdit = ClickableLineEdit()
        self.included_tables: ClickableLineEdit = ClickableLineEdit()
        self.excluded_columns: ClickableLineEdit = ClickableLineEdit()

    def set_tooltips(self) -> None:
        """Method sets tooltips for non-specific line edits"""
        self.set_tooltip(self.send_mail_to)
        self.set_tooltip(self.included_tables)
        self.set_tooltip(self.excluded_tables)
        self.set_tooltip(self.excluded_columns)

    @staticmethod
    def set_tooltip(element: QLineEdit) -> None:
        """Unified method for setting tooltip"""
        element.setToolTip(element.text().replace(',', ',\n'))


class SqlLineEdits:
    """Intended for specific line edits, related to sql variables"""
    def __init__(self):
        self.host: QLineEdit = QLineEdit()
        # TODO: commenting of strings like this disables autoconnection to db feature
        # self.prod.le_host.textChanged.connect(lambda: self.check_sqlhost('prod'))
        self.user: QLineEdit = QLineEdit()
        # self.prod.le_user.textChanged.connect(lambda: self.check_sqlhost('prod'))
        self.password: QLineEdit = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        # self.prod.le_password.textChanged.connect(lambda: self.check_sqlhost('prod'))
        self.db: ClickableLineEdit = ClickableLineEdit()
        self.db.hide()

    def set_tooltip(self) -> None:
        """Method sets tooltips to instance of class sql-related line edits"""
        self.host.setToolTip(self.host.text())
        self.user.setToolTip(self.user.text())
        self.db.setToolTip(self.db.text())

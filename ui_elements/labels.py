"""Module contains class with labels implementation of main window"""
from PyQt5.QtWidgets import QLabel


class Labels:
    """Class contains labels implementation of main window"""
    def __init__(self):
        self.prod: SqlLabels = SqlLabels('prod')
        self.test: SqlLabels = SqlLabels('test')
        self.send_mail_to: QLabel = QLabel('Send mail to')
        self.checking_mode: QLabel = QLabel('Checking mode:')
        self.included_tables: QLabel = QLabel('Included tables')
        self.excluded_tables: QLabel = QLabel('Excluded tables')
        self.excluded_columns: QLabel = QLabel('Excluded columns')
        self.set_tooltips()

    def set_tooltips(self) -> None:
        """Method intended for setting tooltips to UI labels elements"""
        self.send_mail_to.setToolTip('Add one or list of e-mails for '
                                     'receiving results of comparing')
        self.included_tables.setToolTip('Set comma-separated list of '
                                        'tables, which should be compared')
        self.excluded_tables.setToolTip('Set tables, which should not be checked')
        self.excluded_columns.setToolTip('Set columns, which should not '
                                         'be compared during checking')
        self.checking_mode.setToolTip('Select type of checking')

    def prepare_labels(self) -> None:
        """Method intended for some label logic"""
        return


class SqlLabels:
    """Intended for specific labels, related to sql variables"""
    def __init__(self, instance_type: str):
        self.instance_type: str = instance_type
        self.host: QLabel = QLabel(f'{instance_type}.host')
        self.user: QLabel = QLabel(f'{instance_type}.user')
        self.password: QLabel = QLabel(f'{instance_type}.password')
        self.base: QLabel = QLabel(f'{instance_type}.db')
        self.set_tooltips()
        self.prepare_labels()

    def set_tooltips(self) -> None:
        """Method sets tooltips on sql-related labels"""
        self.host.setToolTip(f'Input host, where {self.instance_type}-db located.\n'
                             f'Example: db.{self.instance_type}.com')
        self.user.setToolTip(f'Input user for connection to {self.instance_type}-db.\n'
                             f'Example: {self.instance_type}')
        self.password.setToolTip(f'Input password for user from '
                                 f'{self.instance_type}.user field')
        self.base.setToolTip(f'Input {self.instance_type}-db name.\n'
                             f'Example: {self.instance_type}')

    def prepare_labels(self) -> None:
        """Method intended for some label logic"""
        self.base.hide()

"""Module contains class with custom implementation of radio button view used
in modal window when user selects databases"""
from typing import List
from PyQt5.QtWidgets import QDialog, QPushButton, QButtonGroup, QRadioButton
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QWidget, QGridLayout


class RadiobuttonItemsView(QDialog):
    """Class contains custom implementation of radio button view used
    in modal window when user selects databases"""
    def __init__(self, dbs: List, selected_db: str):
        super().__init__()
        self.layout: QGridLayout = QGridLayout()
        self.selected_db: str = selected_db
        self.databases: List[str] = dbs

        btn_ok = QPushButton('OK', self)
        btn_ok.clicked.connect(self.ok_pressed)
        btn_cancel = QPushButton('Cancel', self)
        btn_cancel.clicked.connect(self.cancel_pressed)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        self.content: QWidget = QWidget()
        scroll.setWidget(self.content)

        rb_vbox = QVBoxLayout(self.content)
        rb_vbox.addStretch(1)
        self.button_group: QButtonGroup = QButtonGroup()

        for database in self.databases:
            self.button_name: QRadioButton = QRadioButton(f"{database}")
            self.button_name.setObjectName(f"radio_btn_{database}")
            rb_vbox.addWidget(self.button_name)
            self.button_group.addButton(self.button_name)
            if database == self.selected_db:
                self.button_name.setChecked(1)

        self.layout.addWidget(scroll, 0, 0)
        self.layout.addWidget(btn_ok, 0, 1)
        self.layout.addWidget(btn_cancel, 0, 2)

        self.setWindowTitle('Select database')
        self.setLayout(self.layout)
        self.setModal(True)
        self.show()

    def ok_pressed(self) -> None:
        """Method sets selected database and closes modal window"""
        for item in range(len(self.button_group.buttons())):
            if self.button_group.buttons()[item].isChecked():
                self.selected_db = self.button_group.buttons()[item].text()
        self.close()

    def cancel_pressed(self) -> None:
        """Method closes modal window of selecting database without
        saving of changes"""
        self.close()

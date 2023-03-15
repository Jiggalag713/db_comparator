"""Module contains abstract clickable item view class"""
import collections
from typing import List, Any, Dict

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QListView, QGridLayout, QPushButton, QDialog


class ClickableItemsView(QDialog):
    """Implements abstract class clickable items view"""
    def __init__(self, item_list: Any, selected_items: List[str], hard_excluded: Dict = None,
                 include: bool = False):
        super().__init__()
        grid: QGridLayout = QGridLayout()
        grid.setSpacing(10)
        self.setLayout(grid)
        self.selected_items: List[str] = selected_items
        self.hard_excluded: Dict = hard_excluded
        self.item_list = self.get_sorted(item_list)
        self.model: QStandardItemModel = QStandardItemModel()

        btn_ok: QPushButton = QPushButton('OK', self)
        btn_ok.clicked.connect(lambda: self.ok_pressed(include))
        btn_cancel: QPushButton = QPushButton('Cancel', self)
        btn_cancel.clicked.connect(self.cancel_pressed)
        btn_clear_all: QPushButton = QPushButton('Clear all', self)
        btn_clear_all.clicked.connect(lambda: self.clear_all(include))

        view: QListView = self.init_items(include)

        grid.addWidget(view, 0, 0)
        grid.addWidget(btn_clear_all, 0, 1)
        grid.addWidget(btn_ok, 1, 1)
        grid.addWidget(btn_cancel, 1, 2)
        self.setModal(True)
        self.show()

    @staticmethod
    def get_sorted(item_list) -> Any:
        """Returns sorted item_list"""
        if isinstance(item_list, dict):
            return collections.OrderedDict(sorted(item_list.items(),
                                                  key=lambda i: i[0].lower()))
        if isinstance(item_list, list):
            return sorted(item_list, key=str.lower)
        return item_list

    def init_items(self, include) -> QListView:
        """Method init items"""
        self.model = QStandardItemModel()
        for table in self.item_list:
            item = QStandardItem(table)
            item.setCheckState(Qt.CheckState(0))
            if item.text() in self.selected_items:
                item.setCheckState(Qt.CheckState(2))
            elif self.hard_excluded is not None:
                item_text = item.text()
                if isinstance(item_text, str):
                    if item_text in self.hard_excluded.keys():
                        item.setCheckState(Qt.CheckState(self.get_included_state(include)))
                        item.setEnabled(False)
                        tooltip = self.hard_excluded.get(item_text)
                        if isinstance(tooltip, str):
                            item.setToolTip(tooltip)
            item.setCheckable(True)
            self.model.appendRow(item)

        view = QListView()
        view.setModel(self.model)
        return view

    @staticmethod
    def get_included_state(include) -> int:
        """Converts bool to proper int value"""
        if include:
            return 0
        return 2

    def ok_pressed(self, include) -> None:
        """Method saves changes which user made in UI and closes form"""
        amount = self.model.rowCount()
        checked_tables = []
        for idx in range(amount):
            item = self.model.item(idx, 0)
            if item.checkState() == 2:
                checked_tables.append(item.text())
        self.selected_items = checked_tables
        self.init_items(include)
        self.close()

    def clear_all(self, include) -> None:
        """Method clears all"""
        amount = self.model.rowCount()
        for idx in range(amount):
            item = self.model.item(idx, 0)
            if item.checkState() == 2:
                item.setCheckState(Qt.CheckState(0))
        self.selected_items = []
        self.init_items(include)

    def cancel_pressed(self) -> None:
        """Method closes form"""
        self.close()

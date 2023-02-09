"""Module contains custom clickable item view class for columns"""
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QListView

from custom_ui_elements.clickable_items_view_exclude import ClickableItemsView


class ClickableItemsViewColumn(ClickableItemsView):
    """Implements list view with ability to make some elements disabled"""
    def init_items(self) -> QListView:
        """Method init items"""
        self.model = QStandardItemModel()
        for table in self.item_list:
            for column in self.item_list.get(table):
                item = QStandardItem(f'{table}.{column}')
                item.setCheckState(0)
                text = item.text()
                if text in self.selected_items:
                    item.setCheckState(self.get_included_state(self.include))
                elif text.split('.')[0] in self.hard_excluded.keys():
                    item.setCheckState(self.get_excluded_state(self.include))
                    item.setEnabled(False)
                    item.setToolTip(self.hard_excluded.get(item.text()))
                item.setCheckable(True)
                self.model.appendRow(item)

        view = QListView()
        view.setModel(self.model)
        return view

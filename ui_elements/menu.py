"""Module contains Menu class with implementation of
application menu"""
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, qApp


class Menu:
    """Class contains implementation of application menu"""
    def __init__(self, main_window, common_logic, serialization, menubar):
        open_action: QAction = QAction(QIcon('open.png'), '&Open', main_window)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open custom file with cmp_properties')
        open_action.triggered.connect(serialization.load_configuration)

        compare_action: QAction = QAction(QIcon('compare.png'), '&Compare', main_window)
        compare_action.setShortcut('Ctrl+F')
        compare_action.setStatusTip('Run comparing')
        compare_action.triggered.connect(common_logic.start_work)

        save_action: QAction = QAction(QIcon('save.png'), '&Save', main_window)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Save current configuration to file')
        save_action.triggered.connect(serialization.save_configuration)

        exit_action = QAction(QIcon('exit.png'), '&Exit', main_window)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(qApp.quit)

        file_menu = menubar.addMenu('&File')
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(compare_action)
        file_menu.addAction(exit_action)

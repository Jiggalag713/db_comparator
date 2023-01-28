"""Module intended for storing UIElements class"""
from ui_elements.buttons import Buttons
from ui_elements.checkboxes import Checkboxes
from ui_elements.elements_position import ElementPositions
from ui_elements.labels import Labels
from ui_elements.line_edits import LineEdits
from ui_elements.radiobuttons import RadioButtons


class UIElements:
    """Class make together all UI elements"""
    def __init__(self, is_toggled, status_bar):
        self.status_bar = status_bar
        self.labels: Labels = Labels()
        self.line_edits: LineEdits = LineEdits()
        self.checkboxes: Checkboxes = Checkboxes(is_toggled)
        self.buttons: Buttons = Buttons()
        self.radio_buttons: RadioButtons = RadioButtons()
        self.positions: ElementPositions = ElementPositions()
        self.positions.locate_elements(self.labels, self.line_edits, self.checkboxes,
                                       self.buttons, self.radio_buttons)

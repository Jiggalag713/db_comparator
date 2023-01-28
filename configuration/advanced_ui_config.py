"""Module intended for storing UIElements class for advanced settings window"""
from ui_elements.advanced_buttons import Buttons
from ui_elements.advanced_combo_boxes import Comboboxes
from ui_elements.advanced_elements_position import ElementPositions
from ui_elements.advanced_labels import Labels
from ui_elements.advanced_line_edits import LineEdits


class UIElements:
    """Class make together all UI elements for advanced settings window"""
    def __init__(self):
        self.labels: Labels = Labels()
        self.line_edits: LineEdits = LineEdits()
        self.combo_boxes: Comboboxes = Comboboxes()
        self.buttons: Buttons = Buttons()
        self.positions: ElementPositions = ElementPositions()
        self.positions.locate_elements(self.labels, self.line_edits, self.combo_boxes, self.buttons)

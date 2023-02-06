"""Module intended for storing Configuration class"""
from dataclasses import dataclass, field
from typing import List

from PyQt5.QtWidgets import QStatusBar

from configuration.sql_variables import SqlVariables
from configuration.system_config import SystemConfig
from configuration.ui_config import UIElements
from configuration.default_variables import DefaultValues


@dataclass
class Configuration:
    """Class intended to make together some different variables
    in purposes throwing of this to different methods"""
    status_bar: QStatusBar
    system_config: SystemConfig
    is_toggled: bool = True
    default_values: DefaultValues = DefaultValues()
    ui_elements: UIElements = field(init=False, repr=True)

    def __post_init__(self):
        self.ui_elements = UIElements(self.is_toggled, self.status_bar)
        self.sql_variables = SqlVariables(self.system_config.logger)
        self.logger = self.system_config.logger
        self.set_connects()

    def set_connects(self):
        """Set connection between ui variables and internal logic variables"""
        self.set_line_edit_variables()
        self.set_check_boxes_variables()
        self.set_radio_buttons_variables()

    def set_line_edit_variables(self) -> None:
        """Connects line_edits with appropriate variables in
        sql_variables/default_variables object"""
        line_edits = self.ui_elements.line_edits
        self.connect_sql_related_line_edits(line_edits.prod, self.sql_variables.prod.credentials)
        self.connect_sql_related_line_edits(line_edits.test, self.sql_variables.test.credentials)
        self.connect_other_line_edits(line_edits.send_mail_to,
                                      line_edits.included_tables,
                                      line_edits.excluded_tables,
                                      line_edits.excluded_columns)

    def connect_sql_related_line_edits(self, instance, credentials) -> None:
        """Connects sql-related line_edits with appropriate internal classes attributes"""
        instance.host.textChanged.connect(lambda: self.set_sql_related_value(instance,
                                                                             credentials))
        instance.user.textChanged.connect(lambda: self.set_sql_related_value(instance,
                                                                             credentials))
        instance.password.textChanged.connect(lambda: self.set_sql_related_value(instance,
                                                                                 credentials))
        instance.base.textChanged.connect(lambda: self.set_sql_related_value(instance,
                                                                             credentials))

    def connect_other_line_edits(self, send_mail_to, included_tables,
                                 excluded_tables, excluded_columns) -> None:
        """Connects another line_edits with appropriate internal classes attributes"""
        send_mail_to.textChanged.connect(lambda: self.set_value(send_mail_to,
                                         self.default_values.__dict__,
                                         'send_mail_to'))
        included_tables.textChanged.connect(lambda: self.set_value(included_tables,
                                            self.default_values.__dict__,
                                            'included_tables'))
        excluded_tables.textChanged.connect(lambda: self.set_value(excluded_tables,
                                            self.default_values.__dict__,
                                            'excluded_tables'))
        excluded_columns.textChanged.connect(lambda: self.set_value(excluded_columns,
                                             self.default_values.__dict__,
                                             'excluded_columns'))

    def set_sql_related_value(self, instance, credentials) -> None:
        """Sets sql related value"""
        for key in instance.__dict__.keys():
            credentials.__dict__.update({key: self.transform_text(instance.host)})

    @staticmethod
    def transform_text(widget):
        """Transforms text from widget to appropriate form"""
        text = widget.text()
        if ',' in text:
            text = text.split(',')
            if '' in text:
                text.remove('')
        return text

    @staticmethod
    def set_value(widget, store, key) -> None:
        """Sets value from widget to some variable"""
        store.update({key: Configuration.transform_text(widget)})

    def set_check_boxes_variables(self) -> None:
        """Connects check_boxes with appropriate variables in
        sql_variables/default_variables object"""
        check_boxes = self.ui_elements.checkboxes
        store = self.default_values.checks_customization
        check_schema = check_boxes.get('check_schema')
        check_schema.stateChanged.connect(lambda: self.set_check_box_value(check_schema,
                                          store,
                                          'check_schema'))
        check_reports = check_boxes.get('check_reports')
        check_reports.stateChanged.connect(lambda: self.set_check_box_value(check_reports,
                                           store,
                                           'check_reports'))
        fail_fast = check_boxes.get('fail_fast')
        fail_fast.stateChanged.connect(lambda: self.set_check_box_value(fail_fast,
                                       store,
                                       'fail_fast'))
        check_entities = check_boxes.get('check_entities')
        check_entities.stateChanged.connect(lambda: self.set_check_box_value(check_entities,
                                            store,
                                            'check_entities'))
        use_dataframes = check_boxes.get('use_dataframes')
        use_dataframes.stateChanged.connect(lambda: self.set_check_box_value(use_dataframes,
                                            store,
                                            'use_dataframes'))

    @staticmethod
    def set_check_box_value(widget, fields, key) -> None:
        """Sets checkbox value from ui to appropriate variable"""
        fields.update({key: widget.isChecked()})

    def set_radio_buttons_variables(self) -> None:
        """Connects radio_buttons with appropriate variables in
        sql_variables/default_variables object"""
        radio_buttons = self.ui_elements.radio_buttons
        radio_buttons.get('day_summary').clicked.connect(self.get_radio_button_value)
        self.logger.debug('day_summary radio_button successfully connected with mode')
        radio_buttons.get('section_summary').clicked.connect(self.get_radio_button_value)
        self.logger.debug('section_summary radio_button successfully connected with mode')
        radio_buttons.get('detailed').clicked.connect(self.get_radio_button_value)
        self.logger.debug('detailed radio_button successfully connected with mode')

    def prepare_radio_buttons_mapping(self) -> List:
        """Returns mapping for radio buttons"""
        result = []
        radio_buttons = self.ui_elements.radio_buttons
        for key in ['day_summary', 'section_summary', 'detailed']:
            result.append((radio_buttons.get(key), self.default_values.__dict__, key))
        return result

    def get_radio_button_value(self) -> None:
        """Connects radio_buttons with internal variables"""
        radio_buttons = self.ui_elements.radio_buttons
        for item in radio_buttons:
            widget = radio_buttons.get(item)
            if widget.isChecked():
                if widget.text() == "Day summary":
                    self.default_values.mode = 'day_summary'
                elif widget.text() == "Section summary":
                    self.default_values.mode = 'section_summary'
                else:
                    self.default_values.mode = 'detailed'

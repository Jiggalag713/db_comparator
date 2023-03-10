"""Module intended for storing Configuration class"""
from dataclasses import dataclass, field
from typing import List

from configuration.ui_config import UIElements
from configuration.variables import Variables


@dataclass
class Configuration:
    """Class intended to make together some different variables
    in purposes throwing of this to different methods"""
    variables: Variables
    ui_elements: UIElements = field(init=False, repr=True)

    def __post_init__(self):
        self.ui_elements = UIElements()
        self.logger = self.variables.logger
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
        self.connect_sql_related_line_edits(line_edits.prod,
                                            self.variables.sql_variables.prod.credentials)
        self.connect_sql_related_line_edits(line_edits.test,
                                            self.variables.sql_variables.test.credentials)
        self.connect_other_line_edits(line_edits.send_mail_to,
                                      line_edits.included_tables,
                                      line_edits.excluded_tables,
                                      line_edits.excluded_columns)

    def connect_sql_related_line_edits(self, instance, credentials) -> None:
        """Connects sql-related line_edits with appropriate internal classes attributes"""
        instance.host.textChanged.connect(lambda: self.set_sql_related_value(instance,
                                                                             credentials,
                                                                             'host'))
        instance.user.textChanged.connect(lambda: self.set_sql_related_value(instance,
                                                                             credentials,
                                                                             'user'))
        instance.password.textChanged.connect(lambda: self.set_sql_related_value(instance,
                                                                                 credentials,
                                                                                 'password'))
        instance.base.textChanged.connect(lambda: self.set_sql_related_value(instance,
                                                                             credentials,
                                                                             'base'))

    def connect_other_line_edits(self, send_mail_to, included_tables,
                                 excluded_tables, excluded_columns) -> None:
        """Connects another line_edits with appropriate internal classes attributes"""
        send_mail_to.textChanged.connect(lambda: set_value(send_mail_to,
                                         self.variables.default_values.__dict__,
                                         'send_mail_to', str))
        included_tables.textChanged.connect(lambda: set_value(included_tables,
                                            self.variables.default_values.__dict__,
                                            'included_tables', list))
        included_tables.textChanged.connect(self.disable_exclude)
        excluded_tables.textChanged.connect(lambda: set_value(excluded_tables,
                                            self.variables.sql_variables.tables.__dict__,
                                            'excluded', list))
        excluded_columns.textChanged.connect(lambda: set_value(excluded_columns,
                                             self.variables.sql_variables.columns.__dict__,
                                             'excluded', list))

    def set_sql_related_value(self, instance, credentials, item) -> None:
        """Sets sql related value"""
        credentials.__dict__.update({item: self.transform_text(instance.__dict__.get(item))})

    @staticmethod
    def transform_text(widget):
        """Transforms text from widget to appropriate form"""
        text = widget.text()
        if ',' in text:
            text = text.split(',')
            if '' in text:
                text.remove('')
        return text

    def set_check_boxes_variables(self) -> None:
        """Connects check_boxes with appropriate variables in
        sql_variables/default_variables object"""
        check_boxes = self.ui_elements.checkboxes
        store = self.variables.default_values.checks_customization
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
        radio_buttons.get('day-sum').clicked.connect(self.get_radio_button_value)
        self.logger.debug('day-sum radio_button successfully connected with mode')
        radio_buttons.get('section-sum').clicked.connect(self.get_radio_button_value)
        self.logger.debug('section-sum radio_button successfully connected with mode')
        radio_buttons.get('detailed').clicked.connect(self.get_radio_button_value)
        self.logger.debug('detailed radio_button successfully connected with mode')

    def prepare_radio_buttons_mapping(self) -> List:
        """Returns mapping for radio buttons"""
        result = []
        radio_buttons = self.ui_elements.radio_buttons
        for key in ['day-sum', 'section-sum', 'detailed']:
            result.append((radio_buttons.get(key), self.variables.default_values.__dict__, key))
        return result

    def get_radio_button_value(self) -> None:
        """Connects radio_buttons with internal variables"""
        radio_buttons = self.ui_elements.radio_buttons
        for item in radio_buttons:
            widget = radio_buttons.get(item)
            if widget.isChecked():
                if widget.text() == "Day summary":
                    self.variables.default_values.mode = 'day-sum'
                elif widget.text() == "Section summary":
                    self.variables.default_values.mode = 'section-sum'
                else:
                    self.variables.default_values.mode = 'detailed'

    def load_from_internal(self):
        """Loads values from internal objects to ui elements"""
        self.load_line_edits()
        self.load_check_boxes()
        self.load_radio_buttons()

    def load_line_edits(self):
        """Loads values from internal objects to line edits"""
        self.load_sql_line_edits('prod')
        self.load_sql_line_edits('test')
        self.load_another_line_edits()

    def load_sql_line_edits(self, instance_type):
        """Loads values from internal objects to sql-related ui line edits"""
        creds = self.variables.sql_variables.__dict__.get(instance_type).credentials
        instance_line_edits = self.ui_elements.line_edits.__dict__.get(instance_type)
        instance_labels = self.ui_elements.labels.__dict__.get(instance_type)
        instance_line_edits.host.setText(creds.host)
        instance_line_edits.user.setText(creds.user)
        instance_line_edits.password.setText(creds.password)
        instance_line_edits.base.setText(creds.base)
        if creds.base:
            instance_line_edits.base.show()
            instance_labels.base.show()
        else:
            instance_line_edits.base.hide()
            instance_labels.base.hide()

    def load_another_line_edits(self):
        """Loads values from internal objects to ui line edits"""
        included_tables = self.variables.sql_variables.tables.included
        self.ui_elements.line_edits.included_tables.setText(','.join(included_tables))
        send_mail_to = self.variables.default_values.send_mail_to
        self.ui_elements.line_edits.send_mail_to.setText(send_mail_to)
        excluded_tables = self.variables.sql_variables.tables.excluded
        common_excluded_tables = excluded_tables.copy()
        hard_excluded = self.variables.sql_variables.tables.hard_excluded
        common_excluded_tables.update(hard_excluded)
        self.ui_elements.line_edits.excluded_tables.setText(','.join(common_excluded_tables))
        excluded_columns = self.variables.sql_variables.columns.excluded
        self.ui_elements.line_edits.excluded_columns.setText(','.join(excluded_columns))

    def load_check_boxes(self):
        """Loads checkboxes state from internal object"""
        check_boxes = self.ui_elements.checkboxes
        store = self.variables.default_values.checks_customization
        for key in check_boxes.keys():
            check_boxes.get(key).setChecked(store.get(key))

    def load_radio_buttons(self):
        """Loads checkboxes state from internal object"""
        mode = self.variables.default_values.mode
        radio_buttons = self.ui_elements.radio_buttons
        for item in radio_buttons:
            if mode == item:
                radio_buttons.get(item).setChecked(True)
            else:
                radio_buttons.get(item).setChecked(False)

    def disable_exclude(self) -> None:
        """Disables excluded_table in case of included_tables is not empty"""
        if self.ui_elements.line_edits.included_tables.text():
            self.ui_elements.line_edits.excluded_tables.setEnabled(False)
        else:
            self.ui_elements.line_edits.excluded_tables.setEnabled(True)


def set_value(widget, store, key, value_type) -> None:
    """Sets value from widget to some variable"""
    value = Configuration.transform_text(widget)
    if isinstance(value_type, list):
        store.update({key: list(value)})
    elif isinstance(value_type, str):
        store.update({key: str(value)})
    elif isinstance(value_type, int):
        store.update({key: int(value)})

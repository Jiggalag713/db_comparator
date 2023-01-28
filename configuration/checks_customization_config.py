"""Module intended to store class for storing variables related to
tuning of comparing"""


class ChecksConfig:
    """Class implemented to store state of and radio_buttons"""
    def __init__(self):
        self.check_schema: bool = True
        self.fail_fast: bool = False
        self.check_reports: bool = True
        self.check_entities: bool = True
        self.use_dataframes: bool = True
        self.report_check_type: str = 'detailed'

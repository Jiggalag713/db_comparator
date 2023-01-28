class Info:
    def __init__(self, logger):
        self.logger = logger
        self.tables = set()
        self.excluded_tables = set()  # TODO: already in SqlVariables
        self.prod_list = set()  # TODO: already in SqlAlchemyHelper
        self.test_list = set()  # TODO: already in SqlAlchemyHelper
        self.prod_uniq_tables = []
        self.test_uniq_tables = []
        self.prod_empty = set()
        self.test_empty = set()
        self.empty = []
        self.no_crossed_tables = []
        self.diff_schema = []
        self.diff_data = []
        self.compared_tables = []
        self.prod_uniq_columns = {}
        self.test_uniq_columns = {}

    def update_table_list(self, stage, value):
        if stage == "prod":
            self.prod_list.update(value)
        elif stage == "test":
            self.test_list.update(value)
        else:
            self.logger.error(f"There is no such stage {stage}")

    def update_empty(self, stage, value):
        if stage == "prod":
            self.prod_empty.update(value)
        elif stage == "test":
            self.test_empty.update(value)
        else:
            self.logger.error(f"There is no such stage {stage}")

    # TODO: check this useless method
    def update_diff_schema(self, value):
        self.diff_schema.append(value)

    def update_diff_data(self, value):
        self.diff_data.append(value)

    def get_uniq_tables(self, stage):
        if stage == "prod":
            self.prod_uniq_tables = self.prod_list - self.test_list
            return self.prod_uniq_tables
        elif stage == "test":
            self.test_uniq_tables = self.test_list - self.prod_list
            return self.test_uniq_tables
        else:
            self.logger.error(f"There is no such stage {stage}")

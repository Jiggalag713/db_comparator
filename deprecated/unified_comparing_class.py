import process_dates
import query_constructor
import query_list_iterator
from helpers import converters
from deprecated import sql_helper


class Comparation:
    def __init__(self, prod_connect, test_connect, table, logger, cmp_params):
        self.prod_sql_connection = prod_connect
        self.test_sql_connection = test_connect
        self.prod_engine = prod_connect.engine
        self.test_engine = test_connect.engine
        self.table = table
        self.cmp_params = cmp_params
        self.depth_report_check = self.cmp_params.get('depth_report_check')
        self.mode = self.cmp_params.get('mode')
        self.logger = logger

    def compare_table(self, is_report, mapping, start_time, comparing_info, comparing_step):
        if is_report:
            proc_dates = process_dates.ProcessDates(self.prod_engine, self.test_engine, self.table,
                                                    self.depth_report_check, self.logger)
            dates = converters.convert_to_list(proc_dates.compare_dates(comparing_info))
            dates.sort()
            if dates:
                local_break, max_amount = self.check_amount(dates)
                self.logger.info(f'Will be checked dates {dates}')
                # alchemy_object = self.prod_sql_connection.set_keyvalues(**self.cmp_params)
                query_list = query_constructor.InitializeQuery(alchemy_object, mapping, self.table, comparing_step,
                                                               self.logger).report(dates, self.mode, max_amount)
            else:
                self.logger.warn('There is not any common dates for comparing')
                query_list = []
        else:
            local_break, max_amount = self.check_amount(None)
            alchemy_object = self.prod_sql_connection.set_keyvalues(
                **self.cmp_params)  # TODO: AttributeError: 'DbAlchemyHelper' object has no attribute 'set_keyvalue'
            query_list = query_constructor.InitializeQuery(alchemy_object, mapping, self.table, comparing_step,
                                                           self.logger).entity(max_amount)
        if query_list:
            query_iterator = query_list_iterator.Iterator(self.prod_engine, self.test_engine,
                                                          self.table, self.logger, self.cmp_params)
            global_break, local_break = query_iterator.iterate_by_query_list(query_list, start_time, comparing_info,
                                                                             self.cmp_params.get('service_dir'))
            return global_break
        else:
            return False

    def check_amount(self, dates):
        prod_record_amount, test_record_amount = sql_helper.get_amount_records(self.table, dates,
                                                                               [self.prod_engine, self.test_engine])
        if prod_record_amount == 0 and test_record_amount == 0:
            self.logger.warn(f"Table {self.table} is empty on both servers!")
            return True, 0
        if prod_record_amount == 0:
            self.logger.warn(f"Table {self.table} is empty on prod-server!")
            return True, 0
        if test_record_amount == 0:
            self.logger.warn(f"Table {self.table} is empty on test-server!")
            return True, 0
        if prod_record_amount != test_record_amount:
            sub_result, instance_type, percents = self.subtract(prod_record_amount, test_record_amount)
            if instance_type == 'Prod':
                base = self.prod_engine.url.database
            else:
                base = self.test_engine.url.database
            self.logger.warn((f'Amount of records differs for table {self.table}. '
                              f'Prod record amount: {prod_record_amount}. '
                              f'Test record amount: {test_record_amount}.'))
            self.logger.warn((f'Db {base} have more records. '
                              f'Difference equals {sub_result}, {percents:.5f}%'))
        max_amount = max(prod_record_amount, test_record_amount)
        return False, max_amount

    @staticmethod
    def subtract(prod_amount, test_amount):
        if prod_amount > test_amount:
            subtraction = prod_amount - test_amount
            instance_type = 'Prod'
            percents = subtraction / prod_amount * 100
        else:
            subtraction = test_amount - prod_amount
            instance_type = 'Test'
            percents = subtraction / test_amount * 100
        return subtraction, instance_type, percents

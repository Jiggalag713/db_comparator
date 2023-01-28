import datetime

import pandas as pd

import process_uniqs
from deprecated import sql_helper


class Iterator:
    def __init__(self, prod_engine, test_engine, table, logger, cmp_params):
        self.prod_engine = prod_engine
        self.test_engine = test_engine
        self.table = table
        self.cmp_params = cmp_params
        self.strings_amount = cmp_params.get('strings_amount')
        self.fail_with_first_error = cmp_params.get('fail_with_first_error')
        self.table_timeout = cmp_params.get('table_timeout')
        self.table_start_time = datetime.datetime.now()
        self.logger = logger

    # TODO: probably need to remove, because there's no reason to iterate with query list
    def iterate_by_query_list(self, query_list, start_time, comparing_info, service_dir):
        prod_uniq = set()
        test_uniq = set()
        for query in query_list:
            percent = (query_list.index(query) / len(query_list)) * 100
            self.logger.info(f'Progress for table {self.table} {percent:.2f}%')
            local_break, prod_tmp_uniq, test_tmp_uniq = self.get_differences(query, comparing_info, self.strings_amount,
                                                                             service_dir)
            prod_uniq = process_uniqs.merge_uniqs(prod_uniq, prod_tmp_uniq)
            test_uniq = process_uniqs.merge_uniqs(test_uniq, test_tmp_uniq)
            if prod_uniq and test_uniq:
                prod_uniq = process_uniqs.thin_uniq_list(prod_uniq, test_uniq, self.logger)
                test_uniq = process_uniqs.thin_uniq_list(test_uniq, prod_uniq, self.logger)
            if local_break:
                if all([prod_uniq, test_uniq]):
                    process_uniqs.dump_uniqs(prod_uniq, test_uniq, self.table, query_list[0], service_dir, self.logger)
                return False, True
            if self.table_timeout is not None:
                if self.is_timeouted(prod_uniq, test_uniq, query, service_dir):
                    return False, True

            if self.fail_with_first_error:
                self.logger.info(f"First error founded, checking failed. Comparing takes "
                                 f"{datetime.datetime.now() - start_time}")
                if all([prod_uniq, test_uniq]):
                    process_uniqs.dump_uniqs(prod_uniq, test_uniq, self.table, query_list[0], service_dir, self.logger)
                return True, False

            if process_uniqs.check_uniqs(prod_uniq, test_uniq, self.strings_amount, self.table, query, service_dir,
                                         self.logger):
                return False, True
        if all([prod_uniq, test_uniq]):
            process_uniqs.dump_uniqs(prod_uniq, test_uniq, self.table, query_list[0], service_dir, self.logger)
        return False, False

    def is_timeouted(self, prod_uniq, test_uniq, query, service_dir):
        duration = datetime.datetime.now() - self.table_start_time
        if duration > datetime.timedelta(minutes=self.table_timeout):
            self.logger.error(f'Checking table {self.table} exceded timeout {self.table_timeout}. Finished')
            process_uniqs.check_uniqs(prod_uniq, test_uniq, self.strings_amount, self.table, query, service_dir,
                                      self.logger)

    def drop_hided_columns(self, df):
        for column in self.cmp_params.get('hide_columns'):
            if column in df.columns.values:
                df.drop(column, 1)

    # TODO: this method inconsistent now, should be refactored asap
    def get_differences(self, query, comparing_info, strings_amount, service_dir):
        prod_df = pd.read_sql_query(query, self.prod_engine)
        # prod_df['new'] = pd.insert
        test_df = pd.read_sql_query(query, self.test_engine)
        self.drop_hided_columns(prod_df)
        self.drop_hided_columns(test_df)
        # TODO: here insert method which drop hided columns from dataframes
        prod_entities, test_entities = sql_helper.get_comparable_objects([self.prod_engine,
                                                                          self.test_engine], query)
        if (prod_entities is None) or (test_entities is None):
            self.logger.warn(f'Table {self.table} skipped because something going bad')
            return False, set(), set()
        prod_uniq = set(prod_entities) - set(test_entities)
        test_uniq = set(test_entities) - set(prod_entities)
        if all([prod_uniq, test_uniq]):
            self.logger.error(f"Tables {self.table} differs!")
            comparing_info.update_diff_data(self.table)
            if max(len(prod_uniq), len(test_uniq)) >= strings_amount:
                local_break = True
            else:
                local_break = False
            if process_uniqs.check_uniqs(prod_uniq, test_uniq, strings_amount, self.table, query, service_dir,
                                         self.logger):
                return local_break, set(), set()
            else:
                return local_break, prod_uniq, test_uniq
        else:
            return True, set(), set()

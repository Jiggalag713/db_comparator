import datetime

from helpers import converters
from deprecated import sql_helper


class ProcessDates:
    def __init__(self, prod_connection, test_connection, table, depth_report_check, logger):
        self.prod_connection = prod_connection
        self.test_connection = test_connection
        self.table = table
        self.depth_report_check = depth_report_check
        self.logger = logger

    def compare_dates(self, comparing_info):
        select_query = f"SELECT distinct(`dt`) from {self.table};"
        prod_dates, test_dates = sql_helper.get_comparable_objects([self.prod_connection,
                                                                          self.test_connection],
                                                                         select_query)
        if (prod_dates is None) or (test_dates is None):
            self.logger.warn(f"Table {self.table} skipped because something going bad")
            return []
        if not prod_dates.empty and not test_dates.empty:
            return self.calculate_comparing_timeframe(prod_dates, test_dates)
        else:
            if prod_dates.empty and test_dates.empty:
                self.logger.warn(f"Table {self.table} is empty in both dbs...")
                comparing_info.empty.append(self.table)
            elif prod_dates.empty:
                self.logger.warn(f"Table {self.table} on "
                                 f"{self.prod_connection.url.database} is empty!")
                comparing_info.update_empty("prod", self.table)
            else:
                self.logger.warn(f"Table {self.table} on "
                                 f"{self.test_connection.url.database} is empty!")
                comparing_info.update_empty("test", self.table)
            return []

    def calculate_comparing_timeframe(self, prod_dates, test_dates):
        actual_dates = set()
        days = self.depth_report_check
        for day in range(1, days):
            actual_dates.add(calculate_date(day))
        if prod_dates.tail(days).equals(test_dates.tail(days)):
            return self.get_comparing_timeframe(prod_dates)
        else:
            return self.get_timeframe_intersection(prod_dates, test_dates)

    def get_comparing_timeframe(self, prod_dates):
        comparing_timeframe = []
        for item in prod_dates.tail(self.depth_report_check).iterrows():
            # TODO: item[1][0] it is ugly nasty hack, should be removed asap
            comparing_timeframe.append(item[1][0].date().strftime("%Y-%m-%d"))
        return comparing_timeframe

    # TODO: method not works, should be debugged!
    def get_timeframe_intersection(self, prod_dates, test_dates):
        prod_set = set(prod_dates)
        test_set = set(test_dates)
        if prod_set - test_set:
            prod_unique_dates = get_unique_dates(prod_set, test_set)
            dates_string = ",".join(prod_unique_dates)
            self.logger.warn(f"This dates absent in {self.test_connection.url.database}: " +
                             f"{dates_string} in report table {self.table}...")
        if test_set - prod_set:
            unique_dates = get_unique_dates(test_set, prod_set)
            test_unique_dates = ",".join(unique_dates)
            self.logger.warn(f"This dates absent in {self.prod_connection.url.database}: " +
                             f"{test_unique_dates} in report table {self.table}...")
        result_dates = list(prod_set & test_set)
        result_dates.sort()
        return result_dates[-self.depth_report_check:]


def calculate_date(days):
    dateformat = "%Y-%m-%d %H:%M:%S"
    current_date = datetime.datetime.today().date()
    return (current_date - datetime.timedelta(days=days)).strftime(dateformat)


def get_unique_dates(first_date_list, second_date_list):
    unique_dates = []
    for item in converters.convert_to_list(first_date_list - second_date_list):
        unique_dates.append(item.strftime("%Y-%m-%d %H:%M:%S"))
    return unique_dates

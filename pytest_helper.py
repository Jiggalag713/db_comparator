"""Module intended for storing useful test functions"""


def get_error_text(actual, expected):
    """Constructs error message, displayed in case of assertion error"""
    return f'AR is {actual} ' \
           f'ER is {expected}'


def result_dict(variables):
    """Returns result dictionary for tests"""
    default_values = variables.default_values
    system_values = variables.system_config
    sql_variables = variables.sql_variables
    return {'check_entities': default_values.checks_customization.get('check_entities'),
            'check_reports': default_values.checks_customization.get('check_reports'),
            'check_schema': default_values.checks_customization.get('check_schema'),
            'comparing_step': default_values.constants.get('comparing_step'),
            'depth_report_check': default_values.constants.get('depth_report_check'),
            # 'excluded_columns': variables.sql_variables.columns.excluded,
            'excluded': sql_variables.tables.excluded,
            'fail_fast': default_values.checks_customization.get('fail_fast'),
            'included': sql_variables.tables.included,
            'logging_level': system_values.logging_level,
            'path_to_logs': system_values.path_to_logs,
            'prod.base': sql_variables.prod.credentials.base,
            'prod.host': sql_variables.prod.credentials.host,
            'prod.port': sql_variables.prod.credentials.port,
            'prod.password': sql_variables.prod.credentials.password,
            'prod.user': sql_variables.prod.credentials.user,
            'report_check_type': default_values.mode,
            'retry_attempts': default_values.constants.get('retry_attempts'),
            'schema_columns': default_values.selected_schema_columns,
            'service_dir': system_values.directories.service_dir,
            'strings_amount': default_values.constants.get('strings_amount'),
            'table_timeout': default_values.constants.get('table_timeout'),
            'test.base': sql_variables.test.credentials.base,
            'test.host': sql_variables.test.credentials.host,
            'test.port': sql_variables.test.credentials.port,
            'test.password': sql_variables.test.credentials.password,
            'test.user': sql_variables.test.credentials.user,
            'result_dir': system_values.directories.result_dir}


def customization_checks(variables):
    """Returns dictionary of customization checks"""
    result = {}
    result.update({'check_entities': result_dict(variables).get('check_entities')})
    result.update({'check_reports': result_dict(variables).get('check_reports')})
    result.update({'check_schema': result_dict(variables).get('check_schema')})
    result.update({'fail_fast': result_dict(variables).get('fail_fast')})
    result.update({'report_check_type': result_dict(variables).get('report_check_type')})
    return result

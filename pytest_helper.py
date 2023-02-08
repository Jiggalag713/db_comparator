def get_error_text(actual, expected):
    return f'AR is {actual} ' \
           f'ER is {expected}'


def result_dict(variables):
    default_values = variables.default_values
    system_values = variables.system_config
    sql_variables = variables.sql_variables
    return {'check_entities': default_values.checks_customization.get('check_entities'),
            'check_reports': default_values.checks_customization.get('check_reports'),
            'check_schema': default_values.checks_customization.get('check_schema'),
            'comparing_step': default_values.constants.get('comparing_step'),
            'depth_report_check': default_values.constants.get('depth_report_check'),
            'excluded_columns': variables.sql_variables.inc_exc.excluded_columns,
            'excluded_tables': sql_variables.inc_exc.excluded_tables,
            'fail_fast': default_values.checks_customization.get('fail_fast'),
            'included_tables': sql_variables.inc_exc.included_tables,
            'logging_level': system_values.logging_level,
            'path_to_logs': system_values.path_to_logs,
            'prod.base': sql_variables.prod.credentials.base,
            'prod.host': sql_variables.prod.credentials.host,
            'prod.password': sql_variables.prod.credentials.password,
            'prod.user': sql_variables.prod.credentials.user,
            'report_check_type': default_values.mode,
            'retry_attempts': default_values.constants.get('retry_attempts'),
            'schema_columns': default_values.schema_columns,
            'service_dir': system_values.service_dir,
            'strings_amount': default_values.constants.get('strings_amount'),
            'table_timeout': default_values.constants.get('table_timeout'),
            'test.base': sql_variables.test.credentials.base,
            'test.host': sql_variables.test.credentials.host,
            'test.password': sql_variables.test.credentials.password,
            'test.user': sql_variables.test.credentials.user,
            'test_dir': system_values.test_dir,
            'use_dataframes': variables.default_values.checks_customization.get('use_dataframes')}


def customization_checks(variables):
    result = {}
    result.update({'check_entities': result_dict(variables).get('check_entities')})
    result.update({'check_reports': result_dict(variables).get('check_reports')})
    result.update({'check_schema': result_dict(variables).get('check_schema')})
    result.update({'fail_fast': result_dict(variables).get('fail_fast')})
    result.update({'use_dataframes': result_dict(variables).get('use_dataframes')})
    result.update({'report_check_type': result_dict(variables).get('report_check_type')})
    return result

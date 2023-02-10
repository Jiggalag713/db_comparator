"""Module for pytest fixtures"""
import pytest

from configuration.variables import Variables


@pytest.fixture(scope='session')
def default_variables():
    """Returns default Variables class instance"""
    return Variables()


@pytest.fixture(scope='session')
def variables():
    """Returns filled Variable class instance"""
    inst = Variables()
    inst.default_values.checks_customization.update({'check_entities': False})
    inst.default_values.checks_customization.update({'check_reports': False})
    inst.default_values.checks_customization.update({'check_schema': False})
    inst.default_values.constants.update({'comparing_step': 713})
    inst.default_values.constants.update({'depth_report_check': 713})
    inst.sql_variables.columns.excluded = ['excluded', 'columns', '713']
    inst.sql_variables.tables.excluded = ['excluded', 'tables', '713']
    inst.default_values.checks_customization.update({'fail_fast': False})
    inst.sql_variables.tables.included = ['included', 'tables', '713']
    inst.system_config.logging_level = 50
    inst.system_config.path_to_logs = '/my/perfect/test/path'
    inst.sql_variables.prod.credentials.host = '127.0.0.1'
    inst.sql_variables.prod.credentials.user = 'testuser'
    inst.sql_variables.prod.credentials.password = 'testpassword'
    inst.sql_variables.prod.credentials.base = 'test_db'
    inst.default_values.mode = 'section_summary'
    inst.default_values.constants.update({'retry_attempts': 713})
    inst.default_values.selected_schema_columns = ['my', 'perfect', 'schema', 'columns']
    inst.system_config.service_dir = '/my/perfect/service/dir'
    inst.default_values.constants.update({'strings_amount': 713})
    inst.default_values.constants.update({'table_timeout': 713})
    inst.sql_variables.test.credentials.host = '127.0.0.2'
    inst.sql_variables.test.credentials.user = 'testuser1'
    inst.sql_variables.test.credentials.password = 'testpassword1'
    inst.sql_variables.test.credentials.base = 'test_db1'
    inst.system_config.test_dir = '/my/perfect/test/dir'
    inst.default_values.checks_customization.update({'use_dataframes': False})
    return inst

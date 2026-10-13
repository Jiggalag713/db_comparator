"""Module contains tests for config_serialization"""
from pytest_helper import customization_checks, get_error_text, result_dict
from ui_logic import config_serialization


def test_default_save_configuration(default_variables):
    """test_default_save_configuration"""
    actual = config_serialization.save_configuration(default_variables)
    expected = result_dict(default_variables)
    assert actual == expected, get_error_text(actual, expected)


def test_save_configuration(variables):
    """test_save_configuration"""
    actual = config_serialization.save_configuration(variables)
    expected = result_dict(variables)
    assert actual == expected, get_error_text(actual, expected)


def test_serialize_check_customization_state(variables):
    """test_serialize_check_customization_state"""
    actual = config_serialization.serialize_check_customization_state(variables.default_values)
    expected = customization_checks(variables)
    assert actual == expected, get_error_text(actual, expected)


def test_prod_host_properties_to_json(variables):
    """test_prod_host_properties_to_json"""
    actual = config_serialization.host_properties_to_json('prod', variables.sql_variables)
    raw = result_dict(variables)
    expected = {
        'prod.host': raw.get('prod.host'),
        'prod.port': raw.get('prod.port'),
        'prod.user': raw.get('prod.user'),
        'prod.password': raw.get('prod.password'),
        'prod.base': raw.get('prod.base'),
    }
    assert actual == expected, get_error_text(actual, expected)


def test_test_host_properties_to_json(variables):
    """test_test_host_properties_to_json"""
    actual = config_serialization.host_properties_to_json('test', variables.sql_variables)
    raw = result_dict(variables)
    expected = {
        'test.host': raw.get('test.host'),
        'test.port': raw.get('test.port'),
        'test.user': raw.get('test.user'),
        'test.password': raw.get('test.password'),
        'test.base': raw.get('test.base'),
    }
    assert actual == expected, get_error_text(actual, expected)


def test_system_variables_to_json(variables):
    """test_system_variables_to_json"""
    actual = config_serialization.system_variables_to_json(variables.system_config)
    raw = result_dict(variables)
    expected = {
        'logging_level': raw.get('logging_level'),
        'path_to_logs': raw.get('path_to_logs'),
        'service_dir': raw.get('service_dir'),
        'result_dir': raw.get('result_dir')
    }
    assert actual == expected, get_error_text(actual, expected)


def test_variables_to_json(variables):
    """test_variables_to_json"""
    actual = config_serialization.variables_to_json(variables)
    raw = result_dict(variables)
    expected = config_serialization.system_variables_to_json(variables.system_config)
    expected.update({
        'comparing_step': raw.get('comparing_step'),
        'depth_report_check': raw.get('depth_report_check'),
        'retry_attempts': raw.get('retry_attempts'),
        'strings_amount': raw.get('strings_amount'),
        'table_timeout': raw.get('table_timeout'),
        'schema_columns': raw.get('schema_columns')
    })
    assert actual == expected, get_error_text(actual, expected)


def test_deserialize_config(variables):
    """test_deserialize_config"""
    expected = config_serialization.save_configuration(variables)
    config_serialization.deserialize_config(variables, expected)
    actual = config_serialization.save_configuration(variables)
    assert actual == expected, get_error_text(actual, expected)

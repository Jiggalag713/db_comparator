"""Module contains class implemented serialization of application configuration"""
from typing import Dict

from configuration.default_variables import DefaultValues
from configuration.sql_variables import SqlVariables
from configuration.system_config import SystemConfig
from configuration.variables import Variables
from helpers.sql_helper import SqlAlchemyHelper


def save_configuration(variables: Variables) -> Dict:
    """Method implements serialization of current application configuration
    to file"""
    config = {}
    sql_variables: SqlVariables = variables.sql_variables
    for key in sql_variables.__dict__:
        if key in ['prod', 'test']:
            config.update(host_properties_to_json(key, sql_variables))
    for key in sql_variables.tables.__dict__:
        if key in ['included', 'excluded']:
            value = sql_variables.tables.__dict__.get(key)
            if isinstance(value, dict):
                if '' in value:
                    value.pop('')
                config.update({key: value})
    for key in sql_variables.columns.__dict__:
        if key in ['excluded']:
            value = sql_variables.tables.__dict__.get(key)
            if isinstance(value, list):
                if '' in value:
                    value.remove('')
                config.update({key: value})
    config.update(variables_to_json(variables))
    config.update(serialize_check_customization_state(variables.default_values))
    return config


def serialize_check_customization_state(default_values: DefaultValues) -> Dict:
    """Method intended for state serialization of main window check_boxes"""
    checks = default_values.checks_customization
    return {
        'check_entities': checks.get('check_entities'),
        'check_reports': checks.get('check_reports'),
        'check_schema': checks.get('check_schema'),
        'fail_fast': checks.get('fail_fast'),
        'report_check_type': default_values.mode
    }


def host_properties_to_json(instance_type: str, instance: SqlVariables) -> Dict:
    """Method intended for serializing part of SqlAlchemyHelper instance
    to config file"""
    example = instance.__dict__.get(instance_type)
    if isinstance(example, SqlAlchemyHelper):
        return {
            f'{instance_type}.host': example.credentials.host,
            f'{instance_type}.port': example.credentials.port,
            f'{instance_type}.user': example.credentials.user,
            f'{instance_type}.password': example.credentials.password,
            f'{instance_type}.base': example.credentials.base
        }
    return {
        f'{instance_type}.host': '',
        f'{instance_type}.user': '',
        f'{instance_type}.password': '',
        f'{instance_type}.base': ''
    }


def system_variables_to_json(system_config: SystemConfig) -> Dict:
    """Method intended to serialization system variables to config file"""
    return {
        'logging_level': system_config.logging_level,
        'path_to_logs': system_config.path_to_logs,
        'service_dir': system_config.directories.service_dir,
        'result_dir': system_config.directories.result_dir
    }


def variables_to_json(variables: Variables) -> Dict:
    """Method intended to serialization of all other variables to config file"""
    system_config = variables.__dict__.get('system_config')
    if isinstance(system_config, SystemConfig):
        property_dict: Dict = system_variables_to_json(system_config)
        default_values = variables.default_values
        property_dict.update({
            'comparing_step': default_values.constants.get('comparing_step'),
            'depth_report_check': default_values.constants.get('depth_report_check'),
            'retry_attempts': default_values.constants.get('retry_attempts'),
            'strings_amount': default_values.constants.get('strings_amount'),
            'table_timeout': default_values.constants.get('table_timeout'),
            'schema_columns': default_values.selected_schema_columns
        })
        return property_dict
    return {}


def deserialize_config(variables, config: Dict) -> None:
    """Loads variables from config to UI variables"""
    default_values = variables.default_values
    sql_variables = variables.sql_variables
    for key in config:
        value = config.get(key)
        if value:
            lineedit_mapping = {
                'prod.host': sql_variables,
                'prod.port': sql_variables,
                'prod.user': sql_variables,
                'prod.password': sql_variables,
                'prod.base': sql_variables,
                'test.host': sql_variables,
                'test.port': sql_variables,
                'test.user': sql_variables,
                'test.password': sql_variables,
                'test.base': sql_variables,
                'included_tables': sql_variables.tables,
                'excluded_tables': sql_variables.tables,
                'excluded_columns': sql_variables.tables
            }
            checkbox_mapping = {
                'check_schema': default_values.checks_customization,
                'fail_fast': default_values.checks_customization,
                'check_reports': default_values.checks_customization,
                'check_entities': default_values.checks_customization
            }
            values = {
                'comparing_step': default_values.constants,
                'depth_report_check': default_values.constants,
                'retry_attempts': default_values.constants,
                'path_to_logs': default_values.constants,
                'table_timeout': default_values.constants
            }
            if key in lineedit_mapping:
                proc_lineedit_mapping(lineedit_mapping, key, value)
            elif key in checkbox_mapping:
                check_box_pack = checkbox_mapping.get(key)
                if isinstance(check_box_pack, dict):
                    check_box_pack.update({key: value})
            elif key in values:
                constants = values.get(key)
                if isinstance(constants, dict):
                    constants.update({key: value})
            elif key == 'logging_level':
                system_config = variables.system_config
                system_config.logging_level = value
                variables.logger.setLevel(value)
            elif 'schema_columns' in key:
                default_values.selected_schema_columns = value
            elif 'mode' in key:
                default_values.mode = value


def proc_lineedit_mapping(lineedit_mapping, key, value):
    """Process key if it in lineedit_mapping keys"""
    if '.' in key:
        first = key.split('.')[0]
        second = key.split('.')[1]
        instance_type = lineedit_mapping.get(key).__dict__.get(first)
        if isinstance(instance_type, SqlAlchemyHelper):
            creds = instance_type.credentials
            creds.__dict__.update({second: value})
    else:
        lineedit_mapping.get(key).__dict__.update({key: value})

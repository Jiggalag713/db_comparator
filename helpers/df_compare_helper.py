"""Module contains not worked implementation of comparing using dataframes"""
import numpy as np
import pandas as pd  # type: ignore


def get_table_schema_dataframe(instance_type, table, engine):
    """Returns dataframe red from sql"""
    query = f"select * from information_schema.columns " \
            f"where table_schema='{instance_type}' and " \
            f"table_name='{table}';"
    return pd.read_sql(query, engine)


def get_metadata_dataframe_diff(prod_instance, test_instance, table, logger):
    """Method implements comparing of two tables schemas using dataframes"""
    prod_schema = get_table_schema_dataframe('prod', table, prod_instance.engine)
    test_schema = get_table_schema_dataframe('test', table, test_instance.engine)
    result = get_dataframes_diff(prod_schema, test_schema, logger)
    return result
    # df_all = pd.concat([prod_columns.set_index('id'), test_columns.set_index('id')],
    # axis='columns', keys=['First', 'Second'])
    # if not any([prod_uniq, test_uniq]):
    #     prod_columns.fillna(value=np.nan, inplace=True)
    #     prod_columns = prod_columns.fillna(0)
    #     test_columns.fillna(value=np.nan, inplace=True)
    #     result_dataframe = pd.DataFrame([False])
    #     try:
    #         result_dataframe = (prod_columns == test_columns)
    #     except ValueError as exception:
    #         logger.warn(exception)
    #     if all(result_dataframe):
    #         return pd.DataFrame()
    #     df_all = pd.concat([prod_columns, test_columns],
    #                        axis='columns', keys=['First', 'Second'])
    #     df_final = df_all.swaplevel(axis='columns')[prod_columns.columns[1:]]
    #     df_final[(prod_columns != test_columns).any(1)].style.apply(highlight_diff, axis=None)
    #     return df_final
    # if prod_uniq:
    #     return pd.DataFrame(list(prod_uniq))
    # return pd.DataFrame(list(test_uniq))


def get_dataframes_diff(prod_columns, test_columns, logger):
    """Method implements comparing data of two tables using dataframes"""
    # df_all = pd.concat([prod_columns.set_index('id'), test_columns.set_index('id')],
    # axis='columns', keys=['First', 'Second'])
    # prod_columns.fillna(value=np.nan, inplace=True)
    # prod_columns = prod_columns.fillna(0)
    # test_columns.fillna(value=np.nan, inplace=True)
    # test_columns = test_columns.fillna(0)
    result_dataframe = prod_columns.compare(test_columns)
    print('stop')
    # result_dataframe = pd.DataFrame([False])
    try:
        if prod_columns == test_columns:
            result_dataframe = True
    except ValueError as exception:
        logger.warn(exception)
    if all(result_dataframe):
        return pd.DataFrame()
    df_all = pd.concat([prod_columns, test_columns], axis='columns', keys=['First', 'Second'])
    df_final = df_all.swaplevel(axis='COLUMN_NAME')[prod_columns.columns[1:]]
    df_final[(prod_columns != test_columns).any(1)].style.apply(highlight_diff, axis=None)
    return df_final


def highlight_diff(data, color='yellow'):
    """Method intended for highlighting differences in dataframes"""
    attr = f'background-color: {color}'
    other = data.xs('First', axis='columns', level=-1)
    return pd.DataFrame(np.where(data.ne(other, level=0), attr, ''),
                        index=data.index, columns=data.columns)

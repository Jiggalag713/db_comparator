from pytest_helper import get_error_text


def test_calculate_table_list(table_calculation):
    actual = table_calculation.calculate_table_list()
    expected = {
        'second': ['one', 'two'],
        'third': ['one', 'two']
    }
    assert actual == expected, get_error_text(actual, expected)


def test_get_common_tables(table_calculation):
    actual = table_calculation.calculate_table_list()
    expected = {
        'second': ['one', 'two'],
        'third': ['one', 'two']
    }
    assert actual == expected, get_error_text(actual, expected)


def test_find_unique_tables():
    assert True


def test_calculate_includes_excludes():
    assert True


def test_unique_table_columns():
    assert True


def test_get_reason():
    assert True


def test_calculate_excluded_columns():
    assert True

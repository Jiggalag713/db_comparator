"""Module intended to store some common methods"""


def write_to_file(result, table, result_dir, logger):
    """Method intended to write results of comparison to file in HTML format"""
    result_file = f'{result_dir}{table}.html'
    if not result.empty:
        with open(result_file, "w", encoding="utf-8") as file:
            file.write(result.to_html())
            logger.error(f"Comparing of tables {table} failed, tables differs...")
            logger.debug(f'Results saved to file {result_file}')
        return True
    return False

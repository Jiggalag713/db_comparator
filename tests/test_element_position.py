"""Module intended to store tests of element_position.py"""
import os


def test_element_position():
    """Check if locations for some elements are same"""
    with open(f'{(os.getcwd())}/ui_elements/elements_position.py', 'r') as file:
        content = file.readlines()
        positions = {}
        errors = []
        for line in content:
            if 'addWidget' in line:
                pattern = line[line.index(',') + 2:][:-2]
                if pattern not in positions.keys():
                    positions.update({pattern: line})
                else:
                    errors.append(f'position duplicates in line: {line}\n')
    assert not errors, f'There is some errors {"".join(errors)}'

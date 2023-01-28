"""Module contains single function to converting and should be removed"""


def convert_to_list(structure_to_convert):
    """Method converts dict or list to list
    and looks like crutch"""
    result_list = []
    for item in structure_to_convert:
        if isinstance(item, dict):
            key = list(item.keys())[0]
            result_list.append(item.get(key))
        else:
            result_list.append(item)
    try:
        result_list.sort()
    except TypeError:
        print('Raised TypeError during list sorting')
    return result_list

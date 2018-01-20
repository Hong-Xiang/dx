def dict_append(target, new_item):
    if not isinstance(target, dict):
        raise TypeError(
            'Target of dict_append needs to be dict, got {}.'.format(type(target)))
    for k in target:
        target[k].append(new_item[k])


def dict_element_to_tensor(target):
    import numpy as np
    if not isinstance(target, dict):
        raise TypeError(
            'Target of dict_append needs to be dict, got {}.'.format(type(target)))
    for k in target:
        target[k] = np.array(target[k])

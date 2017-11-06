def filter_out_none_elements(dct):
    result = dict()
    for n in dct:
        if dct[n] is not None:
            result[n] = dct[n]
    return result

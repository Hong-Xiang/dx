import numpy as np


def linspace(start, stop, num=50, *, method='default', endpoint=True):
    if method == 'mid':
        num = num + 1
    xi = np.linspace(start, stop, num, endpoint)
    if method == 'mid':
        xi = (xi[1:] + xi[:-1]) / 2
    return xi


def linspace_nd(start, end, num, *, method='default', endpoint=True):
    result = [linspace(s, e, num, method=method, endpoint=endpoint)
              for s, e in zip(start, end)]
    result = np.array(result).T
    return result

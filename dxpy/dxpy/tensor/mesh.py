import numpy as np


def linspace(start, stop, num=50, *, method='default', endpoint=True):
    if method == 'mid':
        num = num + 1
    xi = np.linspace(start, stop, num, endpoint)
    if method == 'mid':
        xi = (xi[1:] + xi[:-1]) / 2
    return xi


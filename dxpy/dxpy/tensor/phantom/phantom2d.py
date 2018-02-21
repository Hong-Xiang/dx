import numpy as np
def chessboard(shape, cell_shape=None):
    from ..slice import block_slices
    result = np.zeros(shape)
    for e, s in block_slices(cell_shape, shape):
        value = (e[0] - e[1]) % 2
        result[s] = value
    return result





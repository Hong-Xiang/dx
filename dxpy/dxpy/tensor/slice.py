import numpy as np


def _infer_shapes(shape_per_block, shape_target, shape_blocks):
    if shape_blocks is None and shape_target is None:
        raise TypeError("At least one of target and shape_blocks needs to"
                        "be specified.")
    if shape_target is None:
        shape_target = tuple([sb * spb
                              for sb, spb in zip(shape_blocks, shape_per_block)])
    if shape_blocks is None:
        shape_blocks = tuple([int(np.ceil(st / spb))
                              for st, spb in zip(shape_target, shape_per_block)])
    return shape_target, shape_blocks


def block_slices(shape_per_block, shape_target=None, shape_blocks=None):
    """
    Args:
        shape_per_block: list of int, shape of block
        target_shape:
    Returns:
        iterator of blocks
    """
    from itertools import product
    result = []
    shape_target, shape_blocks = _infer_shapes(shape_per_block,
                                               shape_target, shape_blocks)
    ranges = [range(s) for s in shape_blocks]
    for e in product(*ranges):
        result.append((e, block_slice(e, shape_per_block,
                                      shape_target, shape_blocks)))
    return result


def block_slice(id_block, shape_per_block, shape_target=None, shape_blocks=None):
    shape_target, shape_blocks = _infer_shapes(shape_per_block,
                                               shape_target, shape_blocks)
    result = []
    for ib, sp, st in zip(id_block, shape_per_block, shape_target):
        imax = min([sp * (ib + 1), st])
        result.append(slice(ib * sp, imax))
    return result

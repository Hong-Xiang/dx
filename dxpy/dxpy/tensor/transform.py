import numpy as np
from typing import List, TypeVar, Tuple


def random_crop_offset(input_shape, target_shape, *, batched=False):
    max_offset = [s - t for s, t in zip(input_shape, target_shape)]
    if any(map(lambda x: x < 0, max_offset)):
        raise ValueError("Invalid input_shape {} or target_shape {}.".format(
            input_shape, target_shape))
    if not batched:
        offset = []
        for s in max_offset:
            if s == 0:
                offset.append(0)
            else:
                offset.append(np.random.randint(0, s))
        return offset
    else:
        offsets = []
        if max_offset[0] > 0:
            raise ValueError(
                "Random crop offset input_shape[0] and target_shape[0]")


def unstack_auto(tensor, *, hint: str='image'):
    pass


def unstack(tensor, axis: int=0, size: int=1, *,  squeeze: bool=True):
    """
    Unstack tensor along given axies with given sizes. 
    Args:
    - tensor: np.ndarray
    - axies: int
    - sizes: int
    - squeeze: bool, whether squeeze dim when size equals one.

    Returns:
    - List[tensor]
    """
    indices = range(0, tensor.shape[axis], size)
    splitted = np.split(tensor, indices)
    if squeeze and size == 1:
        sli = [slice(0, s) for s in tensor.shape]
        sli[axis] = 0
        splitted = [t[sli] for t in splitted]
    return splitted


def mirror(tensor, axis, *, forward: bool=True):
    tensor_m = np.flip(tensor, axis)
    if forward:
        return np.concatenate([tensor, tensor_m], axis=axis)
    else:
        return np.concatenate([tensor_m, tensor], axis=axis)


# def pad(tensor, axis: int, target_size: int, offset: int=0, method: str='constant', *, padding_value=0)
#     def padding_one_block(source, target, idx, ids, method, mirror_axis=None):
#         if method is None:
#             target[idx] = source[ids]
#         elif method.lower() == 'constant':
#             target[idx] = constant_value
#         elif method.lower() == 'period':
#             target[idx] = source[ids]
#         elif method.lower() == 'mirror':
#             ids[mirror_axis] = slice(ids[mirror_axis].stop - 1, None, -1)
#             target[idx] = source[ids]

#     def index(tensor, target_size, axis, offset):
#         ids = list()
#         idt = list()
#         for i in range(tensor.ndim):
#             if i == axis:
#                 max_idx = target_size
#                 slice_min = min([max([offset, 0]), max_idx])

#                 slice_max = min(
#                     [max([offset + tensor.shape[i], 0]), max_idx])
#             else:
#                 slice_min = 0
#                 slice_max = tensor.shape[i]
#             idt.append(slice(slice_min, slice_max))
#             ids.append(slice(0, slice_max - slice_min))
#         return idt, ids

#     def current_method(method, is_mirror):
#         if method == 'mirror':
#             if is_mirror:
#                 c_method = 'mirror'
#                 is_mirror = False
#             else:
#                 c_method = 'period'
#                 is_mirror = True
#         else:
#             c_method = method
#         return c_method, is_mirror

#     offset_start = offset
#     offset_now = offset_start
#     next_shape = list(tensor.shape)
#     next_shape[axis] = target_size
#     result = np.zeros(next_shape)
#     is_mirror = False
#     while offset_now < target_size:
#         idt, ids = index(tensor, target_size, i, offset_now)
#         c_method, is_mirror = current_method(method, is_mirror)
#         padding_one_block(tensor, result, idt, ids, c_method, axis)
#         offset_now += tensor.shape[axis]
#     is_mirror = True
#     offset_now = offset_start - tensor.shape[axis]
#     while offset_now > - tensor.shape[axis]:
#         idt, ids = index(tensor, target_size, i, offset_now)
#         c_method, is_mirror = current_method(method, is_mirror)
#         padding_one_block(tensor, result, idt, ids, c_method, axis)
#         offset_now -= tensor.shape[axis]
#     return result

# def padding()
    # TODO: add guard for tf.Tensor
    # tensor = np.array(tensor)
    # tensors = [tensor]
    # for i in range(len(axies)):
    #     tensors = [_unbatch_single_axis(t) for t in tensors]
    #     for j, v in enumerate(axies):
    #         if v > axies:
    #             axies[j] = v - 1
    # return tensors
    # if isinstance(tensor, np.ndarray):
    # return list(map(lambda x: x[0, ...], np.split(tensor, tensor.shape[0])))
#    raise TypeError("numpy.ndarray is required, got {}.".format(type(tensor)))


def batch(tensors):
    return np.array(tensors)


def maybe_unbatch(tensors: TypeVar('T', np.ndarray, List[np.ndarray])) -> List[np.ndarray]:
    if isinstance(tensors, (list, tuple)):
        return tensors
    else:
        return unbatch(tensors)


def padding(tensor: np.ndarray, target_shape: List[int], offset: TypeVar('T', int, List[int])=0, method: TypeVar('T', str, List[str])=None, *, padding_order: List[int]=None, constant_value: float=None):
    """
    Supported method:
        period: periodically padding tensor, assuming period equals to tensor shape.
        mirror: mirror reflect
        constant: pad with constant value
    """
    for i, v in enumerate(target_shape):
        if v is None:
            target_shape[i] = tensor.shape[i]
    if isinstance(offset, int):
        offset = [offset] * tensor.ndim
    if isinstance(method, str):
        method = [method] * tensor.ndim
    if padding_order is None:
        padding_order = list(range(tensor.ndim))

    def padding_one_block(source, target, idx, ids, method, mirror_axis=None):
        if method is None:
            target[idx] = source[ids]
        elif method.lower() == 'constant':
            target[idx] = constant_value
        elif method.lower() == 'period':
            target[idx] = source[ids]
        elif method.lower() == 'mirror':
            ids[mirror_axis] = slice(ids[mirror_axis].stop - 1, None, -1)
            target[idx] = source[ids]

    def index(tensor, target_size, axis, offset):
        ids = list()
        idt = list()
        for i in range(tensor.ndim):
            if i == axis:
                max_idx = target_size
                slice_min = min([max([offset, 0]), max_idx])

                slice_max = min(
                    [max([offset + tensor.shape[i], 0]), max_idx])
            else:
                slice_min = 0
                slice_max = tensor.shape[i]
            idt.append(slice(slice_min, slice_max))
            ids.append(slice(0, slice_max - slice_min))
        return idt, ids

    def current_method(method, is_mirror):
        if method == 'mirror':
            if is_mirror:
                c_method = 'mirror'
                is_mirror = False
            else:
                c_method = 'period'
                is_mirror = True
        else:
            c_method = method
        return c_method, is_mirror

    def padding_one_dim(tensor, axis, target_size, offset, method):
        offset_start = offset
        offset_now = offset_start
        next_shape = list(tensor.shape)
        next_shape[axis] = target_size
        result = np.zeros(next_shape)
        is_mirror = False
        while offset_now < target_size:
            idt, ids = index(tensor, target_size, i, offset_now)
            c_method, is_mirror = current_method(method, is_mirror)
            padding_one_block(tensor, result, idt, ids, c_method, axis)
            offset_now += tensor.shape[axis]
        is_mirror = True
        offset_now = offset_start - tensor.shape[axis]
        while offset_now > - tensor.shape[axis]:
            idt, ids = index(tensor, target_size, i, offset_now)
            c_method, is_mirror = current_method(method, is_mirror)
            padding_one_block(tensor, result, idt, ids, c_method, axis)
            offset_now -= tensor.shape[axis]
        return result
    result = np.array(tensor)
    for i in padding_order:
        if method[i] is None:
            continue
        result = padding_one_dim(
            result, i, target_shape[i], offset[i], method[i])
    return result


def rotate(tensor, offset, axis):
    slis = [slice(0, s) for s in tensor.shape]
    slil = list(slis)
    slir = list(slis)
    offset = offset % tensor.shape[axis]
    slil[axis] = slice(offset, tensor.shape[axis])
    slir[axis] = slice(0, offset)
    tl = tensor[slil]
    tr = tensor[slir]
    result = np.concatenate([tl, tr], axis=axis)
    return result


def upsample(tensor, ratio):
    import itertools
    result_shape = [r * s for r, s in zip(ratio, tensor.shape)]
    result = np.zeros(result_shape)
    ranges = [range(r) for r in ratio]
    for offsets in itertools.product(*ranges):
        slices = [slice(o, s, r)
                  for o, s, r in zip(offsets, result_shape, ratio)]
        result[slices] = tensor
    return result


def crop_to_shape(tensor: np.ndarray,
                  target_shape: TypeVar('T', List[int], Tuple[int]),
                  method=None):
    """
    method: list/tuple/str of chars:
        'c': center
        'h': half offset
        's': squeeze dim, if shape of specified dim > 1, pick first element. 
        '0': alias of 's' 
    """
    if method is None:
        method = 'c' * tensor.ndim
    method = tuple(method)
    # squeeze or pick 0
    slices = list()
    for i, m in enumerate(method):
        if m in ['s', '0']:
            slices.append(0)
        else:
            slices.append(slice(0, tensor.shape[i]))
    method = [m for m in method if m not in ['s', '0']]
    tensor = tensor[slices]
    if tensor.ndim != len(target_shape):
        raise ValueError("Invalid target_shape dimension")
    slices = list()
    for i, m in enumerate(method):
        if m == 'c':
            o = (tensor.shape[i] - target_shape[i]) // 2
            slices.append(slice(o, -o))
        elif m == 'h':
            o = tensor.shape[1] // 2
            slices.append(slice(o, o + target_shape[i]))
    return tensor[slices]

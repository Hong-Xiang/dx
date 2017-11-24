import tensorflow as tf


def random_crop(input_, target_shape, name='random_crop'):
    from dxpy.tensor.transform import random_crop_offset
    from ..tensor import ensure_tensor, shape_as_list
    with tf.name_scope(name):
        input_shape = shape_as_list(input_)
        target_shape = shape_as_list(target_shape)
        random_offset = tf.py_func(random_crop_offset,
                                   [input_shape, target_shape], tf.int64)
        return tf.slice(input_, random_offset, target_shape)


def align_crop(input_, target, offset=None, name='align_crop'):
    from ..tensor import shape_as_list
    with tf.name_scope(name):
        shape_input = shape_as_list(input_)
        shape_output = shape_as_list(target)
        if offset is None:
            offset = [0] + [(shape_input[i] - shape_output[i]) // 2
                            for i in range(1, 3)] + [0]
        return tf.slice(input_, offset, shape_output)


def boundary_crop(input_, offset, name="boundary_crop"):
    from ..tensor import shape_as_list
    with tf.name_scope(name):
        shape = shape_as_list(input_)
        if len(offset) == 2:
            offset = [0] + list(offset) + [0]
        shape_output = [s - 2 * o for s, o in zip(shape, offset)]
        return tf.slice(input_, offset, shape_output)

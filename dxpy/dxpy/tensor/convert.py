"""
Type converters for tensors
"""
import numpy as np


def rescale_to_uint16(arr):
    """
    Convert tensor to UINT16 Type while keeping maximum information.
    """
    UINT16MAX = 65535
    if isinstance(arr, np.ndarray):
        arr = np.maximum(arr, 0.0)
        arr = arr / np.max(arr) * UINT16MAX
        arr = np.minimum(arr, UINT16MAX)
        return arr.astype(np.uint32)
    else:
        import tensorflow as tf
        if isinstance(arr, tf.Tensor):
            raise NotImplementedError
        else:
            raise TypeError(
                "Requires np.yndarray or tf.Tensor, got {}.".format(type(arr)))

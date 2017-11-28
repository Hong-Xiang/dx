import numpy as np
def assert_ndim(tensor, valid_dims, tensor_name=None):
    if isinstance(valid_dims, int):
        valid_dims = [valid_dims]
    if tensor.ndim not in valid_dims:
        prefix = "Tensor {} ".format(tensor_name) if tensor is not None else "Tensor "
        msg = "{} is required to have dims in {}, got {}.".format(prefix,
                                                                  valid_dims, tensor.ndim)
        raise ValueError(msg.format())


def assert_batch_ndim(tensors, valid_dims, tensor_name=None):
    if isinstance(valid_dims, int):
        valid_dims = [valid_dims]
    if tensor.ndim not in valid_dims:
        prefix = "Tensor {} ".format(tensor_name) if tensor is not None else "Tensor "
        msg = "{} is required to have dims in {}, got {}.".format(prefix,
                                                                  valid_dims, tensor.ndim)
        raise ValueError(msg.format())

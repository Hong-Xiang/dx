import h5py
import numpy as np


def save(filename, array, tensor_spec=None):    
    from .base import TensorSpec
    if tensor_spec is None:
        tensor_spec = TensorSpec()
    with h5py.File(filename, 'w') as fout:
        return tensor_spec.create_dateset_on(fout, array)


def load(tensor_spec, slices=None):
    with h5py.File(tensor_spec.filename, 'r') as fin:
        dataset = fin
        for n in tensor_spec.dataset_names[:-1]:
            dataset = dataset[n]
        if slices is None:
            return np.array(dataset[tensor_spec.dataset_names[-1]])
        else:
            return np.array(dataset[tensor_spec.dataset_names[-1]][slices])

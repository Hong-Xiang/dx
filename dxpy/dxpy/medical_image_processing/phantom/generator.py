
import numpy as np
from dxpy.matlab import call_matlab_api


def generate_shepp_logans(nb_images, nb_size, sigma, *, backend='matlab'):
    if backend == 'matlab':
        return np.array(call_matlab_api(lambda e: e.GenerateSheppLogans(nb_images, float(nb_size), float(sigma))))
    raise ValueError("Unknown backend {}.".format(backend))


def generate_phantom(shape, *, backend='matlab'):
    if backend == 'matlab':
        return np.array(call_matlab_api(lambda eng: eng.phantom(shape)))
    raise ValueError("Unknown backend {}.".format(backend))

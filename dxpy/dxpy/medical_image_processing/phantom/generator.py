
import numpy as np
from dxpy.matlab import MatlabEngine


def _generate_shepp_logans_matlab(nb_images, nb_size, sigma):
    res = eng.GenerateSheppLogans(10, 256.0, 0.1)


def generate_shepp_logans(nb_images, nb_size, sigma, *, backend='matlab'):
    pass


def generate_phantom(*, backend='matlab'):
    if backend == 'matlab':
        if MatlabEngine.get_default_engine() is None:
            with MatlabEngine() as eng:
                result = np.array(eng.phantom())
        else:
            result = np.array(MatlabEngine.get_default_engine().phantom())
        return result
    raise ValueError("Unknown backend {}.".format(backend))

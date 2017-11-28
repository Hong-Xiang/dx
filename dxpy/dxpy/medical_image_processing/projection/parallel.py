import astra
import numpy as np


def proj(image, detector, phantom):
    shape = img.shape
    if not len(shape) == 2:
        raise ValueError('Invalid img shape {}.'.format(shape))
    vol_geom = astra.create_vol_geom(*shape)
    proj_geom = astra.create_proj_geom('parallel', sen_width, num_sen, theta)
    proj_id = astra.create_projector('cuda', proj_geom, vol_geom)
    sinogram_id, sinogram = astra.create_sino(img, proj_id)
    sinogram = np.array(sinogram)
    astra.data2d.clear()
    astra.projector.clear()
    astra.algorithm.clear()
    return sinogram

import astra
import numpy as np
from dxpy.tensor.checks import assert_ndim
from dxpy.tensor.transform import maybe_unbatch
from ..config import config
from dxpy.configs import configurable


@configurable(config['projection'])
def projection2d(image, detector, phantom, method='cuda'):
    assert_ndim(image, 2, 'image')
    vol_geom = astra.create_vol_geom(*image.shape)
    proj_geom = astra.create_proj_geom('parallel',
                                       detector.sensor_width,
                                       detector.nb_sensors,
                                       detector.views)
    proj_id = astra.create_projector(method, proj_geom, vol_geom)
    sinogram_id, sinogram = astra.create_sino(image, proj_id)
    sinogram = np.array(sinogram)
    astra.data2d.clear()
    astra.projector.clear()
    astra.algorithm.clear()
    return sinogram


# @configurable(config['projection'])
# def projection2d_batch(images, detector, phantom, method='cuda'):
#     images = maybe_unbatch(images)
#     for image in images:
#         assert_ndim(image, 2, 'image')
#     vol_geom = astra.create_vol_geom(*image.shape)
#     proj_geom = astra.create_proj_geom('parallel', sen_width, num_sen, theta)
#     proj_id = astra.create_projector(method, proj_geom, vol_geom)
#     sinogram_id, sinogram = astra.create_sino(img, proj_id)
#     sinogram = np.array(sinogram)
#     astra.data2d.clear()
#     astra.projector.clear()
#     astra.algorithm.clear()
#     return sinogram

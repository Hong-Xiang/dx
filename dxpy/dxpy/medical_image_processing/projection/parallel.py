import astra
import astra.creators as ac
import numpy as np
from dxpy.tensor.checks import assert_ndim
from dxpy.tensor.transform import maybe_unbatch
from ..config import config
from dxpy.configs import configurable


@configurable(config['projection'])
def projection2d(image, detector, *, method='cuda', projection_model='linear'):
    assert_ndim(image, 2, 'image')
    vol_geom = ac.create_vol_geom(image.shape)
    proj_geom = ac.create_proj_geom('parallel',
                                    detector.sensor_width,
                                    detector.nb_sensors,
                                    detector.views)
    proj_id = ac.create_projector(projection_model, proj_geom, vol_geom)
    sid, sinogram = ac.create_sino(image, proj_id, gpuIndex=0)
    astra.data2d.clear()
    astra.projector.clear()
    astra.algorithm.clear()
    return sinogram

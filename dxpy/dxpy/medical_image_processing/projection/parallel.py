import astra
import astra.creators as ac
import numpy as np
from dxpy.tensor.checks import assert_ndim
from dxpy.tensor.transform import maybe_unbatch
from ..config import config
from dxpy.configs import configurable


@configurable(config.get('projection'))
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


class Projector2DParallel:
    @configurable(config.get('projection'))
    def __init__(self, detector, phantom_spec, *, method='cuda', projection_model='linear'):
        vol_geom = ac.create_vol_geom(phantom_spec.shape)
        proj_geom = ac.create_proj_geom('parallel',
                                        detector.sensor_width,
                                        detector.nb_sensors,
                                        detector.views)
        self.proj_id = ac.create_projector(
            projection_model, proj_geom, vol_geom)
        self.phan_id = astra.data2d.create('-vol', vol_geom)

    def project(self, image):
        assert_ndim(image, 2, 'image')
        astra.data2d.store(self.phan_id, image)
        sid, result = ac.create_sino(self.phan_id, self.proj_id)
        astra.data2d.delete(sid)
        return result

    def clear(self):
        astra.data2d.delete(self.phan_id)
        astra.projector.delete(self.proj_id)


def padding_pi2full(sinogram):
    """
    Padding sinogram of [0, np.pi) to full [0, 2*np.pi)
    """
    return np.concatenate([sinogram, np.flip(sinogram, 0)], axis=1)
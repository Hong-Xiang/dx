import astra
import astra.creators as ac
from ..config import config
from dxpy.configs import configurable


def _inputs_verification2d(detector, phantom_spec, sinogram):
    from ..detector.base import Detector2D
    from ..exceptions import InputVerifacationError
    if not isinstance(detector, Detector2D):
        raise InputVerifacationError("Input detector is not Detector2D, {}.")
    detector.assert_fit(sinogram)


@configurable(config['reconstruction'])
def reconstruction2d(sinogram, detector, phantom_spec, *, method='FBP_CUDA', iterations=1):
    """
    Args:
        detector: Detector specifics,
        phantom_spec: phantom specifics
        sinogram: 2-dimensional ndarray.
    """
    _inputs_verification2d(detector, phantom_spec, sinogram)
    vol_geom = ac.create_vol_geom(phantom_spec.shape)
    image_id = ac.data2d.create('-vol', vol_geom)
    proj_geom = ac.create_proj_geom('parallel',
                                    detector.sensor_width,
                                    detector.nb_sensors,
                                    detector.views)
    proj_id = ac.create_projector('linear', proj_geom, vol_geom)
    rid, result = astra.creators.create_reconstruction(method,
                                                       proj_id,
                                                       sinogram,
                                                       iterations)
    astra.data2d.clear()
    astra.projector.clear()
    astra.algorithm.clear()
    return result

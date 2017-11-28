import astra
from ..config import config
from dxpy.configs import configurable


def _inputs_verification2d(detector, phantom, sinogram):
    from ..detector.base import Detector2D
    from ..exceptions import InputVerifacationError
    if not isinstance(detector, Detector2D):
        raise InputVerifacationError("Input detector is not Detector2D, {}.")
    detector.assert_fit(sinogram)


@configurable(config['reconstruction'])
def reconstruction2d(detector, phantom, sinogram, *, method=None):
    """
    Args:
        detector: Detector specifics,
        phantom: phantom specifics
        sinogram: 2-dimensional ndarray.
    """
    _inputs_verification2d(detector, phantom, sinogram)
    vol_geom = astra.create_vol_geom(*phantom.shape)
    image_id = astra.data2d.create('-vol', vol_geom)
    sino_geom = astra.create_proj_geom('parallel',
                                       detecotr.sensor_width,
                                       detector.nb_sensors,
                                       detector.views)
    sinogram_id = astra.data2d.create('-sino', sino_geom, data=sinogram)
    cfg = astra.astra_dict(method)
    cfg['ReconstructionDataId'] = image_id
    cfg['ProjectionDataId'] = sinogram_id
    alg_id = astra.algorithm.create(cfg)
    astra.algorithm.run(alg_id, run_time)
    rec = astra.data2d.get(image_id)
    astra.data2d.clear()
    astra.projector.clear()
    astra.algorithm.clear()
    return result

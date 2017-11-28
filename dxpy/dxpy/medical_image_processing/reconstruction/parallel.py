import astra

def _inputs_verification2d(detector, phantom, sinogram):
    from ..detector.base import Detector2D
    from ..exceptions import InputVerifacationError
    if not isinstance(detector, Detector2D):
        raise InputVerifacationError("Input detector is not Detector2D, {}.")

    nb_sensors = detector.nb_sensors

    if isinstance(detector, Detector2DParallelRing):
        nb_sensors = detector.nb_sensors
    if nb_sensors is None:
        raise InputVerifacationError(
            "Unknown detector, can not get nb_sensors, detecotr: {}.")
    raise InputVerifacationError("Unknown error.")


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
                                       detecotr.densor_width,
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

import unittest
import numpy as np
class TestProjectionReconstruction(unittest.TestCase):
    def test_basic(self):
        from dxpy.medical_image_processing.phantom.generator import generate_phantom
        from dxpy.medical_image_processing.phantom import Phantom2DSpec
        from dxpy.medical_image_processing.detector import Detector2DParallelRing
        from dxpy.medical_image_processing.projection.parallel import Projector2DParallel
        from dxpy.medical_image_processing.reconstruction.parallel import Reconstructor2DParallel
        phan = generate_phantom()
        phantom_spec = Phantom2DSpec([256, 256])
        detector = Detector2DParallelRing(nb_sensors=320, nb_views=640, sensor_width=1.0)

        pj = Projector2DParallel(detector, phantom_spec)
        rc = Reconstructor2DParallel(detector, phantom_spec)

        sino = pj.project(phan)
        recon = rc.reconstruct(sino)

        err = phan - recon
        relative_error = np.linalg.norm(err, 2) / np.linalg.norm(phan, 2)
        self.assertLessEqual(relative_error, 0.06)
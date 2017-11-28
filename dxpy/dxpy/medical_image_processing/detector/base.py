class Detector:
    def assert_fit(self, data):
        pass


class Detector3D(Detector):
    ndim = 3


class Detector2D(Detector):
    ndim = 2

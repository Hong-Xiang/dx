from .base import Detector2D
import numpy as np


class Detector2DParallelRing(Detector2D):
    def __init__(self, sensors, views):
        self._sensors = np.array(sensors)
        self._views = np.array(views)
        if self._sensors.ndim != 1:
            raise ValueError('Sensor sensors spec is required to be one dimension, got {}.'.format(
                self._sensors.ndim))
        if self._views.ndim != 1:
            raise ValueError('Sensor views spec is required to be one dimension, got {}.'.format(
                self._views.ndim))

    @property
    def nb_sensors(self):
        return len(self._sensors)

    @property
    def sensor_width(self):
        return np.mean(self._sensors[1:] - self._sensors[:-1])

    @property
    def sensors(self):
        return self._sensors

    @property
    def nb_views(self):
        return len(self._views)

    @property
    def views(self):
        return self._views

    def assert_fit(self, data):
        if detector.nb_sensors != data.shape[0] or detector.nb_views != data.shape[1]:
        msg = "Shape of sinogram {} is not consisted with detector: nb_sensors: {}, nb_views: {}."
        raise ValueError(msg.format(data.shape,
                                    self.nb_sensors, self.nb_views))

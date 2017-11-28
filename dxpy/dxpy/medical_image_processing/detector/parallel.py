from .base import Detector2D


class Detector2DParallelRing(Detector2D):
    def __init__(self, nb_sensors, sensor_width, views):
        self._nb_sensors = nb_sensors
        self._sensor_width = sensor_width
        self._views = views

    @property
    def nb_sensors(self):
        return self._nb_sensors

    @property
    def sensor_width(self):
        return self._sensor_width

    @property
    def views(self):
        return self._views

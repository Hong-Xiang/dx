from ...graph import Graph
import tensorflow as tf


class Normalizer(Graph):
    def __init__(self, name):
        super(__class__, name)
        self.register_main_task(self._normalization)
        self.register_task('denorm', self._denormalization)

    def _normalization_kernel(self, feeds):
        raise NotImplementedError

    def _denormalization_kernel(self, feeds):
        raise NotImplementedError

    def _normalization(self, feeds):
        return self._normalization_kernel(feeds)

    def _denormalization(self, feeds):
        return self._denormalization_kernel(feeds)


class FixWhite(Normalizer):
    def __init__(self, name):
        super(__class__, name)

    def _normalization_kernel(self, feeds):
        with tf.name_scope('normalization'):
            return (feeds - self.c['mean']) / self.c['std']

    def _denormalization_kernel(self, feeds):
        with tf.name_scope('denormalization'):
            return feeds * self.c['std'] + self.c['mean']


class SelfWhite(Normalizer):
    def __init__(self, name):
        super(__class__, name)

    def _normalization_kernel(self, feeds):
        with tf.name_scope('normalization'):
            rmin = tf.reduce_min(feeds, self.c['axis'], True)
            rmax = tf.reduce_max(feeds, self.c['axis'], True)
            data = (feeds - rmin) / (rmin - rmax)
            return {'min': rmin, 'max': rmax, 'data': data}

    def _denormalization_kernel(self, feeds):
        with tf.name_scope('denormalization'):
            return feeds['data'] * (feeds['max'] - feeds['min']) + feeds['min']

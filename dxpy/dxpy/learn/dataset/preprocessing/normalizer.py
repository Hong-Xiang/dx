from ...graph import Graph
import tensorflow as tf


class Normalizer(Graph):

    def __init__(self, name):
        super(__class__, self).__init__(name)
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
    method_name = 'fix_white'

    def __init__(self, name):
        super(__class__, self).__init__(name)

    def _normalization_kernel(self, feeds):
        with tf.name_scope('normalization'):
            return (feeds - self.c['mean']) / self.c['std']

    def _denormalization_kernel(self, feeds):
        with tf.name_scope('denormalization'):
            return feeds * self.c['std'] + self.c['mean']


class MeanStdWhite(Normalizer):
    method_name = 'mean_std_white'

    def __init__(self, name):
        super(__class__, self).__init__(name)

    def _normalization_kernel(self, feeds):
        with tf.name_scope('normalization'):
            mean = tf.reduce_mean(feeds)
            maxb = tf.reduce_max(feeds)
            minb = tf.reduce_min(feeds)
            return (feeds - self.c['mean']) / self.c['std']


class SelfMinMax(Normalizer):
    method_name = 'self_min_max'

    def __init__(self, name):
        super(__class__, self).__init__(name)

    def _normalization_kernel(self, feeds):
        with tf.name_scope('normalization'):
            rmin = tf.reduce_min(feeds)
            rmax = tf.reduce_max(feeds)
            data = (feeds - rmin) / (rmax - rmin)
            return {'min': rmin, 'max': rmax, 'data': data}

    def _denormalization_kernel(self, feeds):
        with tf.name_scope('denormalization'):
            return feeds['data'] * (feeds['max'] - feeds['min']) + feeds['min']


class SelfMeanStd(Normalizer):
    method_name = 'self_mean_std'

    def __init__(self, name):
        super(__class__, self).__init__(name)

    def _normalization_kernel(self, feeds):
        with tf.name_scope('normalization'):
            mean, stdv = tf.nn.moments(feeds)
            data = (feeds - mean) / stdv
            return {'mean': mean, 'std': stdv, 'data': data}

    def _denormalization_kernel(self, feeds):
        with tf.name_scope('denormalization'):
            return feeds['data'] * feeds['std'] + feeds['mean']

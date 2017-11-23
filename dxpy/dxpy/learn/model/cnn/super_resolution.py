import tensorflow as tf
from ..base import Model, NodeKeys
from .blocks import StackedConv2D


class SRKeys:
    REPS = 'reps'


class SuperResolution2x(Model):
    def __init__(self, name, inputs, **config):
        super().__init__(name, inputs, **config)

    def _kernel(self, feeds):
        from ..image import resize
        with tf.name_scope('input'):
            u = resize(feeds[NodeKeys.INPUT], (2, 2))
            if SRKeys.REPS in feeds:
                r = resize(feeds[SRKeys.REPS], (2, 2))
                u = tf.concat([r, u], axis=3)
        x = StackedConv2D('kernel', u, nb_layers=10, filters=32)()
        with tf.variable_scope('inference'):
            y = tf.layers.conv2d(x, 1, 3, padding='same')
        with tf.name_scope('loss'):
            l = tf.losses.mean_squared_error(feeds[NodeKeys.LABEL], y)
        return {NodeKeys.INFERENCE: y, NodeKeys.LOSS: l,  SRKeys.REPS: x}


class SuperResolutionMultiScale(Model):
    def __init__(self, name, inputs, nb_down_sample, **config):
        super().__init__(name, inputs, **config)

    @classmethod
    def _default_config(cls):
        from dxpy.collections.dicts import combine_dicts
        return combine_dicts({
            'nb_down_sample': 3,
            'loss_weight': 1.0,
        }, super()._default_config())

    def _get_node(self, node_type, down_sample_ratio, source=None):
        if source is None:
            source = self.nodes
        name = "{}/image{}x".format(node_type, 2**down_sample_ratio)
        return source[name]

    def _kernel(self, feeds):
        x = None
        r = None
        losses = []
        for i_down_sample in reversed(range(1, self.param('nb_down_sample') + 1)):
            if x is None:
                x = self._get_node('input', i_down_sample, feeds)
            mid_result = SuperResolution2x('sr2x_{}'.format(i_down_sample),
                                           {NodeKeys.INPUT: x,
                                            NodeKeys.LABEL: self._get_node('label', i_down_sample - 1, feeds),
                                            SRKeys.REPS: r})()
            x = mid_result[NodeKeys.INFERENCE]
            if NodeKeys.LOSS in mid_result:
                losses.append(mid_result[NodeKeys.LOSS])
            r = mid_result[SRKeys.REPS]
        result = {NodeKeys.INFERENCE: x}
        if len(losses) > 0:
            with tf.name_scope('loss'):
                if not isinstance(self.param('loss_weight'), (list, tuple)):
                    lw = [self.param('loss_weight')] * \
                        self.param('nb_down_sample')
                else:
                    lw = self.param('loss_weight')
                for i, l in enumerate(losses):
                    losses[i] = losses[i] * lw[i]
                result[NodeKeys.LOSS] = tf.add_n(losses)
        return result

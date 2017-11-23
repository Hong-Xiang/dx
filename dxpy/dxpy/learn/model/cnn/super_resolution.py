import tensorflow as tf
from ..base import Model, NodeKeys
from .blocks import StackedConv2D


class SuperResolution2x(Model):
    def __init__(self, name, inputs, **config):
        super().__init__(name, inputs, **config)

    def _kernel(self, feeds):
        from ..image import resize
        with tf.name_scope('input'):
            u = resize(feeds[NodeKeys.INPUT], (2, 2))
            if 'represens' in feeds:
                r = resize(represens, (2, 2))
                u = tf.concat([r, u], axis=3)
        x = StackedConv2D('kernel', u, nb_layers=10, filters=32)()
        with tf.variable_scope('inference'):
            y = tf.layers.conv2d(x, 1, 3, padding='same')
        with tf.name_scope('loss'):
            l = tf.losses.mean_squared_error(feeds[NodeKeys.LABEL], y)
        return {NodeKeys.INFERENCE: y, NodeKeys.LOSS: l, 'represens': x}


# class SRB(Model):
#     def __init__(self, image_input, represents=None, name='srb', **configs):
#         super().__init__(name=name, inputs={'ipt': image_input, 'rep': represents},
#                          **configs)

#     def _kernel(self, feeds):
#         if feeds['rep'] is None:

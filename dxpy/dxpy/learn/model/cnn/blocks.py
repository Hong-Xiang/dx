import tensorflow as tf
from ..base import Model
from ..activation import get_activation


class Conv2D(Model):
    def __init__(self, name='conv2d', input_=None, **config):
        super().__init__(name, inputs={'input': input_}, **config)

    @classmethod
    def _default_config(cls):
        result = dict()
        result.update(super()._default_config())
        result.update({
            'kernel_size': 3,
            'strides': (1, 1),
            'padding': 'same',
            'reuse': False,
            'activation': 'relu',
            'pre_activation': False,
            'post_activation': True,
            'kernel_name': 'conv2d'
        })
        return result

    def _kernel(self, feeds):
        x = feeds['input']
        with tf.variable_scope('kernel'):
            if self.param('pre_activation', feeds):
                x = get_activation(self.param('activation', feeds))(x)
            x = tf.layers.conv2d(x, self.param('filters', feeds),
                                 self.param('kernel_size', feeds),
                                 self.params('strides', feeds),
                                 self.params('padding', feeds), name='conv')
            if self.param('pre_activation', feeds):
                x = get_activation(self.param('activation', feeds))(x)
        return x


class InceptionBlock(Model):
    def __init__(self, name='incept', input_=None, **config):
        super().__init__(name, inputs={'input': input_}, **config)

    @classmethod
    def _default_config(cls):
        result = dict()
        result.update(super()._default_config())
        result.update({
            'paths': 3
            'reuse': False,
            'pre_activation': True,
        })
        return result

    def _kernel(self, feeds):
        x = feeds['input']
        filters = x.shape.aslist()[-1]
        with tf.variable_scope('kernel'):
            if self.param('pre_activation', feeds):
                x = get_activation(self.param('activation', feeds))(x)
            paths = []
            for i_path in range(self.param('paths')):
                paths.append(Conv2D('conv2d_{}'.format(i_path), x, filters=filters, kernel_size=1)
                for j in range(i_path):

            if self.param('pre_activation', feeds):
                x=get_activation(self.param('activation', feeds))(x)
        return x

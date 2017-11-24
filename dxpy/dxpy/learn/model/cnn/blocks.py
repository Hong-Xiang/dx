import tensorflow as tf
from ..base import Model, NodeKeys, ModelPipe
from .. import activation
from ..tensor import shape_as_list


class Conv2D(Model):
    def __init__(self, name='conv2d', input_tensor=None, filters=None, kernel_size=None,
                 *,
                 strides=None, padding=None, activation=None, **config):
        super().__init__(name, input_tensor,
                         filters=filters,
                         kernel_size=kernel_size,
                         strides=strides,
                         padding=padding,
                         activation=activation,
                         **config)

    @classmethod
    def _default_config(cls):
        from dxpy.collections.dicts import combine_dicts
        return combine_dicts({
            'kernel_size': 3,
            'strides': (1, 1),
            'padding': 'same',
            'activation': 'basic'
        }, super()._default_config())

    def _kernel(self, feeds):
        x = feeds[NodeKeys.INPUT]
        acc = activation.unified_config(self.param('activation', feeds))
        x = activation.apply(acc, x, 'pre')
        x = tf.layers.conv2d(x, self.param('filters', feeds),
                             self.param('kernel_size', feeds),
                             self.param('strides', feeds),
                             self.param('padding', feeds), name='convolution')
        x = activation.apply(acc, x, 'post')
        return x


class StackedConv2D(Model):
    def __init__(self, name, input_tensor, *,
                 nb_layers=None,
                 activation=None,
                 filters=None, **config):
        super().__init__(name, input_tensor, nb_layers=nb_layers,
                         filters=filters, activation=activation, **config)

    @classmethod
    def _default_config(cls):
        from dxpy.collections.dicts import combine_dicts
        cfg = {
            'activation': 'basic',
            'padding': 'same',
            'filters': 32
        }
        return combine_dicts(cfg, super()._default_config())

    def _kernel(self, feeds):
        x = feeds[NodeKeys.INPUT]
        for i in range(self.param('nb_layers')):
            x = Conv2D('conv2d_{}'.format(i), x, self.param('filters'),
                       activation=self.param('activation'),
                       padding=self.param('padding'))()
        return x


class InceptionBlock(Model):
    def __init__(self, name='incept', input_tensor=None, activation=None, **config):
        super().__init__(name, inputs={NodeKeys.INPUT: input_tensor}, **config)

    @classmethod
    def _default_config(cls):
        from dxpy.collections.dicts import combine_dicts
        return combine_dicts({
            'paths': 3,
            'activation': 'incept',
        }, super()._default_config())

    def _kernel(self, feeds):
        x = feeds[NodeKeys.INPUT]
        filters = x.shape.as_list()[-1]
        acc = activation.unified_config(self.param('activation', feeds))
        x = activation.apply(acc, x, 'pre')
        paths = []
        for i_path in range(self.param('paths')):
            with tf.variable_scope('path_{}'.format(i_path)):
                h = Conv2D('conv2d_0', x, filters, 1,
                           activation='linear').as_tensor()
                for j in range(i_path):
                    h = Conv2D('conv2d_{}'.format(j + 1), h, filters,
                               3, activation='pre').as_tensor()
                paths.append(h)
        with tf.name_scope('concat'):
            x = tf.concat(paths, axis=-1)
        x = Conv2D('conv_end', x, filters, 1, activation='pre').as_tensor()
        return x


class ResidualIncept(Model):
    def __init__(self, name, input_tensor, **config):
        super().__init__(name, inputs=input_tensor, **config)

    @classmethod
    def _default_config(cls):
        from dxpy.collections.dicts import combine_dicts
        return combine_dicts({
            'ratio': 0.1,
            'paths': 3,
        }, cls._default_config())

    def _kernel(self, feeds):
        x = feeds[NodeKeys.INPUT]
        h = InceptionBlock('incept', x, paths=self.param('paths'))
        with tf.name_scope('add'):
            x = x + h * self.param('ratio')
        return x


class ResidualStackedConv(Model):
    def __init__(self, name, input_tensor, *, nb_layers=None, ratio=None, **config):
        super().__init__(name, inputs=input_tensor,
                         nb_layers=nb_layers, ratio=ratio, **config)

    @classmethod
    def _default_config(cls):
        from dxpy.collections.dicts import combine_dicts
        return combine_dicts({
            'ratio': 0.1,
            'nb_layers': 2,
        }, super()._default_config())

    def _kernel(self, feeds):
        x = feeds[NodeKeys.INPUT]
        h = StackedConv2D('convs', x, nb_layers=self.param('nb_layers'),
                          activation='res_celu', filters=shape_as_list(x)[-1])()
        with tf.name_scope('add'):
            return x + h * self.param('ratio')


class StackedResidual(Model):
    """
    Sub model name: sub_{0..nb_layers}
    """

    def __init__(self, name, input_tensor, *, nb_layers=None, block_type=None, **config):
        super().__init__(name, inputs=input_tensor, nb_layers=nb_layers, **config)

    @classmethod
    def _default_config(cls):
        from dxpy.collections.dicts import combine_dicts
        return combine_dicts({
            'nb_layers': 10,
            'block_type': 'incept',
        }, cls._default_config())

    def _kernel(self, feeds):
        x = feeds[NodeKeys.INPUT]
        for i in range(self.param('nb_layers')):
            name = self.name / 'res_{}'.format(i)
            if self.param('block_type') == 'incept':
                x = ResidualIncept(name, x)
            elif self.param('block_type') == 'stacked_conv':
                x = ResidualStackedConv(name, x)
        return x

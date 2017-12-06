import tensorflow as tf
from .blocks import Conv2D, StackedConv2D, InceptionBlock
from ..base import Model, NodeKeys
from ..tensor import shape_as_list
from dxpy.configs import configurable
from ...config import get_configs_view

class ResidualIncept(Model):
    @configurable(get_configs_view(), with_name=True)
    def __init__(self, name, input_tensor, ratio=0.3, paths=3, **kw):
        super().__init__(name, inputs=input_tensor, ratio=ratio, paths=paths, **kw)

    @classmethod
    def _default_config(cls):
        from dxpy.collections.dicts import combine_dicts
        return combine_dicts({
            'ratio': 0.1,
            'paths': 3,
        }, super()._default_config())

    def _kernel(self, feeds):
        x = feeds[NodeKeys.INPUT]
        h = InceptionBlock('incept', x, paths=self.param('paths'))()
        with tf.name_scope('add'):
            x = x + h * self.param('ratio')
        return x


class ResidualStackedConv(Model):
    @configurable(get_configs_view(), with_name=True)
    def __init__(self, name, input_tensor, *, nb_layers=None, block_type=None, ratio=0.1, **config):
        super().__init__(name, inputs=input_tensor, nb_layers=nb_layers, ratio=ratio, **config)

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
    INCEPT_TYPE = 'incept'
    STACKED_CONV_TYPE = 'stacked_conv'

    @configurable(get_configs_view(), with_name=True)
    def __init__(self, name, input_tensor, *, nb_layers=None, block_type=None, **config):
        super().__init__(name, inputs=input_tensor,
                         nb_layers=nb_layers, block_type=block_type, **config)

    @classmethod
    def _default_config(cls):
        from dxpy.collections.dicts import combine_dicts
        return combine_dicts({
            'nb_layers': 10,
            'block_type': cls.INCEPT_TYPE,
        }, super()._default_config())

    def _kernel(self, feeds):
        x = feeds[NodeKeys.INPUT]
        for i in range(self.param('nb_layers')):
            name = self.name / 'res_{}'.format(i)
            if self.param('block_type') == self.INCEPT_TYPE:
                x = ResidualIncept(name, x)()
            elif self.param('block_type') == self.STACKED_CONV_TYPE:
                x = ResidualStackedConv(name, x)()
        return x

from dxpy.configs import configurable
from ...config import config
class StackedResidualv2(Model):
    """
    Sub model name: sub_{0..nb_layers}
    """
    INCEPT_TYPE = 'incept'
    STACKED_CONV_TYPE = 'stacked_conv'
    @configurable(config, with_name=True)
    def __init__(self, name, input_tensor, *, nb_layers=10, block_type='incept', **config):
        super().__init__(name, inputs=input_tensor,
                         nb_layers=nb_layers, block_type=block_type, **config)

    def _kernel(self, feeds):
        x = feeds[NodeKeys.INPUT]
        for i in range(self.param('nb_layers')):
            name = self.name / 'res_{}'.format(i)
            if self.param('block_type') == self.INCEPT_TYPE:
                x = ResidualIncept(name, x)()
            elif self.param('block_type') == self.STACKED_CONV_TYPE:
                x = ResidualStackedConv(name, x)()
        return x

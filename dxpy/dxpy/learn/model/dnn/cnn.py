import tensorflow as tf
from ...graph import Graph


class InceptionBlock(Graph):
    def __init__(self, name):
        super(__class__, self).__init__(name)
        self.register_main_task(self._kernel)

    @classmethod
    def _default_config(cls):
        return {
            'kernel_size': 3,
            'strides': (1, 1),
            'padding': 'same',
            'reuse': False,
            'activation': 'relu',
            'pre_activation': True,
            'kernel_name': 'conv2d'
        }

    def _kernel(self, input_tensor):
        x = input_tensor
        with tf.name_scope(self.c['kernel_name']):
        if self.c['pre_activation']:
            if self.c['activation'].lower() == 'relu':

        x = tf.layers.conv2d(
            x, self.c['filters'], self.c['kernel_size'], self.c['strides'], self.c['padding'], reuse=self.c['reuse'], name='conv')

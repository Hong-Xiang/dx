import tensorflow as tf
from ..net import Net
from ..graph import NodeKeys


class SRStackCNN(Net):
    def __init__(self, name, low_image, high_image, **config):
        super().__init__(name,
                         inputs={NodeKeys.INPUT: low_image,
                                 NodeKeys.LABEL: high_image}, **config)

    @classmethod
    def _default_config(cls):
        from dxpy.collections.dicts import combine_dicts
        cfg = {
            'input_shape': [14, 14, 1],
            'label_shape': [28, 28, 1]
        }
        return combine_dicts(cfg, super()._default_config())

    @classmethod
    def _default_inputs(cls):
        return {
            NodeKeys.INPUT: {'shape': cls._default_config()['input_shape']},
            NodeKeys.LABEL: {'shape': cls._default_config()['label_shape']}
        }

    def _pre_create_in_scope(self):
        from ..model.cnn.blocks import StackedConv2D
        model = StackedConv2D('stackedcnns', self.tensor(
            NodeKeys.INPUT), 10, lazy_create=True)
        self.register_child_model('sr_kernel', model)

    def _kernel(self, feeds):
        from ..model.image import resize
        x = feeds[NodeKeys.INPUT]
        u = resize(x, (2, 2))
        h = self.child_model('sr_kernel')(u)
        with tf.name_scope('inference'):
            y = tf.layers.conv2d(h, 1, 3, padding='same')
        result = {NodeKeys.INFERENCE: y}
        if NodeKeys.LABEL in feeds:
            with tf.name_scope('loss'):
                l = tf.losses.mean_squared_error(feeds[NodeKeys.LABEL], y)
        result[NodeKeys.LOSS] = l
        return result

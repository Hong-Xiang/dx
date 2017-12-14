import tensorflow as tf
from ...base import Net, NodeKeys
from dxpy.configs import configurable
from dxpy.learn.config import config


class SinNet(Net):
    @configurable(config, with_name=True)
    def __init__(self, name, inputs, nb_layers, nb_units, **kw):
        super().__init__(name=name, inputs=inputs, nb_layers=nb_layers,
                         nb_units=nb_units, add_trainer=True, add_saver=True, **kw)

    def _post_kernel_post_outputs(self):
        from dxpy.learn.train.trainer_2 import Trainer
        from dxpy.learn.train.saver import Saver
        if self.param('add_trainer'):
            if NodeKeys.LOSS in self.nodes:
                self.register_node(NodeKeys.TRAINER,
                                   Trainer(self.name / 'trainer', self.nodes[NodeKeys.LOSS]))
        if self.param('add_saver'):
            self.register_node(NodeKeys.SAVER, Saver(self.name / 'saver'))

    def _kernel(self, feeds):
        from dxpy.learn.model.losses import mean_square_error
        x = feeds[NodeKeys.INPUT]
        with tf.variable_scope('kernel'):
            h = x
            for i in range(self.param('nb_layers')):
                h = tf.layers.dense(h, self.param(
                    'nb_units'), activation=tf.nn.relu, name='dense_{}'.format(i))
            yp = tf.layers.dense(h, 1, name='infer')
        result = {NodeKeys.INFERENCE: yp}
        if NodeKeys.LABEL in feeds:
            y = feeds[NodeKeys.LABEL]
            loss = mean_square_error(y, yp)
            result[NodeKeys.LOSS] = loss
        return result

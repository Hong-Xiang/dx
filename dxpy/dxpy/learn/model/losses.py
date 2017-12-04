import tensorflow as tf
from dxpy.configs import configurable
from ..config import config
from .base import NodeKeys

def mean_square_error(label, data):
    with tf.name_scope('mean_squared_error'):
        return tf.sqrt(tf.reduce_mean(tf.square(label - data)))


@configurable(config.get('loss').get('poission_loss'))
def poission_loss(label, data, *, restrict_data_absolute=True):
    with tf.name_scope('poission_loss'):
        return log_possion_loss(tf.log(label), data,
                                restrict_data_absolute=restrict_data_absolute)


@configurable(config.get('loss').get('poission_loss'))
def log_possion_loss(log_label, data, *, restrict_data_absolute=True):
    with tf.name_scope('log_poission_loss'):
        if restrict_data_absolute:
            data = tf.abs(data)
        return tf.nn.log_poisson_loss(log_label, data)

from ..model.base import Model

class PoissionLossWithDenorm(Model):
    """
    Inputs:
    NodeKeys.INPUT: infer
    NodeKeys.LABEL: label
    Outputs:
    NodeKeys.OUTPUT: scalar loss
    """
    @configurable(config, with_name=True)
    def __init__(self, name, inputs, with_log=False, threshold=10, mean=0.0, std=1.0, weight=1.0):
        super().__init__(name, inputs=inputs, with_log =with_log, threshold=threshold, mean=mean, std=std, weight=weight)

    def _kernel(self, feeds):
        label = feeds[NodeKeys.LABEL]
        infer = feeds[NodeKeys.INPUT]
        with tf.name_scope('denorm_white'):
            label = label * self.param('std') + self.param('mean')
            infer = infer * self.param('std') + self.param('mean')
        if self.param('with_log'):
            with tf.name_scope('denorm_log'):
                infer = tf.exp(infer)
            with tf.name_scope('loss'):
                loss = log_possion_loss(label, infer)
        else:
            with tf.name_scope('loss')
                loss = poission_loss(label, infer) 
        return {NodeKeys.OUTPUT: loss}
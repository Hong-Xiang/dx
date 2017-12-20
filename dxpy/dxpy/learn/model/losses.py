import tensorflow as tf
from dxpy.configs import configurable, ConfigsView
# from ..config import get_configs_view, config
from dxpy.learn.config import config
from .base import NodeKeys

def mean_square_error(label, data):
    with tf.name_scope('mean_squared_error'):
        return tf.sqrt(tf.reduce_mean(tf.square(label - data)))


def poission_loss(label, data, *, compute_full_loss=False):
    with tf.name_scope('poission_loss'):
        label = tf.maximum(label, 0.0)
        # return log_possion_loss(tf.log(label), data)
        return tf.reduce_mean(tf.keras.losses.poisson(label, data))
                                


def log_possion_loss(log_label, data, *, compute_full_loss=False):
    """
    log_label: log value of expectation (inference)
    data: Poission sample
    """
    with tf.name_scope('log_poission_loss'):
        data = tf.maximum(data, 0.0)
        return tf.reduce_mean(tf.nn.log_poisson_loss(data, log_label, compute_full_loss))

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
    def __init__(self, name, inputs, with_log=False, threshold=10, mean=0.0, std=1.0, **kw):
        super().__init__(name, inputs=inputs, with_log =with_log, threshold=threshold, mean=mean, std=std, **kw)
    def _kernel(self, feeds):
        from dxpy.debug.utils import dbgmsg
        dbgmsg(self.param('mean'))
        dbgmsg(self.param('std'))

        label = feeds[NodeKeys.LABEL]
        infer = feeds[NodeKeys.INPUT]
        with tf.name_scope('denorm_white'):
            label = label * self.param('std') + self.param('mean')
            infer = infer * self.param('std') + self.param('mean')
        if self.param('with_log'):
            with tf.name_scope('denorm_log_for_data'):
                infer = tf.exp(infer)
            with tf.name_scope('loss'):
                loss = log_possion_loss(label, infer)
        else:
            with tf.name_scope('loss'):
                loss = poission_loss(label, infer) 
        return {NodeKeys.MAIN: loss}
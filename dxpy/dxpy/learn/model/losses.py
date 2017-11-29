import tensorflow as tf
from dxpy.configs import configurable
from ..config import config


def mean_square_error(label, data):
    with tf.name_scope('mean_squared_error'):
        return tf.sqrt(tf.reduce_mean(tf.square(label - data)))


@configurable(config['loss']['poission_loss'])
def poission_loss(label, data, *, restrict_data_absolute=True):
    with tf.name_scope('poission_loss'):
        return log_possion_loss(tf.log(label), data,
                                restrict_data_absolute=restrict_data_absolute)


@configurable(config['loss']['poission_loss'])
def log_possion_loss(log_label, data, *, restrict_data_absolute=True):
    with tf.name_scope('log_poission_loss'):
        if restrict_data_absolute:
            data = tf.abs(data)
        return tf.nn.log_poisson_loss(log_label, data)

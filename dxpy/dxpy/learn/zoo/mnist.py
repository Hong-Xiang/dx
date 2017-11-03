import tensorflow as tf

from ..model.base import Model
from ..graph import Graph


class MNISTSimpleConvModel(Model):
    def __init__(self, name, keep_prob, *, config):
        super(__class__, self).__init__(name, config=config)

    @classmethod
    def _default_config(self):
        return {
            'inputs': {
                'image': {'shape': [None, 28, 28, 1]},
                'label': {'shape': [None, 10]}
            }
        }

    def _kernel(self, feeds):
        x = feeds['image']
        x = tf.layers.conv2d(x, 32, 5, padding='same',
                             name='conv1', activation=tf.nn.relu)
        x = tf.layers.conv2d(x, 32, 1, padding='same',
                             name='pool1', strides=(2, 2), activation=tf.nn.relu)
        x = tf.layers.conv2d(x, 64, 3, padding='same',
                             name='conv2', activation=tf.nn.relu)
        x = tf.layers.conv2d(x, 64, 1, padding='same',
                             name='pool2', strides=(2, 2), activation=tf.nn.relu)
        x = tf.reshape(x, [-1, 7 * 7 * 64])
        x = tf.layers.dense(x, 1024, activation=tf.nn.relu)

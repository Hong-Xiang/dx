import tensorflow as tf

from ..model.base import Model
from ..graph import Graph


class MNISTSimpleConvModel(Model):
    def __init__(self, name, inputs=None, **config):
        super(__class__, self).__init__(name, inputs, **config)

    @classmethod
    def _default_inputs(self):
        return {
            'image': {'shape': [None, 28, 28, 1]},
            'label': {'shape': [None, 10]}}

    def _kernel(self, feeds):
        x = feeds['image']        
        result = dict()
        with tf.variable_scope('kernel'):
            x = tf.layers.conv2d(x, 32, 5, padding='same',
                                 name='conv1', activation=tf.nn.relu)
            x = tf.layers.conv2d(x, 32, 1, padding='same',
                                 name='pool1', strides=(2, 2), activation=tf.nn.relu)
            x = tf.layers.conv2d(x, 64, 3, padding='same',
                                 name='conv2', activation=tf.nn.relu)
            x = tf.layers.conv2d(x, 64, 1, padding='same',
                                 name='pool2', strides=(2, 2), activation=tf.nn.relu)
            with tf.name_scope('flatten'):
                x = tf.reshape(x, [-1, 7 * 7 * 64])
            x = tf.layers.dense(x, 1024, activation=tf.nn.relu, name='fc1')
            result['logits'] = tf.layers.dense(x, 10, name='fc2')
        with tf.name_scope('prediction'):
            result['prediction'] = tf.argmax(result['logits'], 1)
        if 'label' in feeds:
            with tf.name_scope('loss'):
                result['cross_entropy'] = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
                    labels=feeds['label'], logits=result['logits']))
            with tf.name_scope('accuracy'):
                correct_prediction = tf.equal(
                    result['prediction'], tf.argmax(feeds['label'], 1))
                result['accuracy'] = tf.reduce_mean(
                    tf.cast(correct_prediction, tf.float32))
        return result

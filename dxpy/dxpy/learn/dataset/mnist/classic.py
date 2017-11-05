import tensorflow as tf
import numpy as np
import random
from ..base import DatasetClassic


class MNISTClassic(DatasetClassic):
    def __init__(self, name, **config):
        super(__class__, self).__init__(name, **config)
        self.images, self.labels = self.__load_data()

    @classmethod
    def _default_config(cls):
        return {
            'fields': {
                'image': {
                    'dtype': tf.float32,
                    'shape': [28, 28, 1],
                },
                'label': {
                    'dtype': tf.int64,
                    'shape': [10]
                }
            },
            'batch_size': 32,
        }

    def _load_sample(self, feeds=None):
        idx = random.randint(0, self.images.shape[0] - 1)
        image = np.reshape(self.images[idx, ...], [28, 28, 1])
        label = self.labels[idx, ...]
        return {'image': image, 'label': label}

    def __load_data(self):
        from tensorflow.examples.tutorials.mnist import input_data
        from tensorflow.contrib.data import Dataset
        mnist = input_data.read_data_sets(
            '/home/hongxwing/Datas/mnist/tfdefault', one_hot=True)
        images = mnist.train.images
        labels = mnist.train.labels

        return images, labels

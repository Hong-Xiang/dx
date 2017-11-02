from ..base import DatasetTFRecords
import tensorflow as tf


class MNIST(DatasetTFRecords):
    def __init__(self, name):
        super(__class__, self).__init__(name)

    @classmethod
    def _parse_example(cls, example):
        return tf.parse_single_example(example, features={
            'image': tf.FixedLenFeature([], tf.string),
            'shape': tf.FixedLenFeature([2], tf.int64),
            'label': tf.FixedLenFeature([1], tf.int64)
        })

    @classmethod
    def _decode_image(cls, data):
        return {'image': tf.decode_raw(data['image'], tf.uint8),
                'shape': data['shape'],
                'label': data['label']}

    @classmethod
    def _reshape_tensors(cls, data):
        return {'image': tf.reshape(data['image'], [28, 28, 1]),
                'shape': tf.concat([data['shape'], [1]], axis=0),
                'label': tf.reshape(data['label'], [])}

    def _normalize(self, data):
        from ..preprocessing.normalizer import FixWhite
        if self.c['normalization']['method'].lower() == 'fixwhite':
            return {'image': FixWhite(self.name / 'normalization')(data['image']),
                    'shape': data['shape'],
                    'label': data['label']}
        return data

    def _processing(self, dataset):
        return (dataset
                .map(self._parse_example)
                .map(self._decode_image)
                .map(self._reshape_tensors)
                .map(self._normalize)
                .batch(self.c['batch_size'])
                .cache()
                .repeat())

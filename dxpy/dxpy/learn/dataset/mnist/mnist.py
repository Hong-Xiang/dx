from ..base import DatasetTFRecords
import tensorflow as tf


class MNIST(DatasetTFRecords):
    def __init__(self, name):
        super(__class__, self).__init__(name)

    def _before_processing(self):
        self._add_normalizer()

    def _add_normalizer(self):
        from ..preprocessing.normalizer import SelfMinMax
        self._normalizer = None
        if self.c['normalization']['method'].lower() == 'selfminmax':
            self._normalizer = SelfMinMax(self.name / 'normalization')

    @classmethod
    def _default_config(cls):
        return {
            'files': ['/home/hongxwing/Datas/mnist/mnist.train.tfrecord'],
            'batch_size': 32,
            'normalization': {
                'method': 'selfminmax'
            },
            'one_hot': True,
        }

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
    def _change_dtype(cls, data):
        return {'image': tf.to_float(data['image']),
                'shape': data['shape'],
                'label': data['label']}

    @classmethod
    def _reshape_tensors(cls, data):
        return {'image': tf.reshape(data['image'], [28, 28, 1]),
                'shape': tf.concat([data['shape'], [1]], axis=0),
                'label': tf.reshape(data['label'], [])}

    def _normalize(self, data):
        if self._normalizer is None:
            image = data['image']
        else:
            image = self._normalizer(data['image'])['data']
        return {'image': image,
                'shape': data['shape'],
                'label': data['label']}
        return data

    def _maybe_onehot(self, data):
        result = {
            'image': data['image'],
            'shape': data['shape']
        }
        if self.c['one_hot']:
            result.update({'label': tf.one_hot(data['label'], depth=10)})
        else:
            result.update({'label': data['label']})
        return result

    def _processing(self, dataset):
        return (dataset
                .map(self._parse_example)
                .map(self._decode_image)
                .map(self._change_dtype)
                .map(self._reshape_tensors)
                .map(self._normalize)
                .map(self._maybe_onehot)
                .batch(self.c['batch_size'])
                .cache()
                .repeat())

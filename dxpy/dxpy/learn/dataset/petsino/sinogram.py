from ..base import DatasetTFRecords
import tensorflow as tf


class PhantomSinograms(DatasetTFRecords):
    def __init__(self, name, **config):
        super().__init__(name, **config)

    @classmethod
    def _parse_example(cls, example):
        return tf.parse_single_example(example, features={
            'phantom_shape': tf.FixedLenFeature([3], tf.int64),
            'sinogram_shape': tf.FixedLenFeature([3], tf.int64),
            'phantom_type': tf.FixedLenFeature([], tf.int64),
            'phantom': tf.FixedLenFeature([256, 256], tf.float32),
            'sinogram': tf.FixedLenFeature([320, 640], tf.float32),
        })

    @classmethod
    def _default_config(cls):
        from dxpy.collections.dicts import combine_dicts
        return combine_dicts({
            'normalization': {
                'method': 'pass'
            },
        }, super()._default_config())

    @classmethod
    def _reshape_tensors(cls, data):
        return {'phantom': tf.reshape(data['phantom'], [256, 256, 1]),
                'sinogram': tf.reshape(data['sinogram'], [320, 640, 1])}

    def _pre_processing(self):
        self._add_normalizer()

    def _normalize(self, data):
        if self._normalizer is None:
            sinogram = data['sinogram']
        else:
            sinogram = self._normalizer(data['sinogram'])['data']
        return {'phantom': data['phantom'], 'sinogram': sinogram}

    def _add_normalizer(self):
        from ...model import normalizer
        self._normalizer = None
        if self.param('normalization')['method'].lower() != 'pass':
            self._normalizer = normalizer.get_normalizer(
                self.param('normalization')['method'].lower())

    def _processing(self):
        return (super()._processing()
                .map(self._parse_example)
                .map(self._reshape_tensors)
                .map(self._normalize)
                .batch(self.c['batch_size'])
                .cache()
                .repeat())

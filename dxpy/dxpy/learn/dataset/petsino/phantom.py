from ..base import DatasetTFRecords
import tensorflow as tf


class PhantomSinograms(DatasetTFRecords):
    def __init__(self, name):
        super(__class__, self).__init__(name)

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
    def _reshape_tensors(cls, data):        
        return {'phantom': tf.reshape(data['phantom'], [256, 256, 1]),
                'sinogram': tf.reshape(data['sinogram'], [320, 640, 1])}

    # def _normalize(self, data):
    #     from ..preprocessing.normalizer import FixWhite
    #     if self.c['normalization']['method'].lower() == 'fixwhite':
    #         return {'image': FixWhite(self.name / 'normalization')(data['image']),
    #                 'shape': data['shape'],
    #                 'label': data['label']}
    #     return data

    def _processing(self, dataset):
        return (dataset
                .map(self._parse_example)
                .map(self._reshape_tensors)
                # .map(self._normalize)
                .batch(self.c['batch_size'])
                .cache()
                .repeat())

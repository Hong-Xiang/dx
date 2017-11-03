import numpy as np
import tensorflow as tf
from ..graph import Graph


class Dataset(Graph):
    """Base class of database
    Database add some special tasks based on graph:
        1. single
        2. batch
    These methods returns a dict of Tensors:


    Parameters:
        batch_size: int, batch size of samples
        fields:
            key, shape
    """

    def __init__(self, name):
        super(__class__, self).__init__(name)

        self.register_task('single', self.single)
        self.register_task('batch', self.batch)

    def _load_sample(self, feeds=None):
        raise NotImplementedError

    def _load_dummpy(self, feeds=None):
        raise NotImplementedError

    def single(self, feeds=None):
        try:
            return self._load_sample(feed_dict)
        except StopIteration:
            return self._load_dummpy(feed_dict)

    def batch(self, feeds=None):
        for f in self.param('fields', feeds):
            result[f['key']] = np.zeros()
        for i in range(self.param('batch_size', feeds)):
            next_sample = self.single(feed_dict)
            for k in next_sample:
                result[k][i, ...] = next_sample[k]


class DatasetTFRecords(Graph):
    def __init__(self, name):
        super(__class__, self).__init__(name)
        self._before_processing()
        self.dataset = self._processing(self._load_tfrecord_files())
        self._register_dataset()

    def _before_processing():
        pass

    @classmethod
    def default_config(cls):
        raise NotImplementedError

    def _load_tfrecord_files(self):
        from dxpy.batch import FilesFilter
        from fs.osfs import OSFS
        return tf.contrib.data.TFRecordDataset(self.c['files'])

    def _processing(self, dataset):
        return dataset

    def _register_dataset(self):
        iterator = self.dataset.make_one_shot_iterator()
        next_element = iterator.get_next()
        self.register_main_node(next_element)
        for k in next_element:
            self.register_node(k, next_element[k])

from ..graph import Graph
import numpy as np


class Dataset(Graph):
    """Base class of database
    Database add some special tasks based on graph:
        1. single
        2. batch
    Parameters
        fields:
            key, shape
    """

    def __init__(self, name):
        super(__class__, self).__init__(name)
        self.register_task('single', self.single)
        self.register_task('batch', self.batch)
        self.key_configs = self.key_configs.add('batch_size', 'fields')

    def _refine_config():
        super(__class__, self)._refine_config()
        for f in self.c['fields']:
            self.c['fields'][f]['batch_shape'] = [
                self.c['batch_size']] + list(f['shape'])

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
        result = dict()
        for f in self.c['fields']:
            result[f['key']] = np.zeros()
        for i in range(self.c['batch_size']):
            next_sample = self.single(feed_dict)
            for k in next_sample:
                result[k][i, ...] = next_sample[k]

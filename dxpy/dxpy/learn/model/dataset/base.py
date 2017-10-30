from ..graph import Graph
import numpy as np


class Dataset(Graph):
    """Base class of database
    Database add some special tasks based on graph:
        1. single
        2. batch
        3. next N samples (given N)
        4. next N samples with batch (given N) (list of tensor)

    Parameters 
        fields:
            key, shape        
    """
    required_configs = ['batch_size', 'fields']

    def __init__(self, name):
        super(__class__, self).__init__(name)

    def _load_sample(self, field, *args, **kwargs):
        pass

    def single(self, feed_dict=None, name=None):
        raise NotImplementedError

    def batch(self, feed_dict=None, name=None):
        result = np.zeros(self.c['batch_shape'])
        for i in range(self.c['batch_size']):
            pass

    def up_to_n(self, feed_dict=None, name=None):
        raise NotImplementedError

    def up_to_n_batch(self, feed_dict=None, name=None):
        raise NotImplementedError

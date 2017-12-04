"""
Analytical Phantom Sinogram module, provide examples with fields:
Example:
    'phantom':  scaled clean 256x256 phantom
    'sinogram': scaled clean original sinogram
    'sinogram1x': sinogram without down sampling, may apply poission sample
    'sinogram[2, 4, 8]x': down sampled with [2, 2], [4, 4], [8, 8] respectively
    'phantom[1..4]x': FBP reconstructed image (with 1e6 events) with respetive sinograms
"""
import os
import tensorflow as tf
from tables import *
from dxpy.configs import configurable
import h5py
import numpy as np
from typing import List, TypeVar
from ...config import config
from ...graph import Graph

DEFAULT_FILE_NAME = 'analytical_phantom_sinogram.h5'
NB_IMAGES = 786543


class _AnalyticalPhantomSinogram(IsDescription):
    phantom = UInt16Col(shape=(256, 256))
    sinogram = UInt16Col(shape=(320, 320))
    phantom_type = UInt8Col()


class _AnalyticalPhantomMultiScaleReconstruction(IsDescription):
    recon1x = UInt16Col(shape=(256, 256))
    recon2x = UInt16Col(shape=(256, 256))
    recon4x = UInt16Col(shape=(256, 256))
    recon8x = UInt16Col(shape=(256, 256))


def data_type_np(field_name):
    import tensorflow as tf
    return {
        'phantom': np.float32,
        'sinogram': np.float32,
        'phantom_type': np.int64,
        'recon1x': np.float32,
        'recon2x': np.float32,
        'recon4x': np.float32,
        'recon8x': np.float32,
    }[field_name]


def data_type_tf(field_name):
    import tensorflow as tf
    return {
        'phantom': tf.float32,
        'sinogram': tf.float32,
        'phantom_type': tf.int64,
        'recon1x': tf.float32,
        'recon2x': tf.float32,
        'recon4x': tf.float32,
        'recon8x': tf.float32,
    }[field_name]


def data_shape(field_name):
    import tensorflow as tf
    return {
        'phantom': (256, 256),
        'recon1x': (256, 256),
        'recon2x': (256, 256),
        'recon4x': (256, 256),
        'recon8x': (256, 256),
        'sinogram': (640, 320),
        'phantom_type': (),
    }[field_name]


@configurable(config.get('datasets').get('analytical_phantom_sinogram'))
def _h5files(path: str, sino_fn='analytical_phantom_sinogram.h5', recon_fn='recons.h5'):
    from dxpy.core.path import Path
    return str(Path(path) / sino_fn), str(Path(path) / recon_fn)


def _post_processing(result):
    from dxpy.medical_image_processing.projection.parallel import padding_pi2full
    if 'sinogram' in result:
        result['sinogram'] = padding_pi2full(result['sinogram']).T
    for k in result:
        result[k] = result[k].astype(data_type_np(k))
    return result


def _get_example(idx, fields, h5sino, h5recon):
    result = dict()
    h5sino_keys = ['phantom', 'sinogram']
    for k in h5sino_keys:
        if k in fields:
            result[k] = h5sino.root.data[idx][k]
    h5recon_keys = ['recon1x', 'recon2x', 'recon4x', 'recon8x']
    for k in h5recon_keys:
        if k in fields:
            result[k] = h5recon.root.data[idx][k]
    return result


def dataset_generator(fields=('sinogram'), ids=None):
    if ids is None:
        ids = range(0, int(NB_IMAGES * 0.8))
    fn_sino, fn_recon = _h5files()
    with open_file(fn_sino) as h5sino, open_file(fn_recon) as h5recon:
        for idx in ids:
            result = _get_example(idx, fields, h5sino, h5recon)
            result = _post_processing(result)
            yield result


class Dataset(Graph):
    SINO_STAT = {'mean': 4.88, 'std': 4.68}
    LOG_SINO_STAT = {'mean': 0.0, 'std': 1.0}
    RECON_STAT = {'mean': 0.0, 'std': 1.0}
    LOG_RECON_STAT = {'mean': 0.0, 'std': 1.0}

    @configurable(config, with_name=True)
    def __init__(self, name='analytical_phantom_sinogram_dataset', *,
                 batch_size=32, fields=('sinogram', ), ids=None, shuffle=True):
        super().__init__(name, batch_size=batch_size,
                         ids=ids, fields=fields, shuffle=shuffle)
        dataset = self._create_dataset()
        self.dataset = self._processing(dataset)
        self._register_dataset()

    def _create_dataset(self):
        from functools import partial
        dataset_gen_partial = partial(dataset_generator,
                                      fields=self.param('fields'),
                                      ids=self.param('ids', raise_key_error=False))
        output_types = {k: data_type_tf(k) for k in self.param('fields')}
        output_shapes = {k: data_shape(k) for k in self.param('fields')}
        return tf.data.Dataset.from_generator(dataset_gen_partial, output_types, output_shapes)

    def _format_tensors(self, data):
        return {k: tf.reshape(tf.cast(data[k], data_type_tf(k)), data_shape(k)) for k in data}

    def _processing(self, dataset):
        dataset = (dataset
                   .repeat()
                   .map(self._format_tensors))
        if self.param('shuffle'):
            dataset = dataset.shuffle(1024)
        return dataset.batch(self.param('batch_size'))

    def _register_dataset(self):
        iterator = self.dataset.make_one_shot_iterator()
        next_element = iterator.get_next()
        self.register_main_node(next_element)
        for k in self.param('fields'):
            self.register_node(k, next_element[k])

    def data_shape(self, key):
        return data_shape(key)



# The following part is a record of dataset generator script.


# def create_dataset_from_tf_records():
#     from tqdm import tqdm
#     from dxpy.learn.dataset.config import config
#     filename = '/media/hongxwing/73f574f4-33b0-46b1-ae5d-de1eca4ef891/home/hongxwing/Workspace/Datas/phantom_sinograms_3.h5'
#     with h5py.File(filename, 'r') as fin:
#         filters = Filters(5, 'blosc')
#         h5file = open_file(str(Path(config['PATH_DATASETS']) / DEFAULT_FILE_NAME),
#                            mode="w", filters=filters)
#         table = h5file.create_table(
#             h5file.root, 'data', AnalyticalPhantomSinogram, expectedrows=fin['phantoms'].shape[0])
#         data = table.row

#         def convert_to_uint16(arr):
#             UINT16MAX = 65535
#             arr = np.maximum(arr, 0.0)
#             arr = arr / np.max(arr) * UINT16MAX
#             arr = np.minimum(arr, UINT16MAX)
#             return arr.astype(np.uint32)

#         for i in tqdm(range(fin['phantoms'].shape[0]), ascii=True):
#             data['sinogram'] = convert_to_uint16(
#                 fin['sinograms'][i, :, :320, 0])
#             data['phantom'] = convert_to_uint16(fin['phantoms'][i, :, :, 0])
#             data['phantom_type'] = np.reshape(np.array(fin['types'][i, ...],
#                                                        dtype=np.uint8), [])
#             data.append()
#     table.flush()
#     h5file.close()


# if __name__ == "__main__":
#     create_dataset_from_tf_records()

import os
from tables import *
from dxpy.core.path import Path
from dxpy.configs import configurable
import h5py
import numpy as np
DEFAULT_FILE_NAME = 'analytical_phantom_sinogram.h5'


class AnalyticalPhantomSinogram(IsDescription):
    phantom = UInt16Col(shape=(256, 256))
    sinogram = UInt16Col(shape=(320, 320))
    phantom_type = UInt8Col()


def h5filename():
    from ..config import config
    return str(Path(config['PATH_DATASETS']) / DEFAULT_FILE_NAME)

def data(fields=('phantom', 'sinogram'), filename=None):
    # with open_file('/tmp/aps.h5') as h5file:
    with open_file(h5filename()) as h5file:
        for d in h5file.root.data.iterrows():
            for k in fields:
                yield {k: d[k]}

def tfdata():
    import tensorflow as tf
    pass

def create_dataset_from_tf_records():
    from tqdm import tqdm
    from dxpy.learn.dataset.config import config
    filename = '/media/hongxwing/73f574f4-33b0-46b1-ae5d-de1eca4ef891/home/hongxwing/Workspace/Datas/phantom_sinograms_3.h5'
    with h5py.File(filename, 'r') as fin:
        filters = Filters(5, 'blosc')
        h5file = open_file(str(Path(config['PATH_DATASETS']) / DEFAULT_FILE_NAME),
                           mode="w", filters=filters)
        table = h5file.create_table(
            h5file.root, 'data', AnalyticalPhantomSinogram, expectedrows=fin['phantoms'].shape[0])
        data = table.row

        def convert_to_uint16(arr):
            UINT16MAX = 65535
            arr = np.maximum(arr, 0.0)
            arr = arr / np.max(arr) * UINT16MAX
            arr = np.minimum(arr, UINT16MAX)
            return arr.astype(np.uint32)

        for i in tqdm(range(fin['phantoms'].shape[0]), ascii=True):
            data['sinogram'] = convert_to_uint16(
                fin['sinograms'][i, :, :320, 0])
            data['phantom'] = convert_to_uint16(fin['phantoms'][i, :, :, 0])
            data['phantom_type'] = np.reshape(np.array(fin['types'][i, ...],
                                                       dtype=np.uint8), [])
            data.append()
    table.flush()
    h5file.close()


if __name__ == "__main__":
    create_dataset_from_tf_records()

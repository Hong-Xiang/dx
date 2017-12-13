import h5py
import tensorflow as tf
import numpy as np
from tqdm import tqdm

class HDF5Converter:
    def __init__(self, source, keys=None):
        self.source = source
        with h5py.File(source) as fin:
            h5_keys = list(fin.keys())
        self.keys = keys or h5_keys

    def dataset(self, h5py_file, key):
        if isinstance(key, str):
            key = [key]
        dataset = h5py_file
        for k in key:
            dataset = dataset[k]
        return dataset

    def nb_examples(self):
        with h5py.File(self.source) as fin:
            shape = self.dataset(fin, self.keys[0]).shape
        return shape[0]

    def check_shapes(self):
        print("Checking shape of {}...".format(self.source))
        succeed = True
        with h5py.File(self.source) as fin:
            nb_examples = self.nb_examples()
            for k in self.keys:
                shape = self.dataset(fin, k).shape
                if shape[0] != nb_examples:
                    succeed = False
                print("dataset:", k, "shape:", shape)
        if not succeed:
            raise ValueError("Shape check failed!")
        print('Succeed!')

    def _float_feature(self, value):
        return tf.train.Feature(float_list=tf.train.FloatList(value=value))

    def _bytes_feature(self, value):
        bytes_list = value.tostring()
        return tf.train.Feature(bytes_list=tf.train.BytesList(value=[bytes_list]))

    def _int64_feature(self, value):
        return tf.train.Feature(int64_list=tf.train.Int64List(value=value))

    def convert(self, filename):
        self.check_shapes()
        writer = tf.python_io.TFRecordWriter(filename)
        with h5py.File(self.source) as fin:
            nb_examples = self.nb_examples()
            feature_func = dict()
            for k in self.keys:
                if self.dataset(fin, k).dtype == np.uint8:
                    feature_func[k] = self._bytes_feature
                elif self.dataset(fin, k).dtype in [np.float16, np.float32, np.float8, np.float64]:
                    feature_func[k] = self._float_feature
                elif self.dataset(fin, k).dtype in [np.int16, np.int32, np.int64]:
                    feature_func[k] = self._int64_feature
            for i in tqdm(range(nb_examples)):
                example = tf.train.Example(features=tf.train.Features(feature={
                    k: feature_func[k](self.dataset(fin, k)[i, ...])
                    for k in self.keys}))
                writer.write(example.SerializeToString())
            writer.close()

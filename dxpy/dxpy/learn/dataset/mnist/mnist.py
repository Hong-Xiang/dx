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
        dataset = dataset.map(self._parse_example)
        image = dataset['image']
        shape = dataset['shape']
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


from ..base import Graph


class MNISTLoadAll(Graph):
    def __init__(self, name, **config):
        super(__class__, self).__init__(name, **config)
        self.register_main_node(self.__load_data())
        self.register_node('image', self.as_tensor()['image'])
        self.register_node('label', self.as_tensor()['label'])

    def __load_data(self):
        from tensorflow.examples.tutorials.mnist import input_data
        from tensorflow.contrib.data import Dataset
        mnist = input_data.read_data_sets(
            '/home/hongxwing/Datas/mnist/tfdefault', one_hot=True)
        images = mnist.train.images
        label = mnist.train.labels

        # def gen_image():            
        #     for i in range(images.shape[0]):
        #         yield {'image': images[i, ...], 'label': label[i, ...]}
        
        dataset_image = Dataset.from_tensor_slices(images).map(
            lambda img: tf.reshape(img, [28, 28, 1]))
        dataset_label = Dataset.from_tensor_slices(label)
        dataset = Dataset.zip({'image': dataset_image, 'label': dataset_label})

        dataset = Dataset.from_gener
        dataset = dataset.batch(32).repeat()
        iterator = dataset.make_one_shot_iterator()
        next_element = iterator.get_next()
        return next_element

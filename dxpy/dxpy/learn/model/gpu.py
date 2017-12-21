import tensorflow as tf
from ..config import config
from dxpy.configs import configurable


def _split_feeds(feeds, nb_gpu):
    from .tensor import MultiGPUSplitor, PlaceHolder
    mgs = MultiGPUSplitor(nb_gpu=nb_gpu)
    feeds_gpus = mgs(feeds)
    first_part = list(feeds_gpus.values())[0]
    with tf.name_scope('cpu_placeholders'):
        cpu_placeholders = {k: PlaceHolder(
            first_part[k]).as_tensor() for k in first_part}
    return feeds_gpus, mgs.part_names(), cpu_placeholders


def _apply_on_gpus(model, feeds_gpu, part_names):
    result_gpus = {}
    for i, k in enumerate(part_names):
        with tf.device(device_name('gpu', i)):
            result_gpus[k] = model(feeds_gpus[k])
    return result_gpus


def _merge(result_gpus, part_names):
    with tf.device(device_name('cpu')):
        with tf.name_scope('merge'):
            with tf.name_scope('inference'):
                infer = tf.concat([result_gpus[k][NodeKeys.INFERENCE]
                                   for k in part_names], axis=0)
            losses = [result_gpus[k][NodeKeys.LOSS]
                      for k in part_names]
            with tf.name_scope('total_loss'):
                loss = tf.add_n(losses)
    return {NodeKeys.INFERENCE: infer,
            NodeKeys.LOSS: losses,
            NodeKeys.EVALUATE: loss}


def apply_multi_gpu(feeds, model_func, nb_gpu=None):
    if nb_gpu is None:
        nb_gpu = config['nb_gpu']
    feeds_gpus, part_names, cpu_placeholders = _split_feeds(feeds, nb_gpu)
    with tf.device(device_name('cpu')):
        model = model_func(cpu_placeholders)
        model()
    result_gpus = _apply_on_gpus(model, feeds_gpu, part_names)
    return _merge(result_gpus, part_names)


class MultiGPUSplitor(Model):
    """
    A Helper class to create
    """
    @configurable(config.get('gpu'))
    def __init__(self, name='gpu_splitor', nb_gpu=2):
        super().__init__(name, nb_gpu=nb_gpu)

    @classmethod
    def _default_config(cls):
        result = dict()
        result.update(super()._default_config())
        result.update({
            'lazy_create': True,
            'register_inputs': False,
            'register_outputs': False,
            'format': 'split'
        })
        return result

    def _kernel(self, feeds):
        from dxpy.collections.dicts import swap_dict_hierarchy
        result = {k: self._slice_tensor_for_gpu(feeds[k]) for k in feeds}
        if self.param('format') == 'name':
            return result
        else:
            return swap_dict_hierarchy(result)

    def _get_shape_split(self, shape):
        if isinstance(shape, tf.TensorShape):
            shape_gpu = shape.as_list()
        else:
            shape_gpu = list(shape)
        if shape_gpu[0] is None:
            raise TypeError("Batch size can not be None for MultiGPUSplitor.")
        shape_gpu[0] = shape_gpu[0] // self.param('nb_gpu')
        return shape_gpu

    def _slice_tensor_for_gpu(self, tensor_input):
        result = dict()
        shape_gpu = self._get_shape_split(tensor_input.shape)
        with tf.name_scope(self._get_tensor_name(tensor_input.name)):
            for id_slice in range(self.param('nb_gpu')):
                with tf.device(device_name('gpu', id_slice)):
                    slice_start = [id_slice * shape_gpu[0]] + \
                        [0] * (len(shape_gpu) - 1)
                    name = 'part_{}'.format(id_slice)
                    result[name] = tf.slice(tensor_input, slice_start,
                                            shape_gpu, name=name)
        if len(result) == 0:
            return tensor_input
        return result

    def part_names(self):
        return ['part_{}'.format(id_slice) for id_slice in range(self.param('nb_gpu'))]

    def _get_tensor_name(self, name):
        prefix, idt = name.split(':')
        idt = int(idt)
        if idt == 0:
            return prefix
        else:
            return '{}_{}'.format(prefix, idt)

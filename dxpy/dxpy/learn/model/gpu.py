import tensorflow as tf
from ..config import config


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

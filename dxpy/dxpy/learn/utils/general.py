def device_name(device_type, device_id=None):
    if device_id is None:
        device_id = 0
    return '/{t}:{i}'.format(t=device_type, i=device_id)


def refined_tensor_or_graph_name(tensor_or_graph):
    import tensorflow as tf
    if isinstance(tensor_or_graph, tf.Tensor):
        return tensor_or_graph.name.replace(':', '_')
    return tensor_or_graph.name

def pre_work(device=None):
    import tensorflow as tf
    from dxpy.learn.scalar import create_global_scalars
    if device is None:
        create_global_scalars()
    else:
        with tf.device(device):
            create_global_scalars()

def load_yaml_config(filename='dxln.yml'):
    from ..config import config
    import yaml
    with open(filename) as fin:
        cfg = yaml.load(fin)
    config.update(cfg)
    if 'include' in cfg:
        for f in cfg['include']:
            with open(f) as fin:
                cfg_i = yaml.load(fin)
                config.update(cfg_i)

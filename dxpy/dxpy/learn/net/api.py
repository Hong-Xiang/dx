from dxpy.configs import configurable
from dxpy.learn.config import config
from dxpy.core.path import Path


@configurable(config, with_name=True)
def get_network(name, dataset, network_cls_name, network_name=None, **kw):
    from .base import NodeKeys
    if network_name is None:
        network_name = name
    if network_cls_name == 'srms':
        from .zoo.srms import SRMultiScale
        return SRMultiScale(name=network_name, inputs=dataset, **kw)
    elif network_cls_name == 'sin':
        from .zoo.sin import SinNet
        return SinNet(name=name, inputs={NodeKeys.INPUT: dataset['x'], NodeKeys.LABEL: dataset['y']}, **kw)

    else:
        raise ValueError(
            'Unknown network name (class name) {}.'.format(dataset_cls_name))

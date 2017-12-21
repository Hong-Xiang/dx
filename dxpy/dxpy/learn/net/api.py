from dxpy.configs import configurable
from dxpy.learn.config import config
from dxpy.core.path import Path


@configurable(config, with_name=True)
def get_network(name, dataset, network_cls_name, network_name=None, **kw):
    from .base import NodeKeys, Graph
    if network_name is None:
        network_name = name
    if network_cls_name == 'srms':
        from .zoo.srms import SRMultiScale
        if not isinstance(dataset, (dict, Graph)):
            raise TypeError('srms network required dataset, got {}.'.format(dataset))
        # valid_keys = ['input/image{}'.format(2**i) for i in range(10)]
        # valid_keys += ['label/image{}'.format(2**i) for i in range(10)]
        # inputs = dict()
        inputs = dataset
        # for k in valid_keys:
        # if k in dataset.nodes:
        # inputs[k] = dataset[k]
        return SRMultiScale(name=network_name, inputs=inputs, **kw)
    elif network_cls_name == 'sin':
        from .zoo.sin import SinNet
        return SinNet(name=name, inputs={NodeKeys.INPUT: dataset['x'], NodeKeys.LABEL: dataset['y']}, **kw)

    else:
        raise ValueError(
            'Unknown network name (class name) {}.'.format(dataset_cls_name))

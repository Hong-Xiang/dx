from dxpy.configs import configurable
from dxpy.learn.config import config
from dxpy.core.path import Path


@configurable(config, with_name=True)
def get_dataset(name, dataset_cls_name, dataset_name=None):
    if dataset_cls_name == 'sraps':
        if dataset_name is None:
            dataset_name = name
        from .zoo.sraps import AnalyticalPhantomSinogramDatasetForSuperResolution 
        return AnalyticalPhantomSinogramDatasetForSuperResolution(name=dataset_name)
    else:
        raise ValueError(
            'Unknown dataset_name (class name) {}.'.format(dataset_cls_name))

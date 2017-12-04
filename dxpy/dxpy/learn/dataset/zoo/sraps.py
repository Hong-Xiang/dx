"""
Super resolution dataset for analytical phantom sinogram dataset
"""
from dxpy.configs import configurable
from ...config import config
from ..raw.analytical_phantom_sinogram import Dataset
from ...graph import Graph, NodeKeys


class AnalyticalPhantomSinogramDatasetForSuperResolution(Graph):
    @configurable(config, with_name=True)
    def __init__(self, name='dataset/apssr',
                   image_type: str,
                   *,
                   log_sinogram: bool,
                   poission_noise: bool=True,
                   target_shape: typing.List[int]=None):
    """
    Args:
        -   image_type: 'sinogram' or 'image'
        -   batch_size
    Returns:
        a `Graph` object, which has several nodes:
    Raises:
    """
    from ...model.normalizer.normalizer import FixWhite, ReduceSum
    from ...model.tensor import ShapeEnsurer
    from dxpy.core.path import Path
    name = Path(name)
    if image_type == 'sinogram':
        fields = ['sinogram']
    else:
        fields = ['phantom'] + ['recon{}x'.format(2**i) for i in range(nb_down_sample+1)]
    with tf.name_scope('aps_{img_type}_dataset'.format(img_type=image_type)):
        dataset_origin = Dataset(name/'origin_dataset', batch_size=batch_size,
                    fields=fields, ids=ids , shuffle=shuffle)
        if image_type == 'sinogram':
            return self._process_sinogram(dataset_origin)
        else:
            return self._process_recons(dataset_origin)
      
    def _process_sinogram(self, dataset, log_sinogram, poission_noise, fixed_event, nb_down_sample, target_shape, batch_size):
        from ...model.normalizer.normalizer import ReduceSum, FixWhite
        if log_sinogram:
            stat = dataset.LOG_SINO_STAT
        else:
            stat = dataset.SINO_STAT
        dataset = ReduceSum(self.name / 'reduce_sum', dataset['sinogram'],
                            fixed_summation_value=1e6).as_tensor()
        if poission_noise:
            with tf.name_scope('add_poission_noise'):
                dataset = tf.random_poisson(dataset, shape=[])
        if log_sinogram:
            dataset = tf.log(dataset)
        dataset = FixWhite(name=name / 'fix_white',
                        inputs=dataset, mean=stat['mean'], std=stat['std'])
        dataset = tf.random_crop(dataset,
                                [batch_size] + list(target_shape) + [1])
        dataset = SuperResolutionDataset('dataset/super_resolution',
                                        lambda: {'image': dataset},
                                        input_key='image')
        return dataset

    def _process_recons(self, dataset):
        raise NotImplementedError
        return dataset



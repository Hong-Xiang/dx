import tensorflow as tf
from dxpy.configs import configurable
from dxpy.learn.config import config



@configurable(config, with_name=True)
def start_dataset_server(cluster_spec_file='cluster.yml', job_name='dataset', task_index=0, dataset_name=None, name='cluster/dataset/task0'):
    """
    Args:
        func: functions which returns dataset
    """
    from .cluster import get_cluster_spec
    cluster = tf.train.ClusterSpec(get_cluster_spec(cluster_spec_file))
    server = tf.train.Server(cluster, job_name=job_name, task_index=task_index)
    get_dist_dataset(name=name)
    server.join()

@configurable(config, with_name=True)
def get_dist_dataset(job_name='dataset', task_index=0, dataset_name=None, name='cluster/dataset/task0'):
    from dxpy.learn.dataset import get_dataset
    with tf.device('/job:{}/task:{}'.format(job_name, task_index)):
        dataset = get_dataset(name=dataset_name)
    return dataset

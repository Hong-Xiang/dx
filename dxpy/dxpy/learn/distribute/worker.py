import tensorflow as tf
from dxpy.configs import configurable
from dxpy.learn.config import config



# @configurable(config, with_name=True)
# def start_parameter_server(cluster_spec_file='cluster.yml', job_name='ps', task_index=0, network_name=None, dataset_cluster_name=None, name='cluster/ps/task0'):
#     """
#     Args:
#         func: functions which returns dataset
#     """
#     from .cluster import get_cluster_spec
#     from .dataset import get_dist_dataset
#     cluster = tf.train.ClusterSpec(get_cluster_spec(cluster_spec_file))
#     server = tf.train.Server(cluster, job_name=job_name, task_index=task_index)
#     dataset = get_dist_dataset(name=dataset_cluster_name) 
#     network = get_dist_network(name=name, dataset=dataset)
#     server.join()

@configurable(config, with_name=True)
def get_dist_network(job_name='dataset', task_index=0, network_config=None, dataset=None, name='cluster/ps/task0'):
    if network_config is None:
        network_config = name
    from dxpy.learn.net.api import get_network
    with tf.device('/job:{}/task:{}'.format(job_name, task_index)):
        network = get_network(name=network_config, dataset=dataset, reuse=True)
    return network

@configurable(config, with_name=True)
def apply_dist_network(job_name='dataset', task_index=0, network=None, dataset=None, name='cluster/ps/task0'):
    with tf.device('/job:{}/task:{}'.format(job_name, task_index)):
        return network(dataset)



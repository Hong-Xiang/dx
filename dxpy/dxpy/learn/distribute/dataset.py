import tensorflow as tf
from dxpy.configs import configurable
from dxpy.learn.config import config

@configurable(config, with_name=True)
def start_dataset_server(func, ip, port, job_name='dataset', task_index=0, name='cluster/dataset/task0'):
    """
    Args:
        func: functions which returns dataset
    """
    cluster = tf.train.ClusterSpec({job_name: ["{}:{}".format(ip, port)]})
    server = tf.train.Server(cluster, job_name=job_name, task_index=task_index)
    with tf.device('/job:{}/task:{}'.format(job_name, task_index)):
        dataset = func()
    server.join()




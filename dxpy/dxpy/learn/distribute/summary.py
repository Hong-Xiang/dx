import tensorflow as tf
from dxpy.configs import configurable
from dxpy.learn.config import config





@configurable(config, with_name=True)
def get_dist_summary(tensors, job_name='dataset', task_index=0, summary_config=None, name='cluster/ps/task0'):
    from dxpy.learn.train.summary_2 import SummaryWriter
    with tf.device('/job:{}/task:{}'.format(job_name, task_index)):
        sw = SummaryWriter(tensors=tensors, name=summary_config)
    return sw


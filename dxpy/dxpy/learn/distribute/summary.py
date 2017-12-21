import tensorflow as tf
from dxpy.configs import configurable
from dxpy.learn.config import config


@configurable(config, with_name=True)
def get_dist_summary(tensors, network=None, job_name='dataset', task_index=0, summary_cls_name=None, summary_config=None, name='cluster/ps/task0'):
    from dxpy.learn.train.summary_2 import SummaryWriter
    from dxpy.learn.net.zoo.srms.summ import SRSummaryWriter_v2
    with tf.device('/job:{}/task:{}'.format(job_name, task_index)):
        if summary_cls_name is None:
            sw = SummaryWriter(tensors=tensors, name=summary_config)
        elif summary_cls_name == 'srms':
            sw = SRSummaryWriter_v2(network=network, tensors=tensors, name=summary_config)

    return sw

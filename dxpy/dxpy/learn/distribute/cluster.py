from dxpy.configs import configurable
from dxpy.learn.config import config
import tensorflow as tf
import yaml


def get_cluster_spec(config_filename, job_name=None):
    return tf.train.ClusterSpec(get_cluster_spec_raw(config_filename, job_name))

def get_cluster_spec_raw(config_filename, job_name=None):
    with open(config_filename) as fin:
        spec = yaml.load(fin)
    result = dict()
    for job_name in spec:
        result[job_name] = ["{}:{}".format(v['ip'], v['port']) for v in spec[job_name]]
    if job_name == 'dataset':
        valid_keys = ['dataset']
    elif job_name == 'ps':
        valid_keys = ['ps', 'dataset']
    elif job_name == 'worker':
        valid_keys = ['ps', 'dataset', 'worker']
    elif job_name in ['summary', 'saver']:
        valid_keys = ['ps', 'dataset', job_name]
    else:
        valid_keys = list(result.keys())
    # result = {k: result[k] for k in valid_keys}
    return result

def get_nb_tasks(cluster_filename, job_name):
    cfg = get_cluster_spec_raw(cluster_filename)
    return len(cfg[job_name])

def get_server(cluster_spec, job_name, task_index=0, config=None):
    if isinstance(cluster_spec, dict):
        cluster_spec = tf.train.ClusterSpec(cluster_spec)
    cluster = tf.train.ClusterSpec(cluster_spec)
    server = tf.train.Server(cluster, job_name, task_index, config=config)
    return server



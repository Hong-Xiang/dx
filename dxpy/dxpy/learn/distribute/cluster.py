from dxpy.configs import configurable
from dxpy.learn.config import config
import tensorflow as tf
import yaml


def get_cluster_spec(config_filename):
    return tf.train.ClusterSpec(get_cluster_spec_raw(config_filename))

def get_cluster_spec_raw(config_filename):
    with open(config_filename) as fin:
        spec = yaml.load(fin)
    result = dict()
    for job_name in spec:
        result[job_name] = ["{}:{}".format(v['ip'], v['port']) for v in spec[job_name]]
    return result

def get_nb_tasks(cluster_filename, job_name):
    cfg = get_cluster_spec_raw(cluster_filename)
    return len(cfg[job_name])

def get_server(cluster_spec, job_name, task_index=0):
    if isinstance(cluster_spec, dict):
        cluster_spec = tf.train.ClusterSpec(cluster_spec)
    cluster = tf.train.ClusterSpec(cluster_spec)
    server = tf.train.Server(cluster, job_name, task_index)
    return server



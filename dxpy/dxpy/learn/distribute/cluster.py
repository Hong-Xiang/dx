from dxpy.configs import configurable
from dxpy.learn.config import config
import yaml

def get_cluster_spec(config_filename):
    with open(config_filename) as fin:
        spec = yaml.load(fin)
    result = dict()
    for job_name in spec:
        result[job_name] = ["{}:{}".format(v['ip'], v['port']) for v in spec[job_name]]
    return result

def get_server(cluster_spec, job_name, task_index=0):
    import tensorflow as tf
    cluster = tf.train.ClusterSpec(cluster_spec)
    server = tf.train.Server(cluster, job_name, task_index)
    return server



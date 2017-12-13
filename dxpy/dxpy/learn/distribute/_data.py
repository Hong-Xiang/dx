import tensorflow as tf

# cluster = tf.train.ClusterSpec({"local": ["localhost:2222", "localhost:2223"]})
cluster = tf.train.ClusterSpec({"local": ["localhost:2222"]})
server = tf.train.Server(cluster, job_name="local", task_index=0)

from dxpy.learn.dataset.zoo.sraps import AnalyticalPhantomSinogramDatasetForSuperResolution
from dxpy.config import config
import yaml

with open('dxln.yml') as fin:
    cfg = yaml.load(fin)
config.update(cfg)

with tf.device('/job:local/task:0'):
    dataset = AnalyticalPhantomSinogramDatasetForSuperResolution()
    sinos = dataset['input/image1x']
server.join()
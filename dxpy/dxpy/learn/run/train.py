from pprint import pprint

import numpy as np
import tensorflow as tf
from dxpy.learn.session import Session
from dxpy.learn.train.summary import SummaryWriter
from dxpy.learn.utils.general import pre_work
from tqdm import tqdm
from dxpy.learn.config import config
import yaml
from dxpy.configs import configurable, ConfigsView


@configurable(ConfigsView(config).get('train'))
def get_train_configs(summary_freq=1000, save_freq=10000, steps=100000000):
    return {'summary_freq': summary_freq,
            'save_freq': save_freq,
            'steps': steps}


def train(definition_func):
    with open('dxln.yml') as fin:
        ycfg = yaml.load(fin)
    config.update(ycfg)
    pre_work()
    train_cfgs = get_train_configs()
    steps = train_cfgs['steps']
    summary_freq = train_cfgs['summary_freq']
    save_freq = train_cfgs['save_freq']
    network, summary = definition_func(ycfg)
    session = Session()
    with session.as_default():
        network.post_session_created()
        summary.post_session_created()
        session.post_session_created()

    with session.as_default():
        network.load()
        for i in tqdm(range(steps)):
            network.train()
            if i % summary_freq == 0 and i > 0:
                summary.summary()
                summary.flush()
            if i % save_freq == 0 and i > 0:
                network.save()

    with session.as_default():
        network.save()


def train_dist(definition_func):
    from dxpy.learn.utils.general import load_yaml_config
    load_yaml_config('dxln.yml')


@configurable(config, with_name=True)
def train_task_dist(cluster, dataset_maker_name, network_maker_name, summary_maker_name, job_name, task_index, name, id_gpu=None):
    import os
    if id_gpu is not None:
        os.environ['CUDA_VISIBLE_DEVICES'] = '"{}"'.format(id_gpu)
    from dxpy.learn.distribute.cluster import get_server
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    server = get_server(cluster, job_name, task_index, config=config)
    if job_name == 'ps':
        server.join()
    elif job_name == 'worker':
        with tf.device(tf.train.replica_device_setter(worker_device="/job:worker/task:{}".format(task_index), cluster=cluster)):
            _, network, _ = create_dataset_network_summary(dataset_maker_name,
                                                           network_maker_name,
                                                           summary_maker_name)
            train_with_monitored_session(network,
                                         target=server.target,
                                         is_chief=(task_index == 0))


def create_dataset_network_summary(dataset_maker_name, network_maker_name, summary_maker_name):
    from dxpy.learn.dataset.api import get_dataset
    from dxpy.learn.net.api import get_network, get_summary
    dataset = get_dataset(dataset_maker_name)
    network = get_network(network_maker_name, dataset=dataset)
    result = network()
    summary = get_summary(summary_maker_name, dataset, network, result)
    return dataset, network, summary


def train_task_local(dataset_maker_name, network_maker_name, summary_maker_name):
    _, network, _ = create_dataset_network_summary(dataset_maker_name,
                                                   network_maker_name,
                                                   summary_maker_name)
    train_with_monitored_session(network)


def train_with_monitored_session(network, is_chief=True, target=None, steps=10000000000000):
    from dxpy.learn.utils.general import pre_work
    from dxpy.learn.session import set_default_session
    from tqdm import tqdm
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    hooks = [tf.train.StepCounterHook()]
    with tf.train.MonitoredTrainingSession(master=target, config=config, checkpoint_dir='./save', hooks=hooks, is_chief=is_chief) as sess:
        set_default_session(sess)
        network.nodes['trainer'].run('set_learning_rate')
        for _ in tqdm(range(steps)):
            network.train()

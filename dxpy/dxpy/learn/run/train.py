from pprint import pprint

import numpy as np
import tensorflow as tf
from dxpy.learn.session import Session
from dxpy.learn.train.summary import SummaryWriter
from dxpy.learn.utils.general import pre_work
from tqdm import tqdm
from dxpy.learn.config import config
import yaml

def train(definition_func):
    with open('dxln.yml') as fin:
        ycfg = yaml.load(fin)
    config.update(ycfg)
    pre_work()
    network, summary = definition_func(ycfg)
    session = Session()
    with session.as_default():
        network.post_session_created()
        summary.post_session_created()
        session.post_session_created()

    with session.as_default():
        network.load()
        for i in tqdm(range(ycfg['train']['steps'])):
            network.train()
            if i % 1000 == 0:
                summary.summary()
                summary.flush()
            if i % 10000 == 0 and i > 0:
                network.save()

    with session.as_default():
        network.save()


from pprint import pprint

import numpy as np
import tensorflow as tf
import logging
from dxpy.learn.dataset.zoo.sraps import AnalyticalPhantomSinogramDatasetForSuperResolution
from dxpy.learn.graph import NodeKeys
from dxpy.learn.net.zoo.srms import SRMultiScale
from dxpy.learn.session import Session
from dxpy.learn.train.summary import SummaryWriter
from dxpy.learn.utils.general import pre_work
from dxpy.learn.model.cnn.super_resolution import SuperResolutionMultiScale, BuildingBlocks
from tqdm import tqdm
from dxpy.learn.config import config
import yaml


with open('dxln.yml') as fin:
    ycfg = yaml.load(fin)
config.update(ycfg)
logging.info('LOADED CONFIGS:')
logging.info(config)
dataset = AnalyticalPhantomSinogramDatasetForSuperResolution()
logging.info('Dataset initialized.')
pre_work()
inputs = {}
for i in range(dataset.param('nb_down_sample') + 1):
    inputs.update({'input/image{}x'.format(2**i): dataset['input/image{}x'.format(2**i)]})
    if ycfg['use_noise_label']:
        inputs.update({'label/image{}x'.format(2**i): dataset['input/image{}x'.format(2**i)]})
    else:
        inputs.update({'label/image{}x'.format(2**i): dataset['label/image{}x'.format(2**i)]})
#     if i < 3:
#         inputs.update({'label/image{}x'.format(2**i)                       : dataset['image{}x'.format(2**i)]})
# images = [dataset['image{}x'.format(2**i)] for i in range(dataset.param('nb_down_sample') + 1)]
# inputs = SuperResolutionMultiScale.multi_scale_input(images)
network = SRMultiScale(inputs, name='network')
summary = SummaryWriter(
    name='train', tensors_to_summary=network.summary_items(), path='./summary/train')
session = Session()
with session.as_default():
    network.post_session_created()
    summary.post_session_created()
    session.post_session_created()

with session.as_default():
    network.load()
    for i in tqdm(range(ycfg['train']['steps'])):
        network.train()
        if i % 10 == 0:
            summary.summary()
        if i % 100 == 0:
            summary.flush()
        if i % 1000 == 0:
            network.save()

with session.as_default():
    network.save()

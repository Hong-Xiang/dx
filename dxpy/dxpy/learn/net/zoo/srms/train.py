from pprint import pprint

import numpy as np
import tensorflow as tf

from dxpy.learn.dataset.zoo.srpet import pet_image_super_resolution_dataset
from dxpy.learn.graph import NodeKeys
from dxpy.learn.net.zoo.srms import SRMultiScale
from dxpy.learn.session import Session
from dxpy.learn.train.summary import SummaryWriter
from dxpy.learn.utils.general import pre_work

from tqdm import tqdm

dataset = pet_image_super_resolution_dataset(
    'ana', 'sinogram', 32 * 3, 3, target_shape=[160, 320])
pre_work()
inputs = {}
for i in range(4):
    inputs.update({'input/image{}x'.format(2**i)                   : dataset['image{}x'.format(2**i)]})
    if i < 3:
        inputs.update({'label/image{}x'.format(2**i)                       : dataset['image{}x'.format(2**i)]})
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
    for i in tqdm(range(10000)):
        network.train()
        if i % 10 == 0:
            summary.summary()
        if i % 100 == 0:
            summary.flush()
            network.save()

with session.as_default():
    network.save()

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
from .summ import SRSummaryWriter
from dxpy.learn.run.train import train

def train_defs(external_configs):
    dataset = AnalyticalPhantomSinogramDatasetForSuperResolution()
    inputs = {}
    for i in range(dataset.param('nb_down_sample') + 1):
        inputs.update({'input/image{}x'.format(2**i): dataset['input/image{}x'.format(2**i)]})
        if external_configs['use_noise_label']:
            inputs.update({'label/image{}x'.format(2**i): dataset['input/image{}x'.format(2**i)]})
        else:
            inputs.update({'label/image{}x'.format(2**i): dataset['label/image{}x'.format(2**i)]})
            if dataset.param('image_type') == 'image':
                inputs['label/image1x'] = dataset['label/phantom']
    network = SRMultiScale(inputs, name='network')
    summary = SRSummaryWriter(name='summary/train', network=network)
    return network, summary
    
def main():
    train(train_defs)


if __name__ == "__main__":
    main()
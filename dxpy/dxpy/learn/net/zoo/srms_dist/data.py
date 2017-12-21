from pprint import pprint

import numpy as np
import tensorflow as tf
from dxpy.learn.dataset.zoo.sraps import AnalyticalPhantomSinogramDatasetForSuperResolution
from dxpy.learn.train.summary import SummaryWriter
from dxpy.learn.utils.general import pre_work
from dxpy.learn.model.cnn.super_resolution import SuperResolutionMultiScale, BuildingBlocks
from tqdm import tqdm
from dxpy.learn.utils.general import load_yaml_config

def dataset():
    load_yaml_config('dxln.yml')
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
    return inputs
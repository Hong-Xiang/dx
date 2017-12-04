#import ptvsd
#ptvsd.enable_attach("ptvsd", address = ('0.0.0.0', 3000))

# Enable the line of source code below only if you want the application to wait until the debugger has attached to it
#ptvsd.wait_for_attach()

import tensorflow as tf
import numpy as np
from dxpy.learn.utils.debug import dummy_image, write_graph
from dxpy.learn.model.cnn.super_resolution import SuperResolutionBlock, SRKeys
from dxpy.learn.graph import NodeKeys
with tf.device('/gpu:1'):
    image = dummy_image()
    label = dummy_image(shape=[14, 14])
    reps = dummy_image(shape=[14, 14], nb_channel=32)
    m = SuperResolutionBlock('srb', {NodeKeys.INPUT: image, NodeKeys.LABEL: label})
    result = m()
    write_graph()
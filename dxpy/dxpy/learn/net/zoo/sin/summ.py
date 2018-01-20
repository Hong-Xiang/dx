from dxpy.configs import configurable
from dxpy.learn.config import config
from dxpy.learn.train.summary_2 import SummaryWriter
from dxpy.learn.graph import NodeKeys
import tensorflow as tf


class SinSummaryWriter(SummaryWriter):
    @configurable(config, with_name=True)
    def __init__(self, network, name='summary', **kw):
        summary_tensors = {
            'loss': network[NodeKeys.LOSS],
        }
        super().__init__(name=name, tensors=summary_tensors, nb_runs=dict(), **kw)


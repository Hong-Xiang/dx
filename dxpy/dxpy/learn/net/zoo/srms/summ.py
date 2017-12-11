from dxpy.configs import configurable
from dxpy.learn.config import config
from dxpy.learn.train.summary import SummaryWriter


class SRSummaryWriter(SummaryWriter):
    @configurable(config, with_name=True)
    def __init__(self, network, name='summary'):
        super().__init__(name=name)
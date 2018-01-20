import tensorflow as tf
from ..model import Model
from ..graph import Graph, NodeKeys

from dxpy.configs import configurable
from dxpy.learn.config import config


class Net(Model):
    """ Base class of nets.
    Net add some special tasks based on graph:
        1. train
        2. inference
        3. evaluate
        4. save/load

    Net will add these supports based on result of _kernel() calls.
    - NodeKeys.LOSS: scalar or List[scalar]
        If NodeKeys.Loss presented in self.nodes (automatically registed by model),
        a trainer will be added with name self.name / 'trainer'. Depending on type
        of loss, trainer will switch between single GPU and multi GPU version.
    - NodeKeys.INFERENCE: output of net, will run with self.inference(feeds)
        NOTE: feeds supports both registered name in self.nodes (str) and tf.Tensor
    - NodeKeys.EVALUATE: used for evaluate performace, will run in self.evaluate(feeds)
        NOTE: if no NodeKeys.EVALUATE in self.nodes, self.nodes[NodeKeys.LOSS] will be used. 
    """

    @configurable(config, with_name=True)
    def __init__(self, name, inputs=None, add_trainer=True, add_saver=True, nb_evaluate_runs=32, **kw):
        super().__init__(name, inputs, nb_evaluate_runs=nb_evaluate_runs,
                         add_trainer=add_trainer, add_saver=add_saver, **kw)

    @classmethod
    def _default_config(cls):
        from dxpy.collections.dicts import combine_dicts
        return combine_dicts({
            'add_trainer': True,
            'add_saver': True
        }, super()._default_config())

    def _tensors_need_summary(self):
        if NodeKeys.EVALUATE in self.nodes:
            if isinstance(self.nodes[NodeKeys.EVALUATE], tf.Tensor):
                return {NodeKeys.EVALUATE: self.nodes[NodeKeys.EVALUATE]}
            elif isinstance(self.nodes[NodeKeys.EVALUATE], dict):
                return self.nodes[NodeKeys.EVALUATE]
        return dict()

    def _post_kernel_post_outputs(self):
        super()._post_kernel_post_outputs()
        from ..train import Trainer, Saver
        if self.param('add_trainer'):
            if NodeKeys.LOSS in self.nodes and not NodeKeys.TRAINER in self.nodes:
                self.register_node(NodeKeys.TRAINER,
                                   Trainer(self.name / 'trainer', self.nodes[NodeKeys.LOSS]))
        if self.param('add_saver'):
            self.register_node(NodeKeys.SAVER, Saver(self.name / 'saver'))

    def post_session_created(self):
        pass

    def summary_items(self):
        return dict()

    @property
    def session(self):
        from dxpy.learn.session import get_default_session
        return get_default_session()

    def train(self, feeds=None):
        self.nodes[NodeKeys.TRAINER].run('set_learning_rate')
        return self.nodes[NodeKeys.TRAINER](feeds)

    def inference(self, feeds=None):
        return self.session.run(self.tensor(NodeKeys.INFERENCE), self.get_feed_dict(feeds))

    def evaluate(self, feeds=None):
        return self.session.run(self.tensor(NodeKeys.EVALUATE), self.get_feed_dict(feeds))

    def save(self, feeds=None):
        return self.nodes[NodeKeys.SAVER].run('save', feeds)

    def load(self, feeds=None):
        return self.nodes[NodeKeys.SAVER].run('load', feeds)

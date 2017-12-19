import tensorflow as tf
from ..graph import Graph, NodeKeys
from contextlib import contextmanager
from dxpy.configs import configurable
from dxpy.learn.config import config

_session = None


def set_default_session(session):
    global _session
    _session = session


def get_default_session():
    if _session is None:
        set_default_session(tf.get_default_session())
    return _session


class Session(Graph):
    def __init__(self, name='session', **config):
        super().__init__(name, **config)
        self._create_session()

    @classmethod
    def _default_config(cls):
        from dxpy.collections.dicts import combine_dicts
        return combine_dicts({
            'allow_growth': True,
            'log_device_placement': False
        }, super()._default_config())

    def _create_session(self):
        config = tf.ConfigProto()
        if self.param('allow_growth'):
            config.gpu_options.allow_growth = True
        if self.param('log_device_placement'):
            config.log_device_placement = True
        self.register_main_node(tf.Session(config=config))

    def run(self, tensors, feed_dict=None):
        with self.nodes[NodeKeys.MAIN].as_default():
            return self.nodes[NodeKeys.MAIN].run(tensors, feed_dict)

    def run_func(self, func):
        with self.nodes[NodeKeys.MAIN].as_default():
            return func()

    @property
    def session(self):
        return self.nodes[NodeKeys.MAIN]

    @property
    def graph(self):
        return self.session.graph

    @contextmanager
    def as_default(self):
        with self.nodes[NodeKeys.MAIN].as_default():
            yield self.nodes[NodeKeys.MAIN]

    def post_session_created(self):
        self.as_tensor().run(tf.global_variables_initializer())


class SessionDist(Session):
    def __init__(self, name='session', target=None, **kw):
        self._target = target
        super().__init__(name=name, **kw)

    def _create_session(self):
        config = tf.ConfigProto()
        if self.param('allow_growth'):
            config.gpu_options.allow_growth = True
        if self.param('log_device_placement'):
            config.log_device_placement = True

        self.register_main_node(tf.Session(self._target, config=config))




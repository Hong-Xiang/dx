import tensorflow as tf

from ..graph import Graph


def create_summary_writers(name='train'):
    pass


_instances = dict()


def add_summary(name='train', value=None):
    from ..scalar import global_step
    if value is None:
        raise TypeError("Can not add summary of None.")
    summary_writer(name).add_summary(value, global_step())


def create(name='train'):
    _instances[name] = SummaryWriter('/summary/{}'.format(name))


def summary_writer(name):
    if not name in _instances:
        create(name)
    return _instances[name]


class SummaryWriter(Graph):
    @classmethod
    def _default_config(cls):
        return {'path': './summary'}

    def __init__(self, name, **config):
        super(__class__, self).__init__(name, **config)
        self.register_main_node(tf.summary.FileWriter(self.c['path'], tf.get_default_session().graph))

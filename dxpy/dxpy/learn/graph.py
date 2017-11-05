""" Base class definition """
import tensorflow as tf
from dxpy.filesystem import Path
from dxpy.collections.dicts import DXDict

# On restrict mode, tensors as allocated to CPU memory if not specified.
RESTRICT_MODE = True
KEY_MAIN = 'main'


class Graph:
    """
    Base class of components.
    A `Graph` is an generalization of `tf.Graph`, which is designed for following features:
        1. An unified interface of `tf.Graph` and general compute graph or operations/procedures;
        2. Seperate config and implementation, use TreeDict for configs, and supports multiple ways of config;
        3. An easy-to-use way of seperate/reuse subgraphs
        4. Supports an warp of sessions.run/normal python function.
            Please add member method for tasks, and register them to tasks

    Methods:

    -   as_tensor(self):    
        return self.nodes['main'], which is designed for sub_graphs.

    - get_feed_dict(self, task=None):
        A method which returns a feed_dict, which can be used to update parent graph's get_feed_dict() or run task.
        Which is used to garantee output nodes (if is Tensor) to be valid under certain tasks, if task is None,
        a feed_dict should be provided so that all nodes are valid.
    """

    def __init__(self, name, **config):
        self.name = Path(name)
        self.c = self._load_config(config)
        self.nodes = dict()
        self.tasks = dict()

    # Methods to be overrided:
    @classmethod
    def _default_config(cls):
        """ Override this method to provide default configs. """
        return dict()

    def get_feed_dict(self, feeds, task=None):
        return dict()

    def _print_config_kernel(self, fout, recursive, indent):
        title = "{ind}>{cls}:{name}({fullname})".format(ind=" " * indent,
                                                        cls=__class__,
                                                        name=self.parse_name())
        indent_sub = indent + 4
        for k in self.nodes:
            if isinstance(self.nodes[k], tf.Tensor):
                print('{ind}tf.Tensor:{name}({sp})'.format(ind=" " * indent_sub,
                                                           name=k, sp=self.nodes[k].shape))
            elif isinstance(self.nodes[k], Graph):
                if recursive:
                    self.nodes[k].print_config(recursive, fout, indent_sub)
                else:
                    print('{ind}Graph:{name}({sub_name})'.format(ind=" " * indent_sub,
                                                                 name=k, sub_name=self.nodes[k].name))

    # Functionality functions:

    @property
    def basename(self):
        """
        Get the base name of graph name. Useful for variable_scope or name_scope of graph.
        """
        return self.name.name

    def register_node(self, name=None, tensor_or_subgraph=None):
        if tensor_or_subgraph is None:
            tensor_or_subgraph = name
            name = str(tensor_or_subgraph.name)
        self.nodes[name] = tensor_or_subgraph

    def register_task(self, name, func):
        self.tasks[name] = func

    def register_main_node(self, tensor_or_subgraph=None):
        self.register_node(KEY_MAIN, tensor_or_subgraph)

    def register_main_task(self, func):
        self.register_task(KEY_MAIN, func)

    def create_variable_node(self, dtype, shape, name, *, trainable=False, init_value=None):
        if init_value is not None:
            initer = tf.constant_initializer(init_value)
        else:
            initer = None
        self.register_node(name, tf.get_variable(
            name, shape, dtype, trainable=trainable, initializer=initer))
        return self.nodes[name]

    def create_placeholder_node(self, dtype, shape, name):
        self.register_node(name, tf.placeholder(dtype, shape, name))
        return self.nodes[name]

    def param(self, key, feeds=None):
        """
        Best practice: always use param instead of directly using self.c
        """
        if isinstance(feeds, dict) and key in feeds:
            return feeds[key]
        return self.c[key]

    def print_config(self, fout=None, recursive=False, indent=0):
        self._print_config_kernel(fout, recursive, indent)

    def __getitem__(self, name):
        if name in self.nodes:
            return self.nodes[name]
        elif name in self.tasks:
            return self.tasks[name]
        else:
            return None

    def __call__(self, feeds=None):
        return self.run(KEY_MAIN, feeds)

    def run(self, task_name, feeds):
        return self.tasks[task_name](feeds)

    def as_tensor(self):
        return self.nodes[KEY_MAIN]

    def _load_config(self, config_direct):
        from .config import config as config_global
        current_config = config_global
        for k in self.name.rel_parts():
            current_config = current_config.get(k)
            if current_config is None:
                current_config = dict()
                break
        full_config = self._default_config()
        full_config.update(current_config)
        full_config.update(config_direct)
        return full_config

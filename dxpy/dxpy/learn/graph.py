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
    """

    def __init__(self, name):
        self.name = Path(name)
        self.c = self._load_config()
        self.nodes = dict()
        self.tasks = dict()

    def _load_config(self):
        from .config import config
        from copy import deepcopy
        current_config = config
        for k in self.name.rel_parts():
            current_config = current_config[k]
        return deepcopy(current_config)

    def register_node(self, name=None, tensor_or_subgraph=None):
        if name is None:
            name = tensor_or_subgraph.name
        self.nodes[name] = tensor_or_subgraph

    def register_task(self, name, func):
        self.tasks[name] = func

    def register_main_node(self, tensor_or_subgraph=None):
        self.nodes[KEY_MAIN] = tensor_or_subgraph

    def register_main_task(self, func):
        self.tasks[KEY_MAIN] = func

    def p(self, key, feeds=None):
        if isinstance(feeds, dict) and key in feeds:
            return feeds[key]
        return self.c[key]

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

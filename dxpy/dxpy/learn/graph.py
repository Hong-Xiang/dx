""" Base class definition """
import tensorflow as tf
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
        self.name = name
        self.c = self._load_config()
        self._refine_config()
        self.nodes = dict()
        self.tasks = dict()
        self.key_configs = set()

    def _load_config(self):
        from .config import config
        self.c = config[self.name]

    def _refine_config(self):
        """
        Implement this method if additional configs is required.
        """
        pass

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

    def print_config(self, recursive=False, fout=None):
        import sys
        if fout is None:
            fout = sys.stdout
        print("CONFIG OF {0:>10}:{1:^20}".format(
            __class__, self.name), file=fout)
        for k in self.key_configs:
            print("{0:>10}:{1:<20}".format(k, self.c[k]))

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
        return self.tasks[name](feeds)

    def as_tensor(self):
        return self.nodes[KEY_MAIN]

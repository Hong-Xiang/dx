""" Base class definition """
import tensorflow as tf
from dxpy.collections.dicts import DXDict

# On restrict mode, tensors as allocated to CPU memory if not specified.
RESTRICT_MODE = True


class Graph:
    """
    Base class of components.
    A graph is an abstraction of computational graph.
    It supports:
        1. Load configs externally. (By name(path))
        2. Exports some interface nodes.
        3. Supports some tasks to run.
        4. A main tensor/graph which will be return by method as_tensor()
    """
    def __init__(name):
        from dxpy.collections import TreeDict
        self.name = name
        self.c = self._load_config()
        self.nodes = dict()
        self.tasks = dict()
        self.main = None

    def _load_config(self):
        from ..config import config
        self.c = config[name]

    def _reigister_node(self, tensor_or_subgraph, name=None):
        if name is None:
            name = tensor_or_subgraph.name
        self.nodes[name] = tensor_or_subgraph

    def _register_task(self, name, func):
        self.tasks[name] = func

    def __getitem__(self, name):
        return self.nodes[name]

    def run(self, task_name, feed_dict):
        return self.tasks[name](feed_dict)

    def as_tensor(self):
        return self.main


class Net(Graph):
    """ Base class of nets.
    Net add some special tasks based on graph:
        1. load data
        2. train
        3. inference
        4. evaluate
        5. save/load
    """

    def __init__(self, name):
        super(__class__, self).__init__(name)

    def __getitem__(self, name):
        """
        Inputs:
            name: str, url like string.
        Returns:
            tensor or subnet.
        """
        from dxpy.filesystem.path import Path
        name = Path(name)
        if name.abs in self.nodes:
            return self.nodes[name.abs]
        else:
            names = name.parts
            return self.nodes[names[0]]['/'.join(names[1:])]
        return None

    def run(self, session, task, feeds):
        pass

    def run_undefined(self):
        pass

    def resolve_feeds(self):
        pass

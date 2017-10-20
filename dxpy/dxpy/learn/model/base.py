""" Base class definition """
import tensorflow as tf
from dxpy.collections.dicts import DXDict

# On restrict mode, tensors as allocated to CPU memory if not specified.
RESTRICT_MODE = True


class Net:
    """ Base class of nets.
    Which is used for:
        configs
        # TODO complete doc.
        # TODO deprecate device type, use auto inference by nb_gpus    
    nodes: {node name: tensor or Net}
    subnets: {subnet name: Net}, A reference
    """

    def __init__(self, name, config):
        """
        Inputs:
            devices_type: 'auto' or 'gpus'. If 'gpus', losses and grads are lists, [0] cpu [1-n] gpus.
        """
        self.name = name
        self.nodes = DXDict()
        self.subnets = DXDict()

    def add_node(self, tensor_or_subnet, name=None):
        self.nodes[name] = tensor_or_subnet

    @property
    def as_tensor(self):
        return self.main

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

    def run_unknown_task(self):
        pass

    def resolve_feeds(self):
        pass

from ...graph import Graph


class Net(Graph):
    """ Base class of nets.
    Net add some special tasks based on graph:        
        1. train
        2. inference
        3. evaluate
        4. save/load
    """

    def __init__(self, name):
        super(__class__, self).__init__(name)
        self._construct()

    def _construc(self):
        raise NotImplementedError

    def train(self, feeds=None):
        return self.nodes['train'](feeds)

    def inference(self, feeds=None):
        return self.nodes['inference'][feeds]

    def evaluate(self, feeds=None):
        return self.nodes['evaluate'][feeds]

    def save(self, feeds=None):
        return self.nodes['saver'].run('save', feeds)

    def load(self, feeds=None):
        return self.nodes['saver'].run('load', feeds)

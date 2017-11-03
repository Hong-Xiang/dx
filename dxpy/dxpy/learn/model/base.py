from ..graph import Graph


class Model(Graph):
    def __init__(self, name):
        super(__class__, self).__init__(name)
        self.register_main_task(self.apply)

    def _create_inputs(self):
        inputs = dict()
        for n in self.c['inputs']:
            self.create_node(tf.float32, self.c['inputs'][n]['shape'], n)
            inputs[n] = self.nodes[n]
        self._kernel(inputs)

    def _kernel(self, feeds):
        pass

    def apply(self, feeds=None):
        return _kernel(feeds)

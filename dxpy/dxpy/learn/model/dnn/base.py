from ..graph import Graph


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

    def _run_sub_graph(self, sub_graph_name, feed_dict=None, sub_task_name=None):
        if sub_task_name is None:
            return self[sub_graph_name](feed_dict)
        else:
            return self[sub_graph_name].run(sub_task_name, feed_dict)

    def train(self, feed_dict=None, name=None):
        return self._run_sub_graph('train', feed_dict, name)

    def inference(self, feed_dict=None, name=None):
        return self._run_sub_graph('inference', feed_dict, name)

    def evaluate(self, feed_dict=None, name=None):
        return self._run_sub_graph('evaluate', feed_dict, name)

    def save(self, feed_dict=None):
        return self._run_sub_graph('saver', feed_dict, 'save')

    def load(self, feed_dict=None):
        return self._run_sub_graph('saver', feed_dict, 'load')

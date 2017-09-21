import networkx as nx
from dxpy.exceptions.checks import assert_same_length


class DenpensGraph:
    def __init__(self, nodes, depens):
        """
            n1 depens on n2 if n2 in n1.out_nodes.
        """
        assert_same_length((nodes, depens), ('nodes', 'depens'))
        self.g = nx.DiGraph()
        self.g.add_nodes_from(nodes)
        for i, ds in enumerate(depens):
            if ds is None:
                continue
            if not isinstance(ds, (list, tuple)):
                ds = [ds]
            for d in ds:
                self.g.add_edge(i, d)

    def add_node(self, n):
        self.g.add_node(n)

    def remove_node(self, n):
        self.g.remove_node(n)

    def add_depens(self, node, depens):
        for d in depens:
            self.g.add_edge(node, d)

    def draw(self):
        nx.draw(self.g, with_labels=True)

    def is_free(self, node):
        return self.g.out_degree(node) == 0

    def free_nodes(self):
        return [n for n in self.g if self.is_free(n)]

    def depens(self, n):
        return self.g.successors(n)

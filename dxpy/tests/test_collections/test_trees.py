import unittest
from treelib import Node, Tree
from dxpy.collections import trees


class TestPathTree(unittest.TestCase):
    def test_basic(self):
        pt = trees.PathTree()
        pt.create_node(name='test', data=1)
        self.assertIsInstance(pt.get_node('/'), Node)
        self.assertEqual(pt.get_data('/test'), 1)

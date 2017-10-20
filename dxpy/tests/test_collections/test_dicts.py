import unittest
from dxpy.collections import dicts
class TestDXDict(unittest.TestCase):
    def test_basic(self):
        d = dicts.DXDict({'a': 123})
        self.assertEqual(d['a'], 123)
        d2 = dicts.DXDict({'c': 456}, default_dict=d)
        self.assertEqual(d2['a'], 123)
        self.assertEqual(d2['c'], 456)
        d2['a'] = 789
        self.assertEqual(d2['a'], 789)
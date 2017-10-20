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

    def test_keys(self):
        d = dicts.DXDict({'a': 123})
        d2 = dicts.DXDict({'b': 456}, default_dict=d)
        self.assertEqual(set(d2.keys()), set({'a', 'b'}))


class TestTreeDict(unittest.TestCase):
    def test_basic(self):
        td = dicts.TreeDict()
        td.add_dict('main', '/', {'key1': 'value1'})
        td.add_dict('test', '/main', {'key2': 'value2'})
        td.compile()
        self.assertEqual(td['/main/test']['key1'], 'value1')
        self.assertEqual(td['/main/test']['key2'], 'value2')

    

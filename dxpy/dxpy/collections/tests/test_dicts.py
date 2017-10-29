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

    def test_unified_key(self):
        from dxpy.unittests import AssertEqualSubtestsForFunc
        tests = AssertEqualSubtestsForFunc(self, dicts.TreeDict._unified_keys)
        tests.add('key', ('key',))
        tests.add('/key', ('key',))
        tests.add(list(['key']), ('key',))
        tests.add(tuple(['key']), ('key',))
        tests.add('/key1/key2', ('key1', 'key2'))
        tests.add('key1/key2', ('key1', 'key2'))
        tests.add(['key1', 'key2'], ('key1', 'key2'))
        tests.add(('key1', 'key2'), ('key1', 'key2'))
        tests.add('', tuple())
        tests.add([], tuple())
        tests.add(tuple(), tuple())
        tests.run()

    def test_set_and_load(self):
        td = dicts.TreeDict({'name1': 'value1'})
        td['name2'] = 'value2'
        self.assertEqual(td['name1'], 'value1')
        self.assertEqual(td['name2'], 'value2')

    @unittest.skip
    def test_2_order_set_load(self):
        td_sub = dicts.TreeDict({'sub1': 'value1'})
        td_main = dicts.TreeDict({'main': td_sub})
        self.assertEqual(td_main['main']['sub1'], 'value1')
        td_main['main']['sub2'] = 'value2'
        self.assertEqual(td_main['main']['sub2'], 'value2')

    @unittest.skip
    def test_path_set_load(self):
        td = dicts.TreeDict()
        td['/main/sub1/sub2'] = 'value1'
        self.assertEqual(td['main']['sub1']['sub2'], 'value1')
        self.assertEqual(td['/main/sub1/sub2'], 'value1')

    @unittest.skip
    def test_inherent_value(self):
        td = dicts.TreeDict({'name1': 'value1', 'sub1': dicts.TreeDict()})
        self.assertEqual(td['sub1']['name1'], 'value1')

    @unittest.skip
    def test_key_error(self):
        td = dicts.TreeDict()
        self.assertIsInstance(td['test'], dicts.TreeDict())

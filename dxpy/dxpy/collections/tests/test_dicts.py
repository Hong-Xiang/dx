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

    def test_unified_dicts(self):
        a = {
            'aaa': {
                'key1': 'value1',
                'key2': 'value2'
            },
            'bbb': 'value3'
        }
        td = dicts.TreeDict(a)
        self.assertEqual(td['aaa']['bbb'], 'value3')

    def test_set_and_load(self):
        td = dicts.TreeDict({'name1': 'value1'})
        td['name2'] = 'value2'
        self.assertEqual(td['name1'], 'value1')
        self.assertEqual(td['name2'], 'value2')

    def test_2_order_set_load(self):
        td_sub = dicts.TreeDict({'sub1': 'value1'})
        td_main = dicts.TreeDict({'main': td_sub})
        self.assertEqual(td_main['main']['sub1'], 'value1')
        td_main['main']['sub2'] = 'value2'
        self.assertEqual(td_main['main']['sub2'], 'value2')

    def test_path_set_load(self):
        td = dicts.TreeDict()
        td['/main/sub1/sub2'] = 'value1'
        self.assertEqual(td['main']['sub1']['sub2'], 'value1')
        self.assertEqual(td['/main/sub1/sub2'], 'value1')

    def test_inherent_value(self):
        td = dicts.TreeDict({'name1': 'value1', 'sub1': dicts.TreeDict()})
        self.assertEqual(td['sub1']['name1'], 'value1')

    def test_key_error(self):
        td = dicts.TreeDict()
        self.assertIsInstance(td['test'], dicts.TreeDict)

    def test_publish(self):
        a = {'key1': 'value1', 'key2': {'subk1': 'v1', 'key3': {'key4': 'v4'}}}
        td = dicts.TreeDict(a)
        sub1 = td['key2']
        # self.assertIsInstance(sub1['key1'], dicts.TreeDict)
        td.publish()
        sub2 = td['key2']
        self.assertEqual(sub2['key1'], 'value1')
        sub3 = td['key2']['key3']
        self.assertEqual(sub3['key1'], 'value1')

    def test_publish_2(self):
        a = {'key': 'v1',
             'key2': {'key': 'v2',
                      'key3': {'key': 'v3'}
                      }
             }
        td = dicts.TreeDict(a)
        td.publish()
        self.assertEqual(td['key'], 'v1')
        self.assertEqual(td['key2']['key'], 'v2')
        self.assertEqual(td['key2']['key3']['key'], 'v3')

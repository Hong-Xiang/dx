import unittest
from dxpy.configs import configurable, ConfigsView
from dxpy.configs._configurable import parse_configs

class TestParseConfigs(unittest.TestCase):
    
    def test_basic(self):
        def foo(a, b, *, c, d, e=4):
            pass
        result = parse_configs(foo, 0, _config_object={'b': 1, 'c': 2}, d=3)
        expect = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4}
        self.assertEqual(len(result), len(expect))
        for k in result:
            self.assertEqual(result[k], expect[k])

    def test_no_args(self):
        def foo(a, b, *, c, d, e=4):
            pass
        result = parse_configs(foo, _config_object={
                               'a': 0, 'b': 1, 'c': 2}, d=3)
        expect = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4}
        self.assertEqual(len(result), len(expect))
        for k in result:
            self.assertEqual(result[k], expect[k])


class TestConfigurable(unittest.TestCase):
    def setUp(self):
        self.c = {
            'a': 0,
            'b': 1
        }

    def test_normal_call(self):
        c = dict()

        @configurable(c)
        def foo(a, b, *, c, d, e=4):
            return [a, b, c, d, e]
        self.assertEqual(foo(0, 1, c=2, d=3), list(range(5)))

    def test_provide_config(self):
        c = {'c': 2, }

        @configurable(c)
        def foo(a, b, *, c, d, e=4):
            return [a, b, c, d, e]
        self.assertEqual(foo(0, 1, d=3), list(range(5)))

    def test_override_config(self):
        c = {'c': 3, }

        @configurable(c)
        def foo(a, b, *, c, d, e=4):
            return [a, b, c, d, e]
        self.assertEqual(foo(0, 1, c=2, d=3), list(range(5)))

    def test_provide_config_arg(self):
        c = {'b': 1}

        @configurable(c)
        def foo(a, b, *, c, d, e=4):
            return [a, b, c, d, e]
        self.assertEqual(foo(0, c=2, d=3), list(range(5)))

    def test_config_extra(self):
        c = {'b': 2, 'd': 4, 'x': 100}

        @configurable(c)
        def foo(a, b, *, c, d, e=4):
            return [a, b, c, d, e]
        self.assertEqual(foo(0, 1, c=2, d=3), list(range(5)))

    def test_config_with_name(self):
        c = {'para': {'c': 2}}

        @configurable(c, with_name=True)
        def foo(a, b, *, c, d, e=4, name='para'):
            return [a, b, c, d, e]
        self.assertEqual(foo(0, 1, d=3), list(range(5)))

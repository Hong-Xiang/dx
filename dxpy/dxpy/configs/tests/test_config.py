import unittest
from dxpy.configs import ConfigsView


class TestConfigs(unittest.TestCase):
    def setUp(self):
        self.c = {
            'k1': 'v1',
            'k2': {'k2_1': 'v2_1',
                   'k2_2': 'v2_2'},
            'k3': {'k3_1': {'k3_3_1': 'v_3'}, 'k3_2': 'v3_0'}
        }

    def test_basic_dict(self):
        cv = ConfigsView(self.c)
        self.assertEqual(cv['k1'], 'v1')
        self.assertEqual(cv['k2']['k2_1'], 'v2_1')
        self.assertEqual(cv['k2']['k2_2'], 'v2_2')
        self.assertEqual(cv['k3']['k3_1']['k3_3_1'], 'v_3')

    def test_basepath1(self):
        cv = ConfigsView(self.c, 'k2')
        self.assertEqual(cv['k2_1'], 'v2_1')

    def test_basepath2(self):
        cv = ConfigsView(self.c, 'k3/k3_1')
        self.assertEqual(cv['k3_3_1'], 'v_3')

    def test_inherence(self):
        cv = ConfigsView(self.c, 'k3/k3_1')
        self.assertEqual(cv['k3_2'], 'v3_0')

    def test_name(self):
        cv = ConfigsView(self.c)
        self.assertEqual(cv['k2/k2_1'], 'v2_1')
    
    def test_none(self):
        cv = ConfigsView(self.c)
        self.assertIsNone(cv['aaa'])

    def test_none_inherence(self):
        cv = ConfigsView(self.c)
        self.assertIsNone(cv.get('aaa')['bbb'])

    def test_none_path(self):
        cv = ConfigsView(self.c)
        self.assertIsNone(cv['aaa/bbb'])

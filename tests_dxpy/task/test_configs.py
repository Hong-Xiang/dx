import unittest
from dxpy.task import configs
from dxpy.task.exceptions import UnknownConfigName

# TODO: add unittests


class TestConfigs(unittest.TestCase):
    def setUp(self):
        self.config_name = 'config_unittest'

        class ConfigUnitTest:
            def __init__(self):
                self.field1 = 'field1'

        configs.CONFIGS[self.config_name] = None
        configs.CONFIGS_CLS[self.config_name] = ConfigUnitTest
        pass

    def tearDown(self):
        configs.CONFIGS.pop(self.config_name)
        configs.CONFIGS_CLS.pop(self.config_name)

    def test_get_config(self):
        self.assertEqual(configs.get_config(self.config_name).field1, 'field1')

    def test_unknown_config_name(self):
        name = 'some_invalid_config_name'
        with self.assertRaises(UnknownConfigName):
            configs.get_config(name)

    def test_set_config_by_name_key(self):
        configs.set_config_by_name_key(self.config_name, 'field1', 'test_set')
        self.assertEqual(configs.get_config(
            self.config_name).field1, 'test_set')
        configs.clear_config(self.config_name)

    def test_clear_configs(self):
        configs.set_config_by_name_key(self.config_name, 'field1', 'modified')
        self.assertEqual(configs.get_config(
            self.config_name).field1, 'modified')
        configs.clear_config(self.config_name)
        self.assertEqual(configs.get_config(self.config_name).field1, 'field1')

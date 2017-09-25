import unittest
from dxpy.task import configs
from dxpy.task.exceptions import UnknownConfigName

# TODO: add unittests


class TestConfigs(unittest.TestCase):
    def setUp(self):
        self.config_name = 'config_unittest'

        class ConfigUnitTest:
            pass
        configs.CONFIGS[self.config_name] = None
        configs.CONFIGS_CLS[self.config_name] = ConfigUnitTest
        pass

    def tearDown(self):
        configs.CONFIGS.pop(self.config_name)
        configs.CONFIGS_CLS.pop(self.config_name)

    def test_unknown_config_name(self):
        name = 'some_invalid_config_name'
        with self.assertRaises(UnknownConfigName):
            configs.get_config(name)

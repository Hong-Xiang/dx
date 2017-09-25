import unittest
from dxpy.task import provider
from dxpy.task.configs import DatabaseConfigs, set_config

class TestDatabaseConfig:
    def test_path_config():
        c = DatabaseConfigs(file=':memory:')        
        set_config(config=c)
        provider.init()
        db_service = provider.get_service('database')


        
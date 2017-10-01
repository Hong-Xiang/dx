import unittest
from dxpy.task.database import model
from dxpy.task import configs


class TestModel(unittest.TestCase):
    def setUp(self):
        configs.set_config_by_name_key('database', 'file', ':memory:')
        model.Database.create()

    def tearDown(self):
        model.Database.clear()
        configs.clear_config('database')

    def test_create_engine(self):
        model.Database.get_or_create_engine()

    def test_create_database(self):
        model.Database.create()
        model.Database.create()
        model.Database.clear()

    def test_get_session(self):
        sess = model.Database.session()
        sess.query(model.TaskDB).all()
        sess.close()

    def test_add(self):        
        sess = model.Database.session()
        t = model.TaskDB('test', 'test data')
        sess.add(t)
        sess.commit()
        sess.close()

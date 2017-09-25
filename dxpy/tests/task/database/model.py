import unittest
from dxpy.task.database import model
from dxpy.task import configs


class TestModel(unittest.TestCase):
    def setUp(self):
        configs.set_config_by_name_key('database', 'file', ':memory:')

    def test_create_engine(self):
        eng = model.Database.get_or_create_engine()
        self.assertEqual(str(eng), 'Engine(sqlite:///:memory:)')
        model.Database.clear()

    def test_create_database(self):
        model.Database.create()
        # try create twice
        model.Database.create()
        model.Database.clear()

    def test_get_session(self):
        model.Database.create()
        sess = model.Database.session()
        sess.query(model.TaskDB).all()
        model.Database.clear()

    def test_add(self):
        model.Database.create()
        sess = model.Database.session()
        t = model.TaskDB('test', 'test body')
        sess.add(t)
        sess.commit()

    @unittest.skip
    def test_clear(self):
        model.Database.get_or_create_engine()
        self.assertIsNotNone(model.Database.engine)
        model.Database.clear()
        self.assertIsNone(model.Database.engine)

    def tearDown(self):
        model.Database.create()
        model.Database.drop()
        model.Database.clear()
        configs.clear_config('database')

import unittest
import rx
from dxpy.task import provider
from dxpy.task.database.service import Service as service, TaskDB
from dxpy.task.database.model import create_datebase, drop_database
from dxpy.task.exceptions import TaskNotFoundError


class TestDataBase(unittest.TestCase):
    def setUp(self):
        config_service = provider.get_or_create_service('config')
        c = config_service.get_config('database')
        c.file = ':memory:'
        config_service.set_config('database', config=c)
        create_datebase()
        self.dummpy_json = """
        {
            "id": null,
            "desc": "dummy task",
            "body": "dummy body",
            "dependency": "",
            "time_create": "2017-09-22 12:57:44.036185",
            "state": "BeforeSubmit",
            "is_root": true        
        }
        """
        self.dummpy_id = service.create(self.dummpy_json)
        self.modify_id = service.create(self.dummpy_json)
        self.delete_id = service.create(self.dummpy_json)

    def tearDown(self):
        drop_database()

    def test_create(self):
        tid = service.create(self.dummpy_json)
        self.assertIsInstance(tid, int)

    def test_read(self):
        # TODO: add desired output json
        t = service.read(self.dummpy_id)
        self.assertIsInstance(t, TaskDB)
        self.assertEqual(service.read(self.dummpy_id), self.dummpy_json)

    def test_read_invalid_tid(self):
        invalid_tid = self.dummpy_id + 1000
        t = service.read(invalid_tid)
        self.assertRaises(TaskNotFoundError, invalid_tid)

    def test_read_all(self):
        t_all = service.read_all()
        self.assertIsInstance(t_all, rx.Observable)
        t_list = (t_all
                  .subscribe_on(rx.concurrency.ThreadPoolScheduler())
                  .to_list()
                  .to_blocking().first())
        self.assertIsInstance(t_list, list)

    def test_update(self):
        new_dummpy_json = """
        {
            "id": {tid},
            "desc": "modified",
            "body": "dummy body",
            "dependency": "",
            "time_create": "2017-09-22 12:57:44.036185",
            "state": "BeforeSubmit",
            "is_root": true        
        }
        """.format(tid=self.modify_id)
        service.update(new_dummpy_json)
        self.assertEqual(service.read(self.modify_id).desc, new_dummpy_json)

    def test_delete(self):
        service.read(self.delete_id)
        service.delete(self.delete_id)
        self.assertRaises(TaskNotFoundError, self.delete_id)

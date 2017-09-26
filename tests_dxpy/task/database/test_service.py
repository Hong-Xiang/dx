import unittest
import json
import rx
from dxpy.task import provider
from dxpy.task import configs
from dxpy.task.database.model import Database, TaskDB
from dxpy.task.exceptions import TaskNotFoundError
from dxpy.task.database.service import Service as service


class TestDataBase(unittest.TestCase):
    def setUp(self):
        configs.set_config_by_name_key('database', 'file', ':memory:')
        Database.create()
        self.dummpy_json = r"""{"id": 1, "desc": "sleep task", "body": "!!python/object:dxpy.task.representation.templates.TaskCommand\nactivity: true\ncommand: sleep 10\ndependency: []\ndesc: sleep task\nid: 1\nis_root: true\nstate: !task_state 'BeforeSubmit'\ntime_stampes: !!python/object:dxpy.time.timestamps.Start\n  time_stamps: {start: !!timestamp '2017-09-22 12:57:44.036185'}\nworkdir: !path '/home/hongxwing/Workspace/jpyn'\nworkers: !!python/object:dxpy.task.misc.Workers {info: null, nb_workers: 1, type: !worker_type 'MultiThreading'}\n", "dependency": [], "time_create": "2017-09-22 12:57:44.036185", "state": "BeforeSubmit", "is_root": true}"""
        self.dummpy_id = service.create(self.dummpy_json)
        self.modify_id = service.create(self.dummpy_json)
        self.delete_id = service.create(self.dummpy_json)

    def tearDown(self):
        # Database.drop()
        # Database.clear()
        pass

    def test_create(self):
        tid = service.create(self.dummpy_json)
        self.assertIsInstance(tid, int)

    def test_read(self):
        # TODO: add desired output json
        t = service.read(self.dummpy_id)
        self.assertIsInstance(t, str)
        # self.assertEqual(t, self.dummpy_json)

    def test_read_invalid_tid(self):
        invalid_tid = self.dummpy_id + 1000
        with self.assertRaises(TaskNotFoundError):
            t = service.read(invalid_tid)

    def test_read_all(self):
        t_all = service.read_all()
        self.assertIsInstance(t_all, rx.Observable)
        t_list = (t_all
                  .subscribe_on(rx.concurrency.ThreadPoolScheduler())
                  .to_list()
                  .to_blocking().first())
        self.assertIsInstance(t_list, list)

    def test_update(self):
        new_dummpy_json = json.dumps({
            "id": self.modify_id,
            "desc": "modified",
            "body": "dummy body",
            "dependency": "",
            "time_create": "2017-09-22 12:57:44.036185",
            "state": "BeforeSubmit",
            "is_root": True
        })
        service.update(new_dummpy_json)
        data = json.loads(service.read(self.modify_id))
        self.assertEqual(data['desc'], "modified")

    def test_delete(self):
        service.read(self.delete_id)
        service.delete(self.delete_id)
        with self.assertRaises(TaskNotFoundError):
            service.read(self.delete_id)

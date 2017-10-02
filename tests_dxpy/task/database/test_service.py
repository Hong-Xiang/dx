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
        self.dummy_dct = {
            '__task__': True,
            'id': 1,
            'desc': 'dummpy task',
            'data': '',
            'time_stamp': {
                'create': "2017-09-22 12:57:44.036185",
                'start': None,
                'end': None,
            },
            'is_root': True,
            'state': 'BeforeSubmit',
            'workdir': '/tmp/test',
            'worker': 'Slurm',
            'dependency': [],
            'type': 'Regular'
        }
        self.dummy_json = json.dumps(self.dummy_dct)
        self.dummy_id = service.create(self.dummy_json)
        self.modify_id = service.create(self.dummy_json)
        self.delete_id = service.create(self.dummy_json)

    def tearDown(self):
        service.clear_session()
        Database.clear()

    def test_create(self):
        tid = service.create(self.dummy_json)
        self.assertIsInstance(tid, int)

    def test_creat_json(self):
        dct = {"__task__": True,
               "id": 1,
               "desc": "test",
               "workdir": "/home/hongxwing/Workspace/dxl/tests_dxpy/task",
               "worker": "NoAction",
               "type": "Regular",
               "state": "BeforeSubmit",
               "dependency": [],
               "time_stamp": {"create": "2017-10-02 05:15:56.349184", "start": None, "end": None},
               "is_root": False,
               "data": {}}
        s = json.dumps(dct)

        tid = service.create(s)

    def test_read(self):
        # TODO: add desired output json
        t = service.read(self.dummy_id)
        self.assertIsInstance(t, str)
        dct = json.loads(t)
        self.assertTrue(dct['__task__'])

    def test_read_invalid_tid(self):
        invalid_tid = self.dummy_id + 1000
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
        new_dct = json.loads(service.read(self.modify_id))
        new_dct['desc'] = 'modified'
        service.update(json.dumps(new_dct))
        data = json.loads(service.read(self.modify_id))
        self.assertEqual(data['desc'], "modified")

    def test_delete(self):
        service.read(self.delete_id)
        service.delete(self.delete_id)
        with self.assertRaises(TaskNotFoundError):
            service.read(self.delete_id)

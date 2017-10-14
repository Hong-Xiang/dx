import unittest
import rx
from unittest.mock import Mock
import json
from dxpy.task import configs
from dxpy.task.representation import task, creators
from dxpy.task.database.model import Database
from dxpy.task.exceptions import TaskNotFoundError
import dxpy.task.interface as interface


class TestInterface(unittest.TestCase):
    def setUp(self):
        configs.set_config_by_name_key('database', 'file', ':memory:')
        Database.create()

    def tearDown(self):
        Database.clear()

    def test_parset_json(self):
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
        self.assertEqual(interface.parse_json(s).id, 1)
        self.assertIsInstance(interface.parse_json(s), task.Task)

    def test_create(self):
        tid = interface.create(task.Task())
        self.assertIsInstance(tid, int)

    def test_read(self):
        tid = interface.create(task.Task(desc='test_read'))
        tr = interface.read(tid)
        self.assertEqual(tr.desc, 'test_read')

    def test_read_all_empty(self):
        ts = (interface.read_all().to_list()
              .subscribe_on(rx.concurrency.ThreadPoolScheduler())
              .to_blocking().first())
        self.assertEqual(len(ts), 0)

    def test_read_all(self):
        t1 = interface.create(task.Task(desc='test_read_all_1'))
        t2 = interface.create(task.Task(desc='test_read_all_2'))
        ts = (interface.read_all()
              .subscribe_on(rx.concurrency.ThreadPoolScheduler())
              .to_list()
              .to_blocking().first())
        self.assertEqual(t1, 1)
        self.assertEqual(t2, 2)
        self.assertEqual(ts[0].desc, 'test_read_all_1')
        self.assertEqual(ts[1].desc, 'test_read_all_2')

    def test_update(self):
        desc0 = 'test_update'
        desc1 = 'test_update_modified'
        tid = interface.create(task.Task(desc=desc0))
        tr = interface.read(tid)
        self.assertEqual(tr.desc, desc0)
        tr.desc = desc1
        interface.update(tr)
        tr2 = interface.read(tid)
        self.assertEqual(tr2.desc, desc1)

    def test_init_state(self):
        tid = interface.create(task.Task())
        self.assertEqual(interface.read(tid).state,
                         task.State.BeforeSubmit)

    def test_submit(self):
        tid = interface.create(task.Task())
        interface.mark_submit(interface.read(tid))
        self.assertEqual(interface.read(tid).state, task.State.Pending)

    def test_start(self):
        tid = interface.create(task.Task())
        interface.mark_start(interface.read(tid))
        self.assertEqual(interface.read(tid).state, task.State.Runing)

    def test_complete(self):
        tid = interface.create(task.Task())
        interface.mark_complete(interface.read(tid))
        self.assertEqual(interface.read(tid).state, task.State.Complete)

    def test_delete(self):
        tid = interface.create(task.Task())
        interface.read(tid)
        interface.delete(tid)
        with self.assertRaises(TaskNotFoundError):
            interface.read(tid)

    def test_add_graph(self):
        tasks = [task.Task() for _ in range(3)]
        g = creators.task_graph(tasks, depens=[None, 0, 1])
        tids = interface.create_graph(g)
        self.assertEqual(len(tids), 3)
        tasks = [interface.read(i) for i in tids]
        tasks_root = [t for t in tasks if t.is_root]
        self.assertEqual(len(tasks_root), 1)
        task2 = tasks_root[0]
        task1 = interface.read(task2.dependency[0])
        task0 = interface.read(task1.dependency[0])
        self.assertEqual({task0.id, task1.id, task2.id}, {1, 2, 3})

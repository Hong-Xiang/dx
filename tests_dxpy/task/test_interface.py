import unittest
import rx
from unittest.mock import Mock
from dxpy.task import configs
from dxpy.task.representation import factory
from dxpy.task.database.model import Database
from dxpy.task import misc
from dxpy.task.exceptions import TaskNotFoundError
import dxpy.task.interface as interface


class TestInterface(unittest.TestCase):
    def setUp(self):
        configs.set_config_by_name_key('database', 'file', ':memory:')
        Database.create()

    def tearDown(self):
        Database.drop()

    def test_parset_json(self):
        from dxpy.task.representation import TaskPy
        s = '{"id": 1, "desc": "sleep task", "body": "!!python/object:dxpy.task.representation.templates.TaskCommand\\nactivity: true\\ncommand: sleep 10\\ndependency: []\\ndesc: sleep task\\nid: 1\\nis_root: true\\nstate: !task_state \'BeforeSubmit\'\\ntime_stampes: !!python/object:dxpy.time.timestamps.Start\\n  time_stamps: {start: !!timestamp \'2017-09-22 12:57:44.036185\'}\\nworkdir: !path \'/home/hongxwing/Workspace/jpyn\'\\nworkers: !!python/object:dxpy.task.misc.Workers {info: null, nb_workers: 1, type: !worker_type \'MultiThreading\'}\\n", "dependency": [], "time_create": "2017-09-22 12:57:44.036185", "state": "BeforeSubmit", "is_root": true}'
        self.assertEqual(interface.parse_json(s).id, 1)
        self.assertIsInstance(interface.parse_json(s), TaskPy)

    def test_create(self):
        tid = interface.create(factory.create('Task'))
        self.assertIsInstance(tid, int)

    def test_read(self):
        tid = interface.create(factory.create('Task', desc='test_read'))
        tr = interface.read(tid)
        self.assertEqual(tr.desc, 'test_read')

    def test_read_all_empty(self):
        ts = (interface.read_all().to_list()
              .subscribe_on(rx.concurrency.ThreadPoolScheduler())
              .to_blocking().first())
        self.assertEqual(len(ts), 0)

    def test_read_all(self):
        t1 = interface.create(factory.create('Task', desc='test_read_all_1'))
        t2 = interface.create(factory.create('Task', desc='test_read_all_2'))
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
        tid = interface.create(factory.create('Task', desc=desc0))
        tr = interface.read(tid)
        self.assertEqual(tr.desc, desc0)
        tr.desc = desc1
        interface.update(tr)
        tr2 = interface.read(tid)
        self.assertEqual(tr2.desc, desc1)

    def test_init_state(self):
        tid = interface.create(factory.create('Task'))
        self.assertEqual(interface.read(tid).state,
                         misc.TaskState.BeforeSubmit)

    def test_submit(self):
        tid = interface.create(factory.create('Task'))
        interface.mark_submit(interface.read(tid))
        self.assertEqual(interface.read(tid).state, misc.TaskState.Pending)

    def test_start(self):
        tid = interface.create(factory.create('Task'))
        interface.mark_start(interface.read(tid))
        self.assertEqual(interface.read(tid).state, misc.TaskState.Runing)

    def test_complete(self):
        tid = interface.create(factory.create('Task'))
        interface.mark_complete(interface.read(tid))
        self.assertEqual(interface.read(tid).state, misc.TaskState.Complete)

    def test_delete(self):
        tid = interface.create(factory.create('Task'))
        interface.read(tid)
        interface.delete(tid)
        with self.assertRaises(TaskNotFoundError):
            interface.read(tid)

    def test_add_graph(self):
        tasks = [factory.create('Task') for _ in range(3)]
        g = factory.create_task_graph(tasks, depens=[None, 0, 1])
        tids = interface.create_graph(g)
        self.assertEqual(len(tids), 3)
        tasks = [interface.read(i) for i in tids]
        tasks_root = [t for t in tasks if t.is_root]
        self.assertEqual(len(tasks_root), 1)
        task2 = tasks_root[0]
        task1 = interface.read(task2.dependency[0])
        task0 = interface.read(task1.dependency[0])
        self.assertEqual({task0.id, task1.id, task2.id}, {1, 2, 3})

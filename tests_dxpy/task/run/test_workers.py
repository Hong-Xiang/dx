import unittest
import threading
from fs.tempfs import TempFS
from dxpy.task import configs, interface, misc
from dxpy.task.representation import factory
from dxpy.task.run import workers
from dxpy.task.database.model import Database
from dxpy.task.database.web.resource import lauch_database_server
from time import sleep

def quick_create(tid_buffer, workers_type=None, state=None):
    if workers_type is None:
        workers_type = misc.WorkerType.NoAction
    if state is None:
        state = misc.TaskState.Pending
    task_prot = factory.create('Task',
                               state=state,
                               workers=misc.Workers(workers_type))
    tid = interface.create(task_prot)
    task = interface.read(tid)
    tid_buffer.append(tid)
    return task


class TestWorkers(unittest.TestCase):
    def setUp(self):
        self.tid_buffer = []
        # self.tempfs = TempFS()
        # p = self.tempfs.getsyspath('testdb.db')
        # configs.set_config_by_name_key('database', 'file', p)
        configs.set_config_by_name_key('database', 'use_web_api', True)
        # configs.set_config_by_name_key('database', 'port', 23342)
        # Database.create()
        # t = threading.Thread(target=lauch_database_server)

    def tearDown(self):
        for tid in self.tid_buffer:
            interface.delete(tid)
        # Database.drop()
        # self.tempfs.clean()
        pass

    def test_is_complete(self):
        self.assertTrue(workers.Workers.is_complete(
            quick_create(self.tid_buffer, state=misc.TaskState.Complete)))
        self.assertFalse(workers.Workers.is_complete(
            quick_create(self.tid_buffer, state=misc.TaskState.Pending)))
        self.assertFalse(workers.Workers.is_complete(
            quick_create(self.tid_buffer, state=misc.TaskState.Runing)))

    def test_on_this_worker(self):
        task = quick_create(self.tid_buffer, misc.WorkerType.NoAction)
        self.assertTrue(workers.NoAction.on_this_worker(task))
        self.assertFalse(workers.Slurm.on_this_worker(task))

    def test_no_action_complete(self):
        task = quick_create(self.tid_buffer, misc.WorkerType.NoAction,
                            misc.TaskState.Pending)
        interface.read(task.id)
        self.assertEqual(task.state, misc.TaskState.Pending)
        workers.NoAction.run(task)
        sleep(0.1)
        self.assertEqual(interface.read(task.id).state,
                         misc.TaskState.Complete)

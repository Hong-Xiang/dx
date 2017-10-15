import unittest
import threading
from fs.tempfs import TempFS
from dxpy.task import configs, interface
from dxpy.task.representation import task, creators
from dxpy.task.run import workers
from dxpy.task.database.model import Database
from time import sleep


def quick_create(tid_buffer, worker=None, state=None):
    if worker is None:
        worker = task.Worker.NoAction
    if state is None:
        state = task.State.Pending
    task_prot = task.Task(desc='test',
                          state=state,
                          worker=worker)
    tid = interface.create(task_prot)
    t = interface.read(tid)
    tid_buffer.append(tid)
    return t


class TestWorkers(unittest.TestCase):
    def setUp(self):
        self.tid_buffer = []
        configs.set_config_by_name_key('database', 'use_web_api', True)

    def tearDown(self):
        for tid in self.tid_buffer:
            interface.delete(tid)

    def test_is_complete(self):
        self.assertTrue(workers.Workers.is_complete(
            quick_create(self.tid_buffer, state=task.State.Complete)))
        self.assertFalse(workers.Workers.is_complete(
            quick_create(self.tid_buffer, state=task.State.Pending)))
        self.assertFalse(workers.Workers.is_complete(
            quick_create(self.tid_buffer, state=task.State.Runing)))

    def test_on_this_worker(self):
        t = quick_create(self.tid_buffer, task.Worker.NoAction)
        self.assertTrue(workers.NoAction.on_this_worker(t))
        self.assertFalse(workers.Slurm.on_this_worker(t))

    def test_no_action_complete(self):
        t = quick_create(self.tid_buffer, task.Worker.NoAction,
                            task.State.Pending)
        interface.read(t.id)
        self.assertEqual(t.state, task.State.Pending)
        workers.NoAction.run(t)
        sleep(0.1)
        self.assertEqual(interface.read(t.id).state,
                         task.State.Complete)

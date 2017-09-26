import unittest
from dxpy.task import configs, interface, misc
from dxpy.task.representation import factory
from dxpy.task.run import workers
from dxpy.task.database.model import Database


def quick_create(workers_type=None, state=None):
    if workers_type is None:
        workers_type = misc.WorkerType.NoAction
    if state is None:
        state = misc.TaskState.Pending
    task_prot = factory.create('Task',
                               state=state,
                               workers=misc.Workers(workers_type))
    tid = interface.create(task_prot)
    task = interface.read(tid)
    return task


class TestWorkers(unittest.TestCase):
    def setUp(self):
        configs.set_config_by_name_key('database', 'file', ':memory:')
        Database.create()

    def tearDown(self):
        Database.drop()

    def test_is_complete(self):
        self.assertTrue(workers.Workers.is_complete(
            quick_create(state=misc.TaskState.Complete)))
        self.assertFalse(workers.Workers.is_complete(
            quick_create(state=misc.TaskState.Pending)))
        self.assertFalse(workers.Workers.is_complete(
            quick_create(state=misc.TaskState.Runing)))

    def test_on_this_worker(self):
        task_prot = factory.create(
            'Task', workers=misc.Workers(misc.WorkerType.NoAction))
        tid = interface.create(task_prot)
        task = interface.read(tid)
        self.assertTrue(workers.NoAction.on_this_worker(task))
        self.assertFalse(workers.Slurm.on_this_worker(task))

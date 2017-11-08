import unittest
import rx
from dxpy.task.exceptions import TaskNotFoundError
from unittest.mock import Mock, call
from dxpy.task import configs, interface
from dxpy.task import database as db
from dxpy.task.model import task, creators
from dxpy.task.run import service, workers

import sys


def quick_create(tid_buffer, state, wks=None):
    if wks is None:
        wks = task.Worker.NoAction
    tid = interface.create(task.Task(state=state, worker=wks))
    tid_buffer.append(tid)
    return tid


def quick_create_chain(tid_buffer, states):
    tids = [quick_create(tid_buffer, s) for s in states]
    for i in range(len(tids)):
        t = interface.read(tids[i])
        t.is_root = False
        if i == len(tids) - 1:
            t.is_root = True
        if i > 0:
            t.dependency = [tids[i - 1]]
        interface.update(t)
    return tids


def get_task(id_dict, key, index=None):
    tid = id_dict[key]
    if index is not None:
        tid = tid[index]
    return interface.read(tid)


class TestService(unittest.TestCase):
    def setUp(self):
        from dxpy.task.database import Database
        Database.clear()
        self.tidcs = []
        configs.set_config_by_name_key('database', 'use_web_api', True)
        # Database.create()
        # Database.drop()
        self.tids = {
            'before_submit': quick_create(self.tidcs, task.State.BeforeSubmit),
            'pending': quick_create(self.tidcs, task.State.Pending),
            'running': quick_create(self.tidcs, task.State.Runing),
            'complete': quick_create(self.tidcs, task.State.Complete),
            'chain_1': quick_create_chain(self.tidcs, [task.State.BeforeSubmit, task.State.Pending]),
            'chain_2': quick_create_chain(self.tidcs, [task.State.Complete, task.State.Pending]),
            'chain_3': quick_create_chain(self.tidcs, [task.State.Runing, task.State.Pending]),
            'slurm': quick_create(self.tidcs, task.State.Runing, task.Worker.Slurm)
        }

    def tearDown(self):

        for tid in self.tidcs:
            interface.delete(tid)
        # configs.clear_config()
        # Database.drop()

        # def test_auto_complete(self):
        #     serv.read_complete_tasks_on_worker = Mock(
        #         return_value=rx.Observable.from_(list(range(3))))
        #     serv.update_complete = Mock()
        #     calls = [call(0), call(1), call(2)]
        #     serv.update_complete.assert_has_calls(calls)

    def test_auto_submit_root(self):
        self.assertEqual(get_task(self.tids, 'before_submit').state,
                         task.State.BeforeSubmit)
        service.auto_submit_root()
        self.assertEqual(get_task(self.tids, 'before_submit').state,
                         task.State.Pending)

    def test_auto_submit_chain(self):
        self.assertEqual(get_task(self.tids, 'chain_1', 0).state,
                         task.State.BeforeSubmit)
        service.auto_submit_chain()
        self.assertEqual(get_task(self.tids, 'chain_1', 0).state,
                         task.State.Pending)

    def test_auto_complete(self):
        self.assertEqual(get_task(self.tids, 'slurm').state, task.State.Runing)
        workers.Slurm.is_complete = Mock(return_value=True)
        service.auto_complete()
        self.assertEqual(get_task(self.tids, 'slurm').state,
                         task.State.Complete)

    def test_auto_start(self):
        self.assertEqual(get_task(self.tids, 'pending').state,
                         task.State.Pending)
        service.auto_start()
        self.assertTrue(get_task(self.tids, 'pending').state in [
                        task.State.Runing, task.State.Complete])

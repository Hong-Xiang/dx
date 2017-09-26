import unittest
import rx
from dxpy.task.exceptions import TaskNotFoundError
from unittest.mock import Mock, call
from dxpy.task import configs
from dxpy.task.representation import factory
from dxpy.task import interface
from dxpy.task.misc import Workers, WorkerType
from dxpy.task.misc import TaskState as S
from dxpy.task.run import service
from dxpy.task.database.model import Database


def quick_create(state):
    return interface.create(factory.create('Task', state=state,
                                           workers=Workers(worker_type=WorkerType.NoAction)))


def quick_create_chain(states):
    tids = [quick_create(s) for s in states]
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
        configs.set_config_by_name_key('database', 'file', ':memory:')
        Database.create()
        self.tids = {
            'before_submit': quick_create(S.BeforeSubmit),
            'pending': quick_create(S.Pending),
            'running': quick_create(S.Runing),
            'complete': quick_create(S.Complete),
            'chain_1': quick_create_chain([S.BeforeSubmit, S.Pending]),
            'chain_2': quick_create_chain([S.Complete, S.Pending]),
            'chain_3': quick_create_chain([S.Runing, S.Pending]),
        }

    def tearDown(self):
        Database.drop()

    # def test_auto_complete(self):
    #     serv.read_complete_tasks_on_worker = Mock(
    #         return_value=rx.Observable.from_(list(range(3))))
    #     serv.update_complete = Mock()
    #     calls = [call(0), call(1), call(2)]
    #     serv.update_complete.assert_has_calls(calls)

    def test_auto_submit_root(self):
        self.assertEqual(get_task(self.tids, 'before_submit').state,
                         S.BeforeSubmit)
        service.auto_submit_root()
        self.assertEqual(get_task(self.tids, 'before_submit').state,
                         S.Pending)

    def test_auto_submit_chain(self):
        self.assertEqual(get_task(self.tids, 'chain_1', 0).state,
                         S.BeforeSubmit)
        service.auto_submit_chain()
        self.assertEqual(get_task(self.tids, 'chain_1', 0).state,
                         S.Pending)

import unittest
import rx
from dxpy.task.exceptions import TaskNotFoundError
from unittest.mock import Mock, call
from dxpy.task import configs
from dxpy.task.representation import factory
from dxpy.task import interface
from dxpy.task.misc import Workers, WorkerType, TaskState
from dxpy.task.run import service


class TestService(unittest.TestCase):
    def setUp(self):
        configs.set_config_by_name_key('database', 'file', ':memory:')
        Database.create()
        self.tids = {
            'before_submit': interface.create(factory.create('Task', state=TaskState.BeforeSubmit))
        }

    def tearDown(self):
        Database.drop()

    def test_auto_complete(self):
        serv.read_complete_tasks_on_worker = Mock(
            return_value=rx.Observable.from_(list(range(3))))
        serv.update_complete = Mock()
        calls = [call(0), call(1), call(2)]
        serv.update_complete.assert_has_calls(calls)

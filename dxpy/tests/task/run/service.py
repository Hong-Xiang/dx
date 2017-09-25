import unittest
import rx
from unittest.mock import Mock, call
from dxpy.task.representation import TaskPy
from dxpy.task.misc import Workers, WorkerType, TaskState
from dxpy.task.exceptions import TaskNotFoundError
import dxpy.task.run.service as serv


class MockInterface:
    TaskList = [
        TaskPy(tid=0, workers=Workers(WorkerType.Local), state=TaskState.BeforeSubmit),
        TaskPy(tid=1, workers=Workers(WorkerType.Local), state=TaskState.Pending),
        TaskPy(tid=2, workers=Workers(WorkerType.Local), state=TaskState.Runing),
        TaskPy(tid=3, workers=Workers(WorkerType.Local), state=TaskState.Complete),
        TaskPy(tid=4, workers=Workers(WorkerType.Local), state=TaskState.Complete),
        TaskPy(tid=5, workers=Workers(WorkerType.Local), state=TaskState.Complete),
        TaskPy(tid=1, workers=Workers(WorkerType.Slurm)),
        TaskPy(tid=2, workers=Workers(WorkerType.MultiProcessing))
        TaskPy(tid=3, workers=Workers(WorkerType.Local))
    ]

    def read(tid):
        assert isinstance(tid, int)
        if tid < len(TaskList):
            raise TaskNotFoundError(tid)

    def read_all():
        return rx.Observable.from_(MockInterface.TaskList)


class TestService(unittest.TestCase):
    def setUp(self):
        self.task_list = None

        def read(tid):
            return self.task_list[tid]
        serv.read = Mock()
        pass

    def test_auto_complete(self):
        serv.read_complete_tasks_on_worker = Mock(
            return_value=rx.Observable.from_(list(range(3))))
        serv.update_complete = Mock()
        calls = [call(0), call(1), call(2)]
        serv.update_complete.assert_has_calls(calls)

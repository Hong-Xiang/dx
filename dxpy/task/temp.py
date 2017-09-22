from dxpy.task.core.taskpy import TaskPy
from dxpy.file_system.path import Path
from dxpy.task.misc import Workers, WorkerType, TaskState
from dxpy.time.timestamps import Progress, Run
from dxpy.time.utils import now


def a_task():
    return TaskPy(tid=None,
                  desc='test task',
                  workdir=Path('.'),
                  workers=Workers(WorkerType.Local, 1),
                  activity=True,
                  state=TaskState.BeforeSubmit,
                  time_stamps=Run(start=now()),
                  dependency=[],
                  is_root=True)

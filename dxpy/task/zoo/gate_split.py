from dxpy.file_system.path import Path
from ..representation.factory import create_task_graph
from ..representation.templates import TaskCommand
from ..interface import create_graph


class GateSplit:
    def __init__(self, workdir=None):
        self.workdir = Path(workdir)        

    def create(self):
        cmd = 'sleep {0} && hostname'
        t1 = TaskCommand(cmd.format(self.duration, 1), workdir=self.workdir)
        t2 = TaskCommand(cmd.format(self.duration, 2), workdir=self.workdir)
        t3 = TaskCommand(cmd.format(self.duration, 3), workdir=self.workdir)
        g = create_task_graph([t1, t2, t3], [None, 0, 1])
        return g


class SbatchCreator:
    def __init__(self, workdir=None, ):
        pass

from dxpy.file_system.path import Path
from ..representation.factory import create_task_graph
from ..representation.task import Worker
from ..representation.templates import TaskCommand, TaskScript
from ..interface import create_graph


class GateSplit:
    def __init__(self, rootdir=None, workdirs=None, files=None, merge_command=None):
        self.rootdir = rootdir
        self.workdirs = [Path(w) for w in workdirs]
        self.files = files
        self.merge_command = merge_command

    def create(self):
        cmd = 'cd {0} && sbatch {1}'
        sbatch_tasks = []
        for w, f in zip(self.workdirs, self.files):
            sbatch_tasks.append(TaskScript(
                workdir=w, file=f, worker=Worker.Slurm))
        dependencies = [None]*len(sbatch_tasks)
        merge_task = TaskCommand(self.merge_command, workdir=)
        g = create_task_graph([t1, t2, t3], [None, 0, 1])
        return g


class SbatchCreator:
    def __init__(self, workdir=None, ):
        pass

from dxpy.file_system.path import Path
from ..representation.factory import create_task_graph
from ..representation.task import Worker
from ..representation.templates import TaskCommand, TaskScript
from ..interface import create_graph


class GateSplit:
    def __init__(self, target=None, post_sh=None, subdirs=None, run_sh=None):
        self.target = Path(target)
        self.subdirs = [Path(d) for d in subdirs]
        self.run_sh = run_sh
        self.post_sh = post_sh

    def create(self):
        cmd = 'cd {0} && sbatch {1}'
        tasks = []
        for w in self.subdirs:
            tasks.append(TaskScript(workdir=w,
                                    file=self.run_sh,
                                    worker=Worker.Slurm))
        dependencies = [None] * len(sbatch_tasks)
        merge_task = TaskScript(workdir=self.target,
                                file=self.post_sh,
                                worker=Worker.Slurm)
        tasks.append(merge_task)
        dependencies.append(list(range(len(dependencies))))
        g = create_task_graph(tasks, dependencies)
        return g


class SbatchCreator:
    def __init__(self, workdir=None, ):
        pass

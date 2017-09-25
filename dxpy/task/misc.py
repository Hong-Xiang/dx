from enum import Enum
import yaml
from dxpy.utils import add_yaml_support


class TaskState(Enum):
    BeforeSubmit = 0
    Pending = 1
    Runing = 2
    Complete = 3


add_yaml_support(TaskState, '!task_state')


class WorkerType(Enum):
    Local = 0,
    MultiThreading = 1,
    # MultiProcessing = 2,
    # Dask = 3,
    Slurm = 4


add_yaml_support(WorkerType, '!worker_type')


class Workers:
    def __init__(self, worker_type=None, nb_workers=1, info=None):
        if worker_type is None:
            worker_type = WorkerType.MultiThreading
        self.type = worker_type
        self.num_workers = nb_workers
        self.info = info

    def __eq__(self, wkr):
        return (self.type == wkr.type
                and self.num_workers == wkr.num_workers
                and self.info == wkr.info)

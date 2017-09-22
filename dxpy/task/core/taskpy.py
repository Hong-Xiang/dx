""" 
A **Representation** of task
Since it is only a representation, it is not mutable, it has only properties.
No action is allowed.
"""
import json
import yaml
import copy
from dxpy.file_system.path import Path
from dxpy.time.timestamps import Start
from dxpy.time.utils import strf
from dxpy.task.misc import TaskState


class TaskPy:
    def __init__(self, tid=None, desc='', workdir='.', workers=None, activity=True, state=None, time_stamps=None, dependency=None, is_root=True):
        self.id = tid
        self.desc = desc
        self.workdir = Path(Path(workdir).abs)
        if workers is None:
            workers = Workers()
        self.workers = workers
        self.desc = desc
        if time_stamps is None:
            time_stamps = Start()
        self.time_stampes = time_stamps
        if dependency is None:
            dependency = tuple()
        self.dependency = dependency
        if state is None:
            state = TaskState.BeforeSubmit
        self.state = state
        self.activity = activity
        self.is_root = is_root

    @property
    def is_pending(self):
        return self.state == TaskState.Pending

    @property
    def is_before_submit(self):
        return self.state == TaskState.BeforeSubmit

    @property
    def is_complete(self):
        return self.state == TaskState.Complete

    def run(self):
        raise NotImplementedError

    @classmethod
    def from_yml(cls, s):
        return yaml.load(s)

    @classmethod
    def from_json(cls, s):
        # TODO: add check here
        return cls.from_yml(json.loads(s)['body'])

    def to_json(self):
        return json.dumps({
            'id': self.id,
            'desc': self.desc,
            'body': self.to_yml(),
            'dependency': ' '.join(str(self.dependency)),
            'time_create': strf(self.time_stampes.start),
            'state': self.state.name,
            'is_root': self.is_root
        })

    def to_yml(self):
        return yaml.dump(self)


def py2json(task):
    return json.dumps({
        'id': task.id,
        'desc': task.desc,
        'body': yaml.dump(task),
        'dependency': ' '.join(str(task.dependency)),
        'time_create': strf(task.time_stampes.start),
        'state': task.state.name,
        'is_root': task.is_root
    })


def json2yml(task):
    return json.loads(task)['body']


def json2py(task):
    return yml2py(json2yml(task))


def yml2py(task):
    return yaml.load(task)


def submit(task):
    task = copy.deepcopy(task)
    task.state = TaskState.Pending
    return task


def start(task):
    task = copy.deepcopy(task)
    task.state = TaskState.Runing
    return task


def complete(task):
    task = copy.deepcopy(task)
    task.state = TaskState.Complete
    return task

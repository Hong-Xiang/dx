""" 
A **Representation** of task
Since it is only a representation, it is not mutable, it has only properties.
No action is allowed.


"""
import json
import yaml
import copy
from dxpy.file_system.path import Path
from dxpy.time.utils import strf
from dxpy.task.misc import TaskState


class Task:
    def __init__(self, tid, desc, workdir, workers, activity, state, time_stamps, dependency):
        self.id = tid
        self.desc = desc
        self.workdir = workdir
        self.workers = workers
        self.desc = desc
        self.time_stampes = time_stamps
        self.dependency = dependency
        self.state = state

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


def py2json(task):
    return json.dumps({
        'id': task.id,
        'desc': task.desc,
        'body': yaml.dump(task),
        'dependency': task.dependency,
        'time_create': strf(task.time_stampes.start),
        'state': task.state.name,
    })


def json2yml(task):
    return json.loads(task)['body']


def json2py(task):
    return yml2py(json2yml(task))


def yml2py(task):
    return yaml.load(task)


def submit(task):
    task = copy.copy(task)
    task.state = TaskState.Pending
    return task


def run(task):
    task = copy.copy(task)
    task.state = TaskState.Runing
    return task


def complete(task):
    task = copy.copy(task)
    task.state = TaskState.Complete
    return task


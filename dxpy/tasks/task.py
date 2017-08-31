"""
==================
Task system design
==================

Task
====

Overview
--------
Task object is a *representation* of a logical task, which is designed to be:
#. 
#. 

Features
--------
#. self content
    A task object contains **ALL** information to perform a task with the help of task server.
#. subtask list
    A task may be consisted by multiple subtasks. There are two type of tasks, 
#. task state inspect
#. task serilization, database support (Optional)
    retrieve task from file, or database


Task server
-----------
#. Task factory
#. Task query
    #. on running
    #. history (recent)

#. List of tasks
#. Create(Load Tasks):
    #. create from scrach
    #. from file
        #. given path
        #. from database 




SLURM => Resource Unlimited
(Pending system)
OS, Hardware => Resource Limited
"""

from enum import Enum
import os
import sys
import copy
import yaml
import logging
from collections import deque
from dxpy.file_system.path import Path
from dxpy.time import TimeStamp
from dxpy.utils import Tags


logger = logging.getLogger(__name__)

PATHDEFAULT = '/tmp/tasks'


class TaskStateCode(Enum):
    Undifined = 0x0000
    WaitingToSubmit = 0x0001
    Pending = 0x0002
    Runing = 0x0004
    Finished = 0x0008
    Locked = 0x0100


class TaskState(yaml.YAMLObject):
    yaml_tag = '!task_state'
    RUNMASK = 0x0001

    @staticmethod
    def _normalize_value(value):
        if value is None:
            value = TaskStateCode.WaitingToSubmit
        if isinstance(value, (TaskStateCode, TaskState)):
            value = value.value
        return value

    def __init__(self, code_or_value=None):
        self.value = TaskState._normalize_value(code_or_value)

    def __or__(self, code_or_value):
        return TaskState(self.value | TaskState._normalize_value(code_or_value))

    def __and__(self, code_or_value):
        return TaskState(self.value & TaskState._normalize_value(code_or_value))

    def __inv__(self, code_or_value):
        return TaskState(~TaskState._normalize_value(code_or_value))

    def format(self):
        return [c.name for c in TaskStateCode if c.value & self.value] or [TaskStateCode.Undifined.name]

    @classmethod
    def parse(cls, states):
        result = TaskStateCode.Undifined.value
        for s in states:
            for c in TaskStateCode:
                if s == c.name:
                    result = result | c.value
        return TaskState(result)

    @classmethod
    def to_yaml(cls, dumper, data):
        vs = data.format()
        value = [yaml.ScalarNode(
            tag='tag:yaml.org,2002:str', value=s) for s in vs]
        return yaml.SequenceNode(cls.yaml_tag, value=value)

    @classmethod
    def from_yaml(cls, loader, node):
        data = loader.construct_sequence(node)
        return TaskState.parse(data)

    def __str__(self):
        return yaml.dump(self)

    def finish(self):
        self.value = self.value & TaskState.RUNMASK | TaskStateCode.Finished.value

    def submit(self):
        self.value = self.value & TaskState.RUNMASK | TaskStateCode.Pending.value

    def run(self):
        self.value = self.value & TaskState.RUNMASK | TaskStateCode.Runing.value

    def lock(self):
        self.value = self.value | TaskStateCode.Locked.value

    def free(self):
        self.value = self.value | ~TaskStateCode.Locked.value


class Task(yaml.YAMLObject):
    yaml_tag = '!task'
    yaml_flow_style = False

    def __init__(self, tid, name=None, workdir=None, state=None, *, time_stamp=None, desc=None, sub_tasks=None, is_lock=False):
        self.id = tid
        self.name = name or Tags.undifined
        self.workdir = workdir or Path(
            PATHDEFAULT) / 'task_{tid:d}.yaml'.format(tid=self.id)
        self.desc = desc or Tags.undifined
        self.time = time_stamp or TimeStamp()
        self.pre = []
        self.state = state or TaskState()

    @property
    def is_fin(self):
        self.pull()
        if (self.state & TaskStateCode.Finished).value > 0:
            return True
        else:
            return False

    @property
    def is_to_run(self):
        self.pull()
        return all(t.is_fin for t in self.pre) and not self.is_lock and not self.is_fin

    @property
    def is_lock(self):
        if (self.state & TaskStateCode.Locked).value > 0:
            return True
        else:
            return False

    def run(self):
        self.lock()
        self.state.run()
        self.push()
        result = self._run_kernel()
        return result

    def _run_kernel(self):
        pass

    def check_state(self):
        pass

    def pull(self):
        tsk = TaskService.get(id=self.id)
        self.__dict__ == copy.deepcopy(tsk.__dict__)

    def push(self):
        TaskService.put(id=self.id, task=self)

    def submit(self):
        RunService.post(self.id)
        self.state.submit()
        self.push()

    def lock(self):
        self.state.lock()
        self.push()

    def free(self):
        self.state.free()
        self.push()

    def finish(self):
        self.state.finish()
        self.free()

    def set_state(self, state):
        if isinstance(state, str):
            state = TaskState.parse(state)
        self.state = state
        self.push()

    def __str__(self):
        return yaml.dump(self)

    def tasks_to_run(self):
        result = []
        self.pull()
        if self.is_to_run:
            result.append(self)
        else:
            for t in self.pre:
                result += t.tasks_to_run()
        return result

    def wait(self, tsks):
        self.pre.append(tsks)
        self.push()
        return self


class TaskService:
    """
    Manipulation of task *representation* objects.

    Functions:
    ----------

    new(task_type, *args, **kwargs):

    """
    TASKS = []

    @classmethod
    def new(cls, task_type, *args, **kwargs):
        id_next = len(TaskService.TASKS)
        if isinstance(task_type, str):
            task_type = getattr(sys.modules[__name__], task_type)
        TaskService.TASKS.append(task_type(id_next, *args, **kwargs))
        return TaskService.get(id_next)

    @classmethod
    def get(cls, id=None):
        return TaskService.TASKS[id]

    @classmethod
    def get_all(cls, filter_func=None):
        if filter_func is None:
            return TaskService.TASKS
        else:
            return [t for t in TaskService.TASKS if filter_func(t)]

    @classmethod
    def put(cls, id, task):
        while len(TaskService.TASKS) < id + 1:
            TaskService.TASKS.append(None)
        TaskService.TASKS[id] = task

    # TODO: delete?
    @classmethod
    def update_state(cls, id,  new_state):
        task = TaskService.get(id)
        if isinstance(new_state, str):
            new_state = TaskState.parse(new_state)
        task.state = new_state
        task.push()
        return TaskService.get(id)

    # TODO: delete?
    @classmethod
    def add_wait(cls, id_post, id_pre):
        task_post = TaskService.get(id_post)
        task_pre = TaskService.get(id_pre)
        task_post.wait(task_pre)
        task_post.push()
        return TaskService.get(id_post)

    @classmethod
    def delete(cls, id):
        TaskService.TASKS.pop(id)


class RunService:
    """ run commands of tasks
    """
    IDTORUN = deque()
    TASKSPERCYCLE = 10

    @classmethod
    def get(cls, index):
        return TaskService.get(RunService.TORUN[index])

    @classmethod
    def get_all(cls):
        return [TaskService.get(i) for i in RunService.IDTORUN]

    @classmethod
    def post(cls, tid):
        RunService.IDTORUN.append(tid)

    @classmethod
    def put(cls, index, tid):
        RunService.IDTORUN[index] = tid

    @classmethod
    def delete(cls, tid):
        RunService.IDTORUN.remove(tid)

    @classmethod
    def run_cycle(cls):
        logger.debug('RunService.run_cycle() called.')
        task_left = RunService.TASKSPERCYCLE
        to_append_next_cycle = []
        while (task_left > 0 and len(RunService.IDTORUN) > 0):
            tid = RunService.IDTORUN.popleft()
            logger.debug('popleft: {tid:d}'.format(tid=tid))
            task_now = TaskService.get(tid)
            if task_now.is_to_run:
                task_now.run()
                task_left -= 1
            else:
                RunService.IDTORUN.extend(
                    [t.id for t in task_now.tasks_to_run()])
                to_append_next_cycle.append(tid)
        RunService.IDTORUN.extend(to_append_next_cycle)


class TaskCommand(Task):
    def __init__(self, *args, command=None, is_print=True, **kwargs):
        logger.debug(type(self))
        super(TaskCommand, self).__init__(*args, **kwargs)
        self.command = command
        self.is_print = is_print

    def _run_kernel(self):
        result = os.popen(self.command)
        self.free()
        self.state = self.state & ~TaskState.RUNMASK | TaskStateCode.Finished
        self.push()
        result = result.read()
        if self.is_print:
            print(result)
        self.finish()
        self.push()
        return result


class TaskSleep(TaskCommand):
    COMMAND = 'echo TaskSleep.{name}.start && sleep 1 && echo TaskSleep.{name}.end'

    def __init__(self, *args, **kwargs):
        super(TaskSleep, self).__init__(
            *args, **kwargs)
        self.command = TaskSleep.COMMAND.format(name=self.name)


class TaskChain(Task):
    def __init__(self, *args, **kwargs):
        super(TaskChain, self).__init__(*args, **kwargs)
        ts = []
        for i in range(3):
            ts.append(TaskService.new(TaskSleep, 'chain_{:d}'.format(i)))
        self.wait(ts)

    def run(self):
        return None

# from flask_restful import Resource

# class TaskResource(Resource):
#     def get(self, id):
#         return str(TaskService.get(id))


# class Task_:
#     def __init__(self,
#                  task_id,
#                  path_work,
#                  path_json=None,
#                  name=None,
#                  desc=None,
#                  prog_bar=None):
#         self.id = task_id
#         self.path_work = str(Path(path).absolute())
#         self.path_json = path_json or "t{id}.json".format(id=self.id)
#         self.name = name or "task_{0:d}".format(_id)
#         self._prog_bar = prog_bar or ProgBar(
#             1, message='ProgBar of task {tname}.'.format(name=self._name))
#         self.desc = desc or ""

#     @property
#     def prog_bar(self):
#         return self._prog_bar

#     class _JSONEncoder(json.JSONEncoder):
#         """ JSON encoder of ProgBar cls """

#         def default(self, obj):
#             if isinstance(obj, Task):
#                 dct = {
#                     '__Task__': True,
#                     'name': obj.name,
#                     'id': obj.id,
#                     'prog_bar': obj.prog_bar.to_json()
#                     'path': obj.path
#                 }
#             return dct
#             return json.JSONEncoder.default(self, obj)

#     @staticmethod
#     def json_decoder(dct):
#         """ JSON decoder of ProgBar cls """
#         if '__Task__' in dct:
#             task_id = dct['id']
#             task_path = dct['path']
#             name = dct.get('name')
#             prog_bar = ProgBar.from_json(dct['prog_bar'])
#             return Task(task_id=task_id, path=task_path, name=name, prog_bar=prog_bar)
#         else:
#             return dct

#     def to_json(self):
#         return json.dumps(self, cls=Task._JSONEncoder)

#     @staticmethod
#     def from_json(s):
#         return json.loads(s, object_hook=Task.json_decoder)

#     # For test only, time stamp is not intend to save to database
#     db_model = None

#     @staticmethod
#     def get_db_model(db):
#         if Task.db_model is None:
#             class TaskDatabaseModel(db.Model):
#                 name = db.Column(db.String(255))
#                 path_work = db.Column(db.String(512))
#                 path_json = db.Column(db.String(512))
#                 prog = db.Column(db.Float)
#                 start = db.Column(db.Float)
#                 desc = db.Column(db.Text)

#                 def __init__(self, name, path_json, path_work, prog, start, desc):
#                     self.name = name
#                     self.path_json = path_json
#                     self.path_work = path_work
#                     self.prog = prog
#                     self.start = start
#                     self.desc = desc
#             Task.db_model = TaskDatabaseModel
#             return TaskDatabaseModel
#         else:
#             return Task.db_model

#     @staticmethod
#     def from_dbobj(obj):
#         path_json = obj.path_json
#         return Task.from_json(path_json)

#     def to_dbobj(self, db):
#         return self.get_db_model(db)(self.name, self.path_json, self.path_work, self.prog_bar.progress, self.prog_bar.start, self.desc)

#     def update_dbobj(self, db):
#         tsk = Task.get_db_model(db).query.get(self.id)
#         tsk['name'] = self.name
#         tsk['path_json'] = self.path_json
#         tsk['path_work'] = self.path_work
#         tsk['progress'] = self.prog_bar.progress
#         tsk['start'] = self.prog_bar.start
#         tsk['desc'] = self.desc
#         db.session.commit()

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

from rx import Observable
from rx.concurrency import ThreadPoolScheduler

NB_THREADS = 5

logger = logging.getLogger(__name__)
pool_scheduler = ThreadPoolScheduler(NB_THREADS)


class TaskState(yaml.YAMLObject):
    yaml_tag = '!task_state'

    class RunState(Enum):
        Undifined = 0x0000
        WaitingToSubmit = 0x0001
        Pending = 0x0002
        Runing = 0x0003
        Finished = 0x0004

    class LockState(Enum):
        Free = 0x0000
        Locked = 0x0010

    @staticmethod
    def _normalize_value(value):
        if value is None:
            value = TaskState.RunCode.Undifined
        if isinstance(value, (TaskStateCode, TaskState)):
            value = value.value
        return value

    def __init__(self, run_state=None, lock_state=None):
        if run_state is None:
            run_state = TaskState.RunState.WaitingToSubmit
        if lock_state is None:
            lock_state = TaskState.LockState.Free
        self.run = run_state
        self.lock = lock_state

    def format(self):
        return [self.run.name, self.lock.name]

    @classmethod
    def parse(cls, states):
        for s in TaskState.RunState:
            if s.name == states[0]:
                rs = s
        for s in TaskState.LockState:
            if s.name == states[1]:
                ls = s
        return TaskState(rs, ls)

    @classmethod
    def to_yaml(cls, dumper, data):
        vs = data.format()
        value = [yaml.ScalarNode(
            tag='tag:yaml.org,2002:str', value=s) for s in vs]
        return yaml.SequenceNode(cls.yaml_tag, value=value)

    @classmethod
    def from_yaml(cls, loader, node):
        data = loader.construct_sequence(node)
        if len(data) == 1:
            data = data + [TaskState.LockState.Free.name]
        return TaskState.parse(data)

    def __str__(self):
        return yaml.dump(self)

    @property
    def is_waiting_to_submit(self):
        return self.run == self.RunState.WaitingToSubmit

    @property
    def is_pending(self):
        return self.run == self.RunState.Pending

    @property
    def is_runing(self):
        return self.run == self.RunState.Runing

    @property
    def is_complete(self):
        return self.run == self.RunState.Finished

    @property
    def is_lock(self):
        return self.lock == self.LockState.Locked


class Task(yaml.YAMLObject):
    yaml_tag = '!task'
    yaml_flow_style = False

    def __init__(self, tid, name=None, workdir=None, state=None, *, time_stamp=None, desc=None, sub_tasks=None, is_lock=False):
        self.id = tid
        self.name = name or Tags.undifined
        self.workdir = Path(workdir) or self._default_workdir()
        self.desc = desc or Tags.undifined
        self.time = time_stamp or TimeStamp()
        self.pre = []
        self.state = state or TaskState()

    def _default_workdir(self):
        return Path('.')

    # @property
    # def is_waiting_to_submit(self):
    #     self.pull()
    #     return self.state.is_waiting_to_submit

    # @property
    # def is_pending(self):
    #     self.pull()
    #     return self.state.is_pending

    # @property
    # def is_running(self):
    #     self.pull()
    #     return self.state.is_runing

    # @property
    # def is_complete(self):
    #     self.pull()
    #     return self.state.is_complete

    def dependence(self):
        from dxpy.task.service import TaskStoreService
        return (Observable.from_(self.pre)
                .map(lambda i: TaskStoreService.get(i)))

    @property
    def is_to_run(self):
        from dxpy.task.service import TaskStoreService
        self.pull()
        return all(TaskStoreService.get(t).state.is_complete for t in self.pre) and not self.state.is_lock and self.state.is_pending

    # @property
    # def is_lock(self):
    #     self.pull()
    #     return self.state.lock == TaskState.LockState.Locked

    def run(self):
        """
        **NO** finish report here.
        """
        self._pre_run()
        a_run = (Observable.just('Run')
                 .map(lambda s: self._run_kernel())
                 .subscribe_on(pool_scheduler))
        a_run.subscribe(on_next=lambda res: self._post_run(
            res), on_error=lambda e: print(e))

        # self._post_run(self._run_kernel())

    def _pre_run(self):
        self.lock()
        self.state.run = TaskState.RunState.Runing
        self.push()

    def _run_kernel(self):
        pass

    def _post_run(self, result):
        pass

    def check_state(self):
        pass

    def pull(self):
        from dxpy.task.service import TaskStoreService
        tsk = TaskStoreService.get(self.id)
        self.__dict__ == copy.deepcopy(tsk.__dict__)

    def push(self):
        from dxpy.task.service import TaskStoreService
        TaskStoreService.update(self)

    def submit(self):
        self.state.run = TaskState.RunState.Pending
        self.push()

    def lock(self):
        self.state.lock = TaskState.LockState.Locked
        self.push()

    def free(self):
        self.state.lock = TaskState.LockState.Free
        try:
            self.push()
        except Exception as e:
            with open('errorlog.txt', 'w') as fout:
                print(e, file=fout)

    def check_complete(self):
        pass

    def finish(self):
        self.state.run = TaskState.RunState.Finished
        self.free()
        self.push()

    def __str__(self):
        return yaml.dump(self)

    def tasks_pre_to_run(self):
        """
        () -> Observable<Task[]>
        """
        self.pull()
        if self.is_to_run:
            return Observable.empty()
        else:
            can_run = (self.dependence()
                       .filter(lambda t: t.is_to_run)
                       .flat_map(lambda t: Observable.just(t)))
            has_pre = (self.dependence()
                       .filter(lambda t: not t.is_to_run)
                       .flat_map(lambda t: t.dependence()))
            return Observable.merge(can_run, has_pre)

    def wait(self, tsks):
        self.pre.append(tsks.id)
        self.push()


class TaskCommand(Task):
    def __init__(self, *args, command=None, is_print=True, **kwargs):
        logger.debug(type(self))
        super(TaskCommand, self).__init__(*args, **kwargs)
        self.command = command
        self.is_print = is_print

    def _run_kernel(self):
        result = os.popen(self.command).read()
        return result

    def _post_run(self, result):
        if self.is_print:
            print(result)
        self.finish()


class TaskSbatch(Task):
    from dxpy.slurm import Slurm

    def __init__(self, *args, sfile, **kwargs):
        logger.debug(type(self))
        super(TaskSbatch, self).__init__(*args, **kwargs)
        self.sfile = sfile
        self.sid = None
        self.cmd = 'cd {dir}'.format(dir=self.workdir.abs)
        self.cmd += ' && sbatch {file}'.format(file=self.sfile)

    def _run_kernel(self):
        result = os.popen(self.cmd).read()        
        return TaskSbatch.Slurm().get_id(result)

    def check_complete(self):        
        for info in TaskSbatch.Slurm().sinfo():
            if int(info.id) == int(self.sid):
                return None
        self.finish()

    def _post_run(self, result):
        self.sid = result
        self.push()

from collections import namedtuple
import copy
import rx
import dask
import sys
import os
import dxpy.slurm as slurm
from .. import misc
from ..representation import templates
from .. import interface

NB_THREADS = 5
THREAD_POOL = rx.concurrency.ThreadPoolScheduler(NB_THREADS)


class Workers:
    @classmethod
    def is_complete(cls, task):
        return task.state == misc.TaskState.Complete

    @classmethod
    def on_this_worker(cls, task):
        return task.workers.type == cls.WorkerType

    @classmethod
    def plan(cls, task):
        raise NotImplementedError

    @classmethod
    def run(cls, task, stdout=None, stderr=None):
        if stdout is None:
            stdout = sys.stdout
        if stderr is None:
            stderr = sys.stderr
        (rx.Observable.just(task)
         .map(cls.plan)
         .subscribe(on_next=lambda r: print(r, file=stdout),
                    on_error=lambda e: print(e, file=stderr)))


class NoAction(Workers):
    WorkerType = misc.WorkerType.NoAction

    @classmethod
    def plan(cls, task):
        task = interface.mark_start(task)
        task = interface.mark_complete(task)
        return 'NoAction of task id: {} done.'.format(task.id)


class Slurm(Workers):
    WorkerType = misc.WorkerType.Slurm

    @classmethod
    def is_complete(cls, task):
        return slurm.is_complete(task.workers.info)

    @classmethod
    def plan(cls, task):
        def add_sid(sid):
            t = copy.deepcopy(task)
            t.workers.info = {'sid': sid}

        assert isinstance(
            task, TaskScript), 'Only TaskScript is supported: {!r}'.format(task)

        return (task.plan(interp='sbatch')
                .map(slurm.sid_from_submit)
                .map(add_sid)
                .map(update))


WORKERS = [NoAction, Slurm]


def get_workers(task):
    for w in WORKERS:
        if w.on_this_worker(task):
            return w


class MultiThreding(Workers):
    WorkerType = misc.WorkerType.MultiThreading

    @classmethod
    def plan(cls, task):
        # TRT = namedtuple('TaskResultTuple', ('task', 'res'))
        with os.popen(task.command()) as fin:
            result = fin.readlines()
        return task, result


# class Dask(Workers):
#     WorkerType = misc.WorkerType.Dask
#     NB_PROCESSES = 5

#     @classmethod
#     def run_plan(cls, task):
#         (rx.Observable.just(task.workers.num_workers)
#          .map(lambda i: dask.delayed(task.run)(i_worker=i))
#          .to_list()
#          .map(lambda l: dask.bag.from_delayed(l))
#          .map(lambda b: b.compute(num_workers=NB_PROCESSES)))

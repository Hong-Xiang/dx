from collections import namedtuple
import copy
import rx
import dask
import sys
import os
import dxpy.slurm as slurm
from ..representation import task as taskpy
from ..representation import creators
from .. import interface

NB_THREADS = 5
THREAD_POOL = rx.concurrency.ThreadPoolScheduler(NB_THREADS)


class Workers:
    @classmethod
    def is_complete(cls, task):
        return task.state == taskpy.State.Complete

    @classmethod
    def on_this_worker(cls, task):
        return task.worker == cls.WorkerType

    @classmethod
    def plan(cls, task):
        raise NotImplementedError

    @classmethod
    def run(cls, task, stdout=None, stderr=None):
        print("RUN CALLED.")
        if stdout is None:
            stdout = sys.stdout
        if stderr is None:
            stderr = sys.stderr
        (rx.Observable.just(task)
         .map(cls.plan)
         .subscribe_on(THREAD_POOL)
         .subscribe(on_next=lambda r: print(r, file=stdout),
                    on_error=lambda e: print(e, file=stderr)))


class NoAction(Workers):
    WorkerType = taskpy.Worker.NoAction

    @classmethod
    def plan(cls, t):
        t = interface.mark_start(t)
        t = interface.mark_complete(t)
        return 'NoAction of task id: {} done.'.format(t.id)


class Slurm(Workers):
    WorkerType = taskpy.Worker.Slurm

    @classmethod
    def is_complete(cls, task):
        return slurm.is_complete(task.workers.info['sid'])

    @classmethod
    def plan(cls, task, *args):
        # why?
        # TODO: FIX
        # print(args)
        # raise ValueError('task {0}, args: {1}'.format(task, args))
        # def srun_command(workdir, command):
        #     return 'cd {0} && srun {1}'.format(workdir, command)

        def sbatch_command(workdir, script_file):
            return 'cd {0} && sbatch {1}'.format(workdir, script_file)
        task = interface.mark_start(task)
        # if isinstance(task, templates.TaskCommand):
        #     command = task.command(srun_command)
        if not isinstance(task, templates.TaskScript):
            raise TypeError(
                'Slurm worker only support TaskScript tasks, got: {!r}.'.format(task))
        command = task.plan(sbatch_command)
        with os.popen(command) as fin:
            result = fin.readlines()[0]
        sid = slurm.sid_from_submit(result)
        task.workers.info = {'sid': sid}
        interface.update(task)
        return result


class MultiThreding(Workers):
    WorkerType = taskpy.Worker.MultiThreading

    @classmethod
    def plan(cls, task):
        # TRT = namedtuple('TaskResultTuple', ('task', 'res'))
        with os.popen(task.command()) as fin:
            result = fin.readlines()
        return task, result


WORKERS = [NoAction, MultiThreding, Slurm]


def get_workers(task):
    for w in WORKERS:
        if w.on_this_worker(task):
            return w

# class Dask(Workers):
#     WorkerType = taskpy.Worker.Dask
#     NB_PROCESSES = 5

#     @classmethod
#     def run_plan(cls, task):
#         (rx.Observable.just(task.workers.num_workers)
#          .map(lambda i: dask.delayed(task.run)(i_worker=i))
#          .to_list()
#          .map(lambda l: dask.bag.from_delayed(l))
#          .map(lambda b: b.compute(num_workers=NB_PROCESSES)))

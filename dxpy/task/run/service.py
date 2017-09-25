import sys
import rx
from rx.concurrency import ThreadPoolScheduler
from ..representation import submit, start, complete
from ..interface import read, read_all, update, dependencies
from .. import interface as ti
from .workers import Workers, Slurm

SUPPORTED_WORKERS = [Slurm]


def read_complete_tasks_on_worker(worker) -> 'rx.Observable<Task>':
    return (ti.read_all_running()
            .filter(w.on_this_worker)
            .filter(w.is_complete))


def auto_complete():
    for w in SUPPORTED_WORKERS:
        tasks = (read_complete_tasks_on_worker(w)
                 .map(ti.mark_complete)
                 .subscribe())


def auto_submit():
    (read_all()
     .filter(lambda t: t.is_pending)
     .flat_map(dependencies)
     .filter(lambda t: t.is_before_submit)
     .map(ti.mark_submit)
     .subscribe())


def all_dependencies_complete(task):
    return (store.dependencies(task)
            .all(lambda t: t.is_complete))


def auto_start():
    task_pending = read_all().filter(lambda t: t.is_pending)
    task_run_flag = task_pending.flat_map(all_dependencies_complete)
    (task_pending.zip(task_run_flag)
     .filter(x: x[1])
     .map(ti.mark_start)
     .subscribe())

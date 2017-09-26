import sys
import rx
from rx.concurrency import ThreadPoolScheduler
from .. import interface
from . import workers

SUPPORTED_WORKERS = []


def read_complete_tasks_on_worker(worker) -> 'rx.Observable<Task>':
    return (interface.read_all()
            .filter(lambda t: t.is_running)
            .filter(w.on_this_worker)
            .filter(w.is_complete))


def auto_complete():
    for w in SUPPORTED_WORKERS:
        tasks = (read_complete_tasks_on_worker(w)
                 .map(lambda t: t.id)
                 .subscribe(interface.mark_complete))


def auto_submit_root():
    (interface.read_all()
     .filter(lambda t: t.is_before_submit)
     .filter(lambda t: t.is_root)     
     .subscribe(interface.mark_submit))


def auto_submit_chain():
    (interface.read_all()
     .filter(lambda t: t.is_pending)
     .flat_map(interface.dependencies)
     .filter(lambda t: t.is_before_submit)     
     .subscribe(interface.mark_submit))


def is_dependencies_complete(task):
    return (interface.dependencies(task)
            .all(lambda t: t.is_complete))

# def start(task):
#     w = workers.
def auto_start():
    tasks = (interface.read_all()
             .filter(lambda t: t.is_pending))
    (rx.Observable.zip_array(tasks,
                             tasks.flat_map(is_dependencies_complete))
     .filter(lambda x: x[1])
     .map(lambda t: t.id)
     .subscribe(interface.mark_start))

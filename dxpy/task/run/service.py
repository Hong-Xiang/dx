import sys
import rx
from rx.concurrency import ThreadPoolScheduler
from .. import interface
from . import workers
from .. import provider

SUPPORTED_WORKERS = [workers.Slurm]


def start(task):
    workers.get_workers(task).run(task)


def read_complete_tasks_on_worker(worker) -> 'rx.Observable<Task>':
    return (interface.read_all()
            .filter(lambda t: t.is_running)
            .filter(worker.on_this_worker)
            .filter(worker.is_complete))


def auto_complete():
    for w in SUPPORTED_WORKERS:
        tasks = (read_complete_tasks_on_worker(w)
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
     .map(lambda x: x[0])
     .subscribe(start))


def cycle():
    auto_complete()
    auto_submit_root()
    auto_submit_chain()
    auto_start()
    print('Cycle.')


def launch_deamon(interval=1000):
    configs = provider.get_or_create_service('config')
    configs.set_config_by_name_key('database', 'use_web_api', True)
    rx.Observable.interval(interval).start_with(0).subscribe(
        on_next=lambda t: cycle(), on_error=lambda e: print(e))

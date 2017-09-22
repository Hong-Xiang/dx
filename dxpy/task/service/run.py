import sys
import rx
from rx.concurrency import ThreadPoolScheduler
import dxpy.task.reps.taskpy as rep
import dxpy.task.service.store as store


class TaskRunService:
    """ run commands of tasks
    """
    @classmethod
    def check_complete(cls):
        from dxpy.task.task import TaskSbatch
        (
            TaskStoreService.all()
            .filter(lambda t: t.state.run == t.state.RunState.Runing)
            .filter(lambda t: isinstance(t, TaskSbatch))
            .subscribe(lambda t: t.check_complete())
        )

    @classmethod
    def submit(cls):
        (
            TaskStoreService.all()
            .filter(lambda t: t.state.run == t.state.RunState.Pending)
            .filter(lambda t: not t.is_to_run)
            .flat_map(lambda t: t.dependence())
            .filter(lambda t: t.state.is_waiting_to_submit)
            .subscribe(lambda t: t.submit())
        )

    @classmethod
    def run(cls):
        (
            TaskStoreService.all()
            .filter(lambda t: t.is_to_run)
            .subscribe(lambda t: t.run())
        )

    @classmethod
    def cycle(cls):
        TaskRunService.check_complete()
        TaskRunService.submit()
        TaskRunService.run()

    @classmethod
    def launch_deamon(cls, interval=10000):

    @classmethod
    def mark_as_finish(self, id_or_task):
        if isinstance(id_or_task, int):
            task = self.get(id_or_task)
        else:
            task = id_or_task
        task.finish()


def complete(task_or_tid):
    if isinstance(task_or_tid, rep.TaskPy):
        source = rx.Observable.rx.Observable.just(task_or_tid)
    else:
        source = store.read(task_or_tid)
    (source
     .map(rep.complete)
     .map(lambda t: t.to_json)
     .map(store.update)
     .subscribe())


def check_complete_slurm(task):
    if task.


def auto_submit():
    (store.read_all()
     .filter(lambda t: t.is_pending)
     .flat_map(store.dependencies)
     .filter(lambda t: t.is_before_submit)
     .map(rep.submit)
     .subscribe(store.update))


def all_dependencies_complete(task):
    return (store.dependencies(task)
            .all(lambda t: t.is_complete))


def auto_run():
    # task_pending = store.read_all().filter(lambda t: t.is_pending)
    # task_run_flag = task_pending.map(store.dependencies).map(lambda ts: ts.all(lambda t: ))
    #  .map(lambda t_and)
    #  .)
    pass


def cycle_kernel():
    check_complete()
    auto_submit()
    auto_run()


def launch_deamon(cycle_intervel=None):
    (Observable.interval(interval).start_with(0)
     .subscribe(on_next=lambda i: cycle_kernel(),
                on_error=lambda e: print(e, file=sys.stderr)))


class DeamonService:
    @staticmethod
    def start():
        launch_deamon()

    @staticmethod
    def stop():
        raise NotImplementedError

    @staticmethod
    def restart():
        raise NotImplementedError

    @staticmethod
    def is_running():
        pass

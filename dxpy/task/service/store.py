import copy
import rx
import json
from rx.concurrency import ThreadPoolScheduler
from dxpy.task.reps.taskpy import json2py, py2json, submit, run, complete
from dxpy.task.database.web import Service as db_service


def create(task_cls, *args, **kwargs):
    """ Create a generic task representation.    
    """
    tid = _DatabaseService().add(path, name)
    # if isinstance(task_cls, str):
    #     task_cls = get_task_cls(task_cls)
    task = task_cls(tid, name, *args, **kwargs)
    _FileService.append(path, task)
    return tid

def read(tid):
    return db_service.read(tid)


    
    


def get_path(cls, id_):
    """
    Returns:
        path: str, path of .yaml file saving task.
    """
    tdb = _DatabaseService().get(id_)
    if tdb:
        return tdb.path
    else:
        return None


def get(cls, id_):
    """
    Returns:
        task: Task.
    Raises:
        FileNotFoundError:            
    """
    for t in _FileService.get(TaskStoreService.get_path(id_)):
        if t.id == id_:
            return t
    return None


def all(cls, filter_func=None):
    """
    (filter_func) -> Observable<Task[]>
    """
    if filter_func is None:
        def filter_func(x): return x is not None
    return (_DatabaseService().all()
            .map(lambda tdb: TaskStoreService.get(tdb.id))
            .filter(filter_func))


def update(cls, task):
    _FileService.append(TaskStoreService.get_path(task.id),
                        task)


def submit(self, tid):
    # rx.Observable.just(db_service.read(tid)).subscribe_on(ThreadPoolScheduler()).map(json2py)
    # task_json =

    # task_
    pass


def delete(self, tid):
    tsk = TaskStoreService.get(id_)
    _FileService.delete(TaskStoreService.get_path(id_),
                        TaskStoreService.get(id_))
    _DatabaseService().delete(tsk.id)

"""
This moudule is designed to be stateless (pure interface):
    No data members
    No Deamon process
Works
"""
import copy
import rx
import json
import rx
from . import provider
from .representation import TaskPy
from . import representation as reps


def db():
    return provider.get_or_create_service('database')


def create(task: TaskPy) -> int:
    return db().create(task.to_json())


def create_graph(task_graph) -> 'list<int>':
    done = []
    for t in task_graph:
        t.id = None

    def all_dependency_added(task):
        return all([t in done for t in task_graph.depens(task)])

    while len(done) < len(task_graph):
        (rx.Observable.from_(task_graph.nodes())
         .filter(lambda t: not t in done)
         .filter(all_dependency_added)
         .map(lambda t: t.id=create(t))
         .subscribe())


def parse_json(s: 'json string'):
    return TaskPy.from_json(s)


def read(tid: int) -> 'TaskPy':
    return parse_json(db().read(tid))


def read_all() -> 'Observable<TaskPy>':
    return (db().read_all()
            .map(parse_json))


def read_all_running() -> 'Observable<TaskPy>':
    return read_all().filter(lambda t: t.is_running)


def dependencies(task: TaskPy) -> 'Observable<TaskPy>':
    return rx.Observable.from_(task.dependency).map(read)


def update(task: TaskPy) -> None:
    db().update(task.to_json())


def mark_submit(tid) -> None:
    update(reps.submit(read(tid)))


def mark_start(tid) -> None:
    update(reps.start(read(tid)))


def mark_complete(tid) -> None:
    update(reps.complete(read(tid)))


def delete(tid: int) -> None:
    db().delete(tid)

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
from . import database as db
from .representation import task as ts


def create(task) -> int:
    return db.create(task.to_json())


def create_graph(task_graph) -> 'list<int>':
    done = []
    for t in task_graph.nodes():
        t.id = None

    def all_dependency_added(task):
        return all([t in done for t in task_graph.dependencies(task)])

    def update_dependency(task):
        task.dependency = [t.id for t in task_graph.dependencies(task)]
        return task

    def add_to_done(task):
        done.append(task)
        return task

    def create_and_update_id(task):
        task.id = create(task)
        return task

    while len(done) < len(task_graph):
        (rx.Observable.from_(task_graph.nodes())
         .filter(lambda t: not t in done)
         .filter(all_dependency_added)
         .map(update_dependency)
         .map(create_and_update_id)
         .map(add_to_done)
         .subscribe())

    return [t.id for t in done]


def parse_json(s: 'json string'):
    return ts.Task.from_json(s)


def read(tid: int):
    if not isinstance(tid, int):
        raise TypeError("read only accept tid of int type: {!r}".format(tid))
    return parse_json(db.read(tid))


def read_all() -> 'Observable<TaskPy>':
    return (db.read_all()
            .map(parse_json))


def dependencies(task) -> 'Observable<TaskPy>':
    return rx.Observable.from_(task.dependency).map(read)


def update(task) -> None:
    db.update(task.to_json())
    return task


def mark_submit(task) -> None:
    return update(ts.submit(task))


def mark_start(task) -> None:
    return update(ts.start(task))


def mark_complete(task) -> None:
    return update(ts.complete(task))


def delete(tid: int) -> None:
    db.delete(tid)

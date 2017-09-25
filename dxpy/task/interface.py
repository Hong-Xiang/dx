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
from .provider import Provider
from .representation import TaskPy
from . import representation as reps


def create(task: TaskPy) -> int:
    return db.create(task.to_json())


def parse_json(s: 'json string'):
    return TaskPy.from_json(s)


def read(tid: int) -> 'TaskPy':
    return parse_json(db.read(tid))


def json_list_to_observale(observable_jsons):
    return (rx.Observable.just(observable_jsons)
            .map(json.loads)
            .flat_map(lambda x: rx.Observable.from_(x))
            .map(json.dumps))


def read_all() -> 'Observable<TaskPy>':
    return (rx.Observable.just(db.read_all())
            .flat_map(json_list_to_observale)
            .map(parse_json))


def read_all_running() -> 'Observable<TaskPy>':
    return read_all().filter(lambda t: t.is_running)


def dependencies(task: TaskPy) -> 'Observable<TaskPy>':
    return rx.Observable.from_(task.dependency).map(read)


def update(task: TaskPy) -> None:
    db.update(task.to_json())


def mark_submit(task: TaskPy) -> None:
    update(reps.submit(task))


def mark_start(task: TaskPy) -> None:
    update(reps.start(task))


def mark_complete(task: TaskPy) -> None:
    update(reps.complete(task))


def delete(tid: int) -> None:
    db.delete(tid)

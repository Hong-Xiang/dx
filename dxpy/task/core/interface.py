"""
This moudule is designed to be stateless (pure interface):
    No data members
    No Deamon process
Works 
"""
import copy
import rx
import json
from .. import database as db
from .taskpy import json2py, py2json


def read_all():
    return (rx.Observable.just(db.read_all())
            .map(json.loads)
            .flat_map(lambda x: rx.Observable.from_(x))
            .map(json.dumps)
            .map(json2py))

def dependencies(task):
    return rx.Observable.from_(task.dependency).map(read)


def create(task):
    return db.create(py2json(task))


def read(tid):
    return json2py(db.read(tid))


def update(task_py):
    rx.Observable.just(task_py).map(py2json).subscribe(db.update)


def delete(tid):
    db.delete(tid)

import json
import yaml
import rx
from rx.concurrency import ThreadPoolScheduler as TPS
from dxpy.time.utils import strf, strp
from ..exceptions import TaskNotFoundError
from .model import Database, TaskDB


# def dbs2json(tasks_db):
#     return json.dumps([json.loads(db2json(task_db)) for task_db in tasks_db])


def db2json(task):
    return json.dumps({
        'id': task.id,
        'desc': task.desc,
        'data': task.data,
        'time_create': strf(task.time_create),
        'time_start': strf(task.time_start),
        'time_end': strf(task.time_end)
        'state': task.state,
        'is_root': task.is_root
    })


def json2db_new(s):
    dct = json.loads(s)
    return TaskDB(desc=dct['desc'],
                  data=dct['data'],
                  state=dct['state'],
                  time_create=strp(dct['time_create']),
                  is_root=dct['is_root'])


class Service:
    session = None

    @classmethod
    def create_session(cls):
        cls.session = Database.session()

    @classmethod
    def get_or_create_session(cls, path=None):
        if cls.session is None:
            cls.create_session()
        return cls.session

    @classmethod
    def clear_session(cls):
        if cls.session is not None:
            cls.session.close()
        cls.session = None

    @classmethod
    def create(cls, task_json: str) -> int:
        """
        Create a task record in database.
        """
        task_db = json2db_new(task_json)
        cls.get_or_create_session().add(task_db)
        cls.get_or_create_session().commit()
        task_db = cls.get_or_create_session().query(TaskDB).get(task_db.id)
        return task_db.id

    @classmethod
    def read_taskdb(cls, tid):
        task_db = cls.get_or_create_session().query(TaskDB).get(tid)
        if task_db is None:
            raise TaskNotFoundError(tid)
        else:
            return task_db

    @classmethod
    def read(cls, tid=None):
        """
        Raises:
        - `TaskNotFoundError`
        """
        return db2json(cls.read_taskdb(tid))

    @classmethod
    def read_all(cls, filter_func=None) -> 'rx.Observable<json str>':
        """
        Returns JSON serilized query results;

        Returns:
        - `str`: JSON loadable observalbe

        Raises:
        - None
        """
        if filter_func is None:
            def filter_func(x): return True
        return (rx.Observable
                .from_(cls.get_or_create_session().query(TaskDB).all())
                .filter(filter_func)
                .map(db2json))

    @classmethod
    def json2db_update(cls, s):
        dct = json.loads(s)
        taskdb = cls.read_taskdb(dct['id'])
        taskdb.desc = dct['desc']
        taskdb.data = dct['data']
        taskdb.state = dct['state']
        taskdb.time_create = strp(dct['time_create'])
        taskdb.time_start = strp(dct['time_start'])
        taskdb.time_end = strp(dct['time_end'])
        taskdb.is_root = dct['is_root']
        return taskdb

    @classmethod
    def update(cls, task_json):
        cls.json2db_update(task_json, cls.get_or_create_session())
        cls.get_or_create_session().commit()

    @classmethod
    def delete(cls, tid):
        cls.get_or_create_session().delete(cls.read_taskdb(tid))
        cls.get_or_create_session().commit()

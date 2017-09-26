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
        'body': task.body,
        'dependency': (rx.Observable.just(task.dependency)
                       .subscribe_on(TPS())
                       .flat_map(lambda x: x.split(' '))
                       .filter(lambda x: x.isdigit())
                       .map(lambda x: int(x))
                       .to_list().to_blocking().first()),
        'time_create': strf(task.time_create),
        'state': task.state,
        'is_root': task.is_root
    })


def json2db_new(task_json):
    task_json = json.loads(task_json)
    return TaskDB(desc=task_json['desc'],
                  body=task_json['body'],
                  state=task_json['state'],
                  time_create=strp(task_json['time_create']),
                  depens=' '.join(task_json['dependency']),
                  is_root=task_json['is_root'])


import pdb


class Service:
    session = None

    @classmethod
    def create_session(cls):
        # TODO: tear down existed session
        cls.session = Database.session()
        cls.session.query(TaskDB).all()
        # pdb.set_trace()

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
        tpy = yaml.load(task_db.body)
        tpy.id = task_db.id
        task_db.body = yaml.dump(tpy)
        cls.get_or_create_session().commit()
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
    def read_all_old(cls, filter_func=None):
        import warnings
        """
        Returns JSON serilized query results; In `"[{task1},{task2}]"` format.

        Returns:
        - `str`: JSON loadable. Would be `"[]"` if no task in database.

        Raises:
        - None
        """
        warnings.warn("there is a new read_all method.", DeprecationWarning)
        if filter_func is None:
            def filter_func(x): return True
        return (rx.Observable
                .from_(cls.get_or_create_session().query(TaskDB).all())
                .subscribe_on(TPS())
                .filter(filter_func)
                .map(db2json)
                .map(json.loads)
                .to_list()
                .map(json.dumps)
                .to_blocking()
                .first())
        # res = session.query(TaskDB).all()
        # if res is None:
        #     res = json.dumps([])
        # return dbs2json(res)

    @classmethod
    def json2db_update(cls, task_json, session):
        task_json = json.loads(task_json)
        taskdb = cls.read_taskdb(task_json['id'])
        taskdb.desc = task_json['desc']
        taskdb.body = task_json['body']
        taskdb.state = task_json['state']
        taskdb.time_create = strp(task_json['time_create'])
        taskdb.dependency = ' '.join(task_json['dependency'])
        taskdb.is_root = task_json['is_root']
        return taskdb

    @classmethod
    def update(cls, task_json):
        cls.json2db_update(task_json, cls.get_or_create_session())
        cls.get_or_create_session().commit()

    @classmethod
    def delete(cls, tid):
        cls.get_or_create_session().delete(cls.read_taskdb(tid))
        cls.get_or_create_session().commit()

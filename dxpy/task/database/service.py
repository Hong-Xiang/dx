import json
import yaml
import rx
from rx.concurrency import ThreadPoolScheduler as TPS
from dxpy.task.database.model import DBSession, TaskDB
from dxpy.time.utils import strf, strp
session = DBSession()


class TaskNotFoundError(Exception):
    def __init__(self, tid=None):
        super(TaskNotFoundError, self).__init__(
            "Task with id: {tid} not found.".format(tid=tid))


def dbs2json(tasks_db):
    return json.dumps([json.loads(db2json(task_db)) for task_db in tasks_db])


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
    })


def json2db_new(task_json):
    task_json = json.loads(task_json)
    return TaskDB(desc=task_json['desc'],
                  body=task_json['body'],
                  state=task_json['state'],
                  time_create=strp(task_json['time_create']),
                  depens=' '.join(task_json['dependency']))


def json2db_update(task_json, session):
    task_json = json.loads(task_json)
    taskdb = session.query(TaskDB).get(task_json['id'])
    if taskdb is None:
        raise TaskNotFoundError(task_json['id'])
    taskdb.desc = task_json['desc']
    taskdb.body = task_json['body']
    taskdb.state = task_json['state']
    taskdb.time_create = strp(task_json['time_create'])
    taskdb.dependency = ' '.join(task_json['dependency'])
    return taskdb


# def json2db(task_json, session=None):
#     task_json = json.loads(task_json)
#     if task_json['id'] is not None:
#         return update_db_by_json(task_json, session)
#     else:
#         return create_new_task_db(task_json)


class Service:
    @staticmethod
    def create(task_json):
        """
        Inputs:
            task: taskJSON
        """
        task_db = json2db_new(task_json)
        session.add(task_db)
        session.commit()
        task_db = session.query(TaskDB).get(task_db.id)
        tpy = yaml.load(task_db.body)
        tpy.id = task_db.id
        task_db.body = yaml.dump(tpy)
        session.commit()
        return task_db.id

    @staticmethod
    def read(tid=None):
        """
        Returns JSON serilized query result.
        """
        task_db = session.query(TaskDB).get(tid)
        if task_db is None:
            raise TaskNotFoundError(tid)
        else:
            return db2json(task_db)

    @staticmethod
    def read_all(filter_func=None):
        """
        Returns JSON serilized query results; In "[{task1},{task2}]" format.
        Returns:
            str: JSON loadable. Would be "[]" if no task in database.
        Exception:
            None
        """
        if filter_func is None:
            def filter_func(x): return True
        return (rx.Observable.from_(session.query(TaskDB).all())
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

    @staticmethod
    def update(task_json):
        json2db_update(task_json, session)
        session.commit()

    @staticmethod
    def delete(tid):
        task_db = session.query(TaskDB).get(tid)
        if task_db is None:
            raise TaskNotFoundError
        session.delete(task_db)
        session.commit()

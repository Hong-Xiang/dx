import json
import rx
from dxpy.task.database.model import DBSession, TaskDB
from dxpy.time.utils import strf, strp
session = DBSession()


class TaskNotFoundError(Exception):
    pass


def db2json(task):
    return json.dumps({
        'id': task.id,
        'desc': task.desc,
        'body': task.body,
        'dependency': (rx.Observable.just(task.dependency)
                       .flat_map(lambda x: x.split(' '))
                       .filter(lambda x: x.isdigit())
                       .map(lambda x: int(x))
                       .to_list().to_blocking().first()),
        'time_create': strf(task.time_create),
        'state': task.state,
    })


def create_new_task_db(task_json):
    return TaskDB(desc=task_json['desc'],
                  body=task_json['body'],
                  state=task_json['state'],
                  time_create=strp(task_json['time_create']),
                  depens=' '.join(task_json['dependency']))


def update_db_by_json(task_json, session):
    task_json = json.loads(task_json)
    taskdb = session.query(TaskDB).get(task_json['id'])
    if taskdb is None:
        raise TaskNotFoundError(
            "Task with id: {tid} not found.".format(tid=task_json['id']))
    taskdb.desc = task_json['desc'],
    taskdb.body = task_json['body'],
    taskdb.state = task_json['state'],
    taskdb.time_create = strp(task_json['time_create'])
    taskdb.depens = ' '.join(task_json['dependency'])
    return taskdb


def json2db(task_json, session=None):
    task_json = json.loads(task_json)
    if task_json['id'] is not None:
        return update_db_by_json(task_json, session)
    else:
        return create_new_task_db(task_json)


class Service:
    @staticmethod
    def create(task_json):
        """
        Inputs:
            task: taskJSON
        """
        task_db = json2db(task_json)
        session.add(task_db)
        session.commit()
        return task_db.id

    @staticmethod
    def read(tid=None):
        if tid is None:
            return [db2json(t) for t in session.query(TaskDB).all()]
        else:
            task_db = session.query(TaskDB).get(tid)
            if task_db is None:
                return None
            else:
                return db2json(task_db)

    @staticmethod
    def update(task_json):
        json2db(task_json, session)
        session.commit()

    @staticmethod
    def delete(tid):
        session.delete(session.query(TaskDB).get(tid))
        session.commit()

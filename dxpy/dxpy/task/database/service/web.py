from functools import wraps
from ..exceptions import TaskDatabaseConnectionError, TaskNotFoundError


def connection_error_handle(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.ConnectionError as e:
            raise TaskDatabaseConnectionError(
                "Task database server connection failed. Details:\n{e}".format(e=e))
    return wrapper


def task_url_tpl(base):
    from ..config import config as c
    return full(c['name'], '/<int:id>', c['version'], base)


def task_url_id(base, tid):
    from ..config import config as c
    return full(c['name'], '/{tid}'.format(tid=tid), c['version'], base)


def tasks_url(base):
    from ..config import config as c
    return full(c['names'], base)


@connection_error_handle
def create(task_json):
    r = requests.post(tasks_url(), {'task': task_json})
    return r.json()['id']


@connection_error_handle
def read(tid):
    r = requests.get(task_url_id(tid))
    if r.status_code == 200:
        return r.text
    else:
        raise TaskNotFoundError(tid)


@connection_error_handle
def read_all():
    return rx.Observable.from_(json.loads(requests.get(tasks_url()).text))


@connection_error_handle
def update(task_json):
    task_json_dct = json.loads(task_json)
    r = requests.put(task_url_id(
        task_json_dct['id']), data={'task': task_json})
    if r.status_code == 404:
        raise TaskNotFoundError(task_json_dct['id'])


@connection_error_handle
def delete(tid):
    r = requests.delete(task_url_id(tid))
    if r.status_code == 404:
        raise TaskNotFoundError(tid)

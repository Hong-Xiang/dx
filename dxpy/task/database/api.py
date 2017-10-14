from functools import wraps
import json
import requests
import rx
from dxpy.utils import urlf
from ..exceptions import TaskNotFoundError, TaskDatabaseConnectionError
from .service import Service as service
from .. import provider


def task_full_url(tid):
    c = provider.get_or_create_service('config').get_config('database')
    return urlf(c.ip, c.port, "{base}/{tid}".format(base=c.task_url, tid=tid))


def tasks_full_url():
    c = provider.get_or_create_service('config').get_config('database')
    return urlf(c.ip, c.port, c.tasks_url)


def connection_error_handle(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.ConnectionError as e:
            raise TaskDatabaseConnectionError(
                "Task database server connection failed. Details:\n{e}".format(e=e))
    return wrapper


@connection_error_handle
def create_web(task_json):
    r = requests.post(tasks_full_url(), {'task': task_json})
    return r.json()['id']


@connection_error_handle
def read_web(tid):
    r = requests.get(task_full_url(tid))
    if r.status_code == 200:
        return r.text
    else:
        raise TaskNotFoundError(tid)


@connection_error_handle
def read_all_web():
    return rx.Observable.from_(json.loads(requests.get(tasks_full_url()).text))


@connection_error_handle
def update_web(task_json):
    task_json_dct = json.loads(task_json)
    r = requests.put(task_full_url(
        task_json_dct['id']), data={'task': task_json})
    if r.status_code == 404:
        raise TaskNotFoundError(task_json_dct['id'])


@connection_error_handle
def delete_web(tid):
    r = requests.delete(task_full_url(tid))
    if r.status_code == 404:
        raise TaskNotFoundError(tid)


def create(s):
    c = provider.get_or_create_service('config').get_config('database')
    if c.use_web_api:
        return create_web(s)
    else:
        return service.create(s)


def read(tid):
    c = provider.get_or_create_service('config').get_config('database')
    if c.use_web_api:
        return read_web(tid)
    else:
        return service.read(tid)


def read_all():
    c = provider.get_or_create_service('config').get_config('database')
    if c.use_web_api:
        return read_all_web()
    else:
        return service.read_all()


def update(s):
    c = provider.get_or_create_service('config').get_config('database')
    if c.use_web_api:
        return update_web(s)
    else:
        return service.update(s)


def delete(tid):
    c = provider.get_or_create_service('config').get_config('database')
    if c.use_web_api:
        return delete_web(tid)
    else:
        return service.delete(tid)

from functools import wraps
import json
import requests
import rx
from dxpy.utils import urlf
from ..exceptions import TaskNotFoundError, TaskDatabaseConnectionError
from ..representation import TaskPy
from .. import provider

config_service = provider.get_or_create_service('config')


def task_full_url(tid):
    return urlf(config_service.get_config('database').ip, config_service.get_config('database').port, "{base}/{tid}".format(base=config_service.get_config('database').task_url, tid=tid))


def tasks_full_url():
    return urlf(config_service.get_config('database').ip, config_service.get_config('database').port, config_service.get_config('database').tasks_url)


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
def create(task_json):
    r = requests.post(tasks_full_url(), {'task': task_json})
    return r.json()['id']


@connection_error_handle
def read(tid=None):
    r = requests.get(task_full_url(tid))
    if r.status_code == 200:
        return r.text
    else:
        raise TaskNotFoundError(tid)


@connection_error_handle
def read_all():
    return rx.Observable.from_(json.loads(requests.get(tasks_full_url()).text))


@connection_error_handle
def update(task_json):
    task_json_dct = json.loads(task_json)
    r = requests.put(task_full_url(
        task_json_dct['id']), data={'task': task_json})
    if r.status_code == 404:
        raise TaskNotFoundError(task_json_dct['id'])


@connection_error_handle
def delete(tid):
    r = requests.delete(task_full_url(tid))
    if r.status_code == 404:
        raise TaskNotFoundError(tid)

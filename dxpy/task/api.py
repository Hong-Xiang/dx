""" Export APIs for task service. """
import json
from flask import request
from flask_restful import Resource
from dxpy.task.service import create_datebase
from dxpy.task.service import TaskStoreService, TaskRunService
from dxpy.task.templates import create
from dxpy.task.task import TaskCommand, TaskSbatch


class TaskService:
    """ TaskService APIs for python.
    Functions:
    ==========
    #. create_from_template(task_template_cls, args, kwargs):
        Create a task from task template class/type, with given args and kwargs. 
        The task will be written to task database.

    #. get(id):
        Get task object by id.

    #. all(filter_func):
        Get all tasks satisfies filter_function.
    """
    # CREATE
    @classmethod
    def create_from_template(cls, task_template_name, *args, **kwargs):
        return create(task_template_name, *args, **kwargs)

    # READ
    @classmethod
    def get(cls, id_):
        """ Get tasks
        """
        return TaskStoreService.get(id_)

    @classmethod
    def all(cls, filter_func=None):
        return TaskStoreService.all(filter_func)

    # UPDATE
    @classmethod
    def submit(cls, id_):
        return TaskStoreService.submit(id_)

    # DELETE
    @classmethod
    def delete(cls, id_):
        TaskStoreService.delete(id_)


def start_run_service(interval=60000):
    TaskRunService.launch_deamon(interval)


def jsonable(task):

    data = {
        'id': task.id,
        'name': task.name,
        'workdir': task.workdir.abs,
        'pre': task.pre,
        'state': task.state.format()
    }

    def task_command_to_dict(task):
        return {
            'command': task.command
        }

    def task_sbatch_to_dict(task):
        return {
            'sid': task.sid,
            'cmd': task.cmd,
        }

    if isinstance(task, TaskCommand):
        data.update(task_command_to_dict(task))
    elif isinstance(task, TaskSbatch):
        data.update(task_sbatch_to_dict)
    return data


class TaskResource(Resource):
    def get(self, tid):
        return jsonable(TaskService.get(tid))

    def put(self, tid):
        task = request.values['task']
        if task == 'submit':
            TaskService.submit(tid)

    def delete(self, tid):
        TaskService.delete(tid)


class TasksResource(Resource):
    def get(self):
        return (TaskService.all()
                .map(jsonable)
                .to_list()
                .to_blocking()
                .first()), 200

    def post(self):
        kwargs = {k: request.values[k] for k in request.values}
        tid = TaskService.create_from_template(**kwargs)
        return {'tid': tid}, 201


def add_web_api(api, api_root, name='task'):
    api.add_resource(TaskResource, api_root + '{name}/<int:tid>'.format(name))
    api.add_resource(TasksResource, api_root + '{name}s'.format(name))
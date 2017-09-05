import json
from flask import request
from flask_restful import Resource

from dxpy.task.task import TaskCommand, TaskSbatch
from dxpy.task.service import TaskStoreService


def jsonable(task):
    data = {
        'id': task.id,
        'name': task.name,
        'workdir': task.workdir.abs,
        'pre': task.pre
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


class Task(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass


class Tasks(Resource):
    def get(self):
        return (TaskStoreService.all()
                .map(jsonable)
                .to_list()
                .to_blocking()
                .first())

    def post(self):
         request.values['template_name']


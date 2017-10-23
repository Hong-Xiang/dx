
from functools import wraps

from flask import Flask, Response, make_response, request
from flask_restful import Api, Resource, reqparse

from dxpy.web.urls import full

from ..exceptions import TaskNotFoundError
from ..import service


class TaskResource(Resource):
    def get(self, id):
        try:
            return Response(service.read_py(id), 200, mimetype="application/json")
        except TaskNotFoundError as e:
            return str(e), 404

    def put(self, id):
        try:
            task = request.form['task']
            return Response(service.update_py(task), 201, mimetype="application/json")
        except TaskNotFoundError as e:
            return str(e), 404

    def delete(self, id):
        try:
            return Response(service.delete_py(id), 200, mimetype="application/json")
        except TaskNotFoundError as e:
            return str(e), 404


class TasksResource(Resource):
    import json

    def get(self):
        task_jsons = []
        service.read_all_py().subscribe(lambda t: task_jsons.append(t))
        return Response(self.json.dumps(task_jsons), 200, mimetype="application/json")

    def post(self):
        task = request.form['task']
        res = service.create_py(task)
        return Response(self.json.dumps({'id': res}), 201, mimetype="application/json")


def add_api(api, root):
    api.add_resource(TaskResource, task_url_tpl(root))
    api.add_resource(TasksResource, tasks_url(root))


def url():
    pass


def url_format():
    pass


def task_full_url(tid):
    c = provider.get_or_create_service('config').get_config('database')
    return urlf(c.ip, c.port, "{base}/{tid}".format(base=c.task_url, tid=tid))


def tasks_full_url():
    c = provider.get_or_create_service('config').get_config('database')
    return urlf(c.ip, c.port, c.tasks_url)

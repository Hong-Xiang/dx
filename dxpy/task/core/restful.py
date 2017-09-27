import requests
import json
from functools import wraps
from flask import Flask, make_response, request, Response
from flask_restful import Resource, reqparse, Api

from ..representation.task import Task

from . import service

app = Flask(__name__)
api = Api(app)


class TaskResource(Resource):
    def get(self, id):
        try:
            return Response(service.read(id), 200, mimetype="application/json")
        except TaskNotFoundError as e:
            return str(e), 404

    def put(self, id):
        try:
            task = Task.from_json(request.form['task'])
            return Response(service.update(task), 201, mimetype="application/json")
        except TaskNotFoundError as e:
            return str(e), 404

    def delete(self, id):
        try:
            return Response(service.delete(id), 200, mimetype="application/json")
        except TaskNotFoundError as e:
            return str(e), 404


class TasksResource(Resource):
    def get(self):
        return Response(service.read_all(), 200, mimetype="application/json")

    def post(self):
        task = Task.from_json(request.form['task'])
        res = service.create(task)
        return Response(json.dumps({'id': res}), 201, mimetype="application/json")


api.add_resource(TaskResource, c.task_url + '/<int:id>')
api.add_resource(TasksResource, c.tasks_url)


def lauch_database_server():
    from .. import provider
    c = provider.get_or_create_service('config').get_config('database')
    app.run(host=c.ip, port=c.port, debug=c.debug)

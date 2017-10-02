import requests
import json
from functools import wraps
from flask import Flask, make_response, request, Response
from flask_restful import Resource, reqparse, Api

from .. import provider
from .service import Service as sv
from ..exceptions import TaskNotFoundError


class TaskResource(Resource):
    def get(self, id):
        try:
            return Response(sv.read(id), 200, mimetype="application/json")
        except TaskNotFoundError as e:
            return str(e), 404

    def put(self, id):
        try:
            task = request.form['task']
            return Response(sv.update(task), 201, mimetype="application/json")
        except TaskNotFoundError as e:
            return str(e), 404

    def delete(self, id):
        try:
            return Response(sv.delete(id), 200, mimetype="application/json")
        except TaskNotFoundError as e:
            return str(e), 404


class TasksResource(Resource):
    def get(self):
        task_jsons = []
        sv.read_all().subscribe(lambda t: task_jsons.append(t))
        return Response(json.dumps(task_jsons), 200, mimetype="application/json")

    def post(self):
        task = request.form['task']
        res = sv.create(task)
        return Response(json.dumps({'id': res}), 201, mimetype="application/json")


def lauch_database_server():
    c = provider.get_or_create_service('config').get_config('database')
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(TaskResource, c.task_url + '/<int:id>')
    api.add_resource(TasksResource, c.tasks_url)
    app.run(host=c.ip, port=c.port, debug=c.debug)

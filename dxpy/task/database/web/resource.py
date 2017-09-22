import requests
import json
from functools import wraps
from flask import Flask, make_response, request, Response
from flask_restful import Resource, reqparse, Api

from ..config import c
from ..service import Service as sv
from ..service import TaskNotFoundError

app = Flask(__name__)
api = Api(app)


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
        return Response(sv.read_all(), 200, mimetype="application/json")

    def post(self):
        task = request.form['task']
        res = sv.create(task)
        return Response(json.dumps({'id': res}), 201, mimetype="application/json")


api.add_resource(TaskResource, c.task_url + '/<int:id>')
api.add_resource(TasksResource, c.tasks_url)


def lauch_database_server():
    app.run(host=c.host, port=c.port, debug=c.debug)

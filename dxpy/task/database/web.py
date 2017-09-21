import requests
import json
from functools import wraps
from flask import Flask, make_response, request, Response
from flask_restful import Resource, reqparse, Api


from dxpy.utils import urlf

from dxpy.task.database.config import ip, port, task_url, tasks_url
from dxpy.task.database.service import Service as sv
from dxpy.task.database.service import TaskNotFoundError

app = Flask(__name__)
api = Api(app)


class TaskDatabaseConnectionError(Exception):
    pass


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


@app.route('/hello')
def hello():
    return 'hello', 200


api.add_resource(TaskResource, task_url() + '/<int:id>')
api.add_resource(TasksResource, tasks_url())


def lauch_database_server(host='0.0.0.0', debug=True):
    app.run(host=host, port=port(), debug=debug)


def turl(tid):
    return urlf(ip(), port(), "{base}/{tid}".format(base=task_url(), tid=tid))


def tsurl():
    return urlf(ip(), port(), tasks_url())


from functools import wraps


def connection_error_handle(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.ConnectionError as e:
            raise TaskDatabaseConnectionError(
                "Task database server connection failed. Details:\n{e}".format(e=e))
    return wrapper


class Service:
    @staticmethod
    @connection_error_handle
    def create(task_json):
        r = requests.post(tsurl(), {'task': task_json})
        return r.json()['id']

    @staticmethod
    @connection_error_handle
    def read(tid=None):
        r = requests.get(turl(tid))
        if r.status_code == 200:
            return r.text
        else:
            raise TaskNotFoundError(tid)

    @staticmethod
    @connection_error_handle
    def read_all():
        return requests.get(tsurl()).text

    @staticmethod
    @connection_error_handle
    def update(task_json):
        task_json_dct = json.loads(task_json)
        r = requests.put(turl(task_json_dct['id']), data={'task': task_json})
        if r.status_code == 404:
            raise TaskNotFoundError(task_json_dct['id'])

    @staticmethod
    @connection_error_handle
    def delete(tid):
        r = requests.delete(turl(tid))
        if r.status_code == 404:
            raise TaskNotFoundError(tid)

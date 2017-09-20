import requests
from flask import Flask, make_response
from flask_restful import Resource, reqparse, Api


from dxpy.utils import urlf
from dxpy.task.database.config import ip, port, task_url, tasks_url
from dxpy.task.database.service import Service as sv

app = Flask(__name__)
api = Api(app)


class TaskResource(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass


class TasksResource(Resource):
    def get(self):
        return sv.read()

    def post(self, task):
        pass


@app.route('/hello')
def hello():
    return 'hello', 200


api.add_resource(TasksResource, task_url())
api.add_resource(TaskResource, tasks_url())


def lauch_database_server(host='127.0.0.1'):
    app.run(host=host, port=port())


def turl(tid):
    return urlf(ip(), port(), "{base}/{tid}".format(base=task_url(), tid=tid))


def tsurl():
    return urlf(ip(), port(), task_url(), tid=tid)


class Service:
    @staticmethod
    def create(task_json):
        r = requests.post(tsurl, {'task': task_json})
        return int(r.text)

    def read(tid):
        return requests.get(turl(task_json.id)).text

    def update(task_json):
        requests.put(turl(task_json.id), {'task': task_json})

    def delete(tid):
        requests.delete(turl(task_json.id))

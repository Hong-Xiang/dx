import json
from time import strftime, localtime, time, gmtime
from flask import Flask, request, jsonify, url_for, make_response
from flask_restful import Resource, Api
import requests

from dxpy.time.stamp import TimeStamp, as_time_stamp

PROGBAR_ROOT = None

time_stamps = dict()

# Server logic
class Server:
    """
    """
    def __init__(self, config_file=None): 
        self.app = Flask(__name__)
        self.api = Api(self.app)        
        self._config_file = config_file
        self._time_stamp = None
        if config_file is None:
            #Init server
            self._time_stamp = TimeStamp()
        else:
            with open(config_file, 'r') as fin:
                config = json.load(fin)
                ts = config.get('time_stamp')            
                self._time_stamp = json.loads()
            self._nb_tasks = config['nb_tasks']
            self._tasks_in_run = config['tasks_in_run']
        if self._time_stamp is None:
            self._time_stamp = TimeStamp()

    def start(self, host=None, port=5000, debug=True):
        self.app.run(host=host, port=port, debug=debug)
    
    @property
    def time_stamp(self):
        self._time_stamp.update()
        return self._time_stamp

    def times(self):
        msg_time_start = strftime("%a, %d %b %Y %H:%M:%S", localtime(self._time_start))
        time_up = time() - self._time_start
        msg_time_up = strftime("%H hurs, %M mins, %S secs", gmtime(time_up))
        msg_times = {
            'start': msg_time_start,
            'up': msg_time_up
        }
        return msg_times

    def update_config(self):
        config_new = {
            'nb_tasks': self
        }

server = Server()

@server.app.route('/greetings', methods=['GET'])
def greetings():
    return jsonify({"msg": "Greetings from Task Server"})

@server.app.route('/test404', methods=['GET'])
def test404():
    return make_response(jsonify({"msg": "Resource not exist"}), 404)

class Times(Resource):
    def get(self):
        return server.time_stamp.readable()

server.api.add_resource(Times, '/times')
    




# @server.route("/tasks/<int:task_id>", methods=['POST'])
# def create_task(task_id):
#     request.form()

if __name__ == "__main__":
    server.start()


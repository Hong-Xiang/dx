from flask import Flask
from flask_restful import Api
from dxpy.task.api import add_web_api

app = Flask(__name__)
api = Api(app)

api_root = '/api/'
add_web_api(api, api_root)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

import click


@click.command()
def start():
    from dxpy.web.urls import api_format
    from flask import Flask
    from .web import add_api
    from ...config import config as c
    """ start task database web service """
    web.launch_database_server()
    app = Flask(__name__)
    api = Api(app)
    add_api(api_format('/', ))
    app.run(host=c['host'], port=c['port'], debug=c['debug'])

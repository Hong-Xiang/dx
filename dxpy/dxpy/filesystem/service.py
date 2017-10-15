from .directory.model import Directory
from .file.model import File
from .directory import service as ds
from .file import service as fs


def mv(sor, tar, overwrite=True):
    if isinstance(sor, Directory):
        ds.mv(sor, tar, overwrite)
    else:
        fs.mv(sor, tar, overwrite)


def cp(sor, tar, overwrite=True):
    if isinstance(sor, Directory):
        ds.cp(sor, tar, overwrite)
    else:
        fs.cp(sor, tar, overwrite)


def rm(sor):
    if isinstance(sor, Directory):
        ds.rm(sor)
    else:
        fs.rm(sor)


def launch_web_ui(host, port, version=0.1, debug=True):
    from flask import Flask, url_for
    from flask_cors import CORS, cross_origin
    from flask_restful import Api
    from .web import add_apis
    app = Flask(__name__)
    CORS(app)
    api = Api(app)
    add_apis(api, '/api/v{0}'.format(version))

    @app.route("/site-map")
    def site_map():
        import json
        links = []
        for rule in app.url_map.iter_rules():
            if rule.endpoint =='static':
                continue
            links.append((url_for(rule.endpoint, path='%252Ftmp%252Ftest'), rule.endpoint))
        return json.dumps(links, indent=4, separators=(',', ':'))
    app.run(host, port, debug=debug)

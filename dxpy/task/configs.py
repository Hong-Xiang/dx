import yaml
from functools import wraps
from .exceptions import UnknownConfigName


class DatabaseConfigs:
    def __init__(self, file=None, root=None, ip=None, port=None, version=None, name=None, use_web_api=False):
        self.file = file or '/home/hongxwing/Workspace/databases/tasksv2.db'
        self.root = root or 'sqlite:///'
        self.ip = ip or '127.0.0.1'
        self.port = port or 23301
        self.version = version or 0.1
        self.name = name or 'task'
        self.use_web_api = use_web_api

    @property
    def path(self):
        return self.root + self.file

    @property
    def task_url(self):
        return '/api/v{version}/{name}'.format(
            version=self.version, name=self.name)

    @property
    def tasks_url(self):
        return '/api/v{version}/{name}s'.format(
            version=self.version, name=self.name)


CONFIGS = {
    'database': None,
}

CONFIGS_CLS = {
    'database': DatabaseConfigs,
}


def name_check(func):
    @wraps(func)
    def wrapper(name, *args, **kwargs):
        if name not in CONFIGS:
            raise UnknownConfigName(name)
        return func(*args, **kwargs)
    return wrapper


@name_check
def get_config_cls(name):
    return CONFIGS_CLS[name]


@name_check
def get_config(name):
    if CONFIGS[name] is None:
        CONFIGS[name] = get_config_cls(name)()
    return CONFIGS[name]


@name_check
def set_config(name, yml_file=None, config=None):
    if yml_file is not None:
        CONFIGS[name] = yaml.load(yml_file)
    elif config is not None:
        CONFIGS[name] = config


@name_check
def set_config_by_name_key(name, key, value):
    c = get_config(name)
    c.key = value


@name_check
def clear_config(name):
    CONFIGS[name] = None

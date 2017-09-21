PATH_DATEBASE_FILE = '/home/hongxwing/Workspace/databases/tasksv2.db'
PATH_DATABASE_ROOT = 'sqlite:///'

TASK_DATABASE_IP = '127.0.0.1'
TASK_DATABASE_PORT = 23301
WEB_API_VERSION = 0.1
TASK_URL_NAME = 'task'


def path_database():
    return PATH_DATABASE_ROOT + PATH_DATEBASE_FILE


def ip():
    return TASK_DATABASE_IP


def port():
    return TASK_DATABASE_PORT


def task_url():
    return '/api/v{version}/{name}'.format(
        version=WEB_API_VERSION, name=TASK_URL_NAME)


def tasks_url():
    return '/api/v{version}/{name}s'.format(
        version=WEB_API_VERSION, name=TASK_URL_NAME)

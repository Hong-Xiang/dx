class Configs:
    def __init__(self):
        self.file = '/home/hongxwing/Workspace/databases/tasksv2.db'
        self.root = 'sqlite:///'
        self.ip = '127.0.0.1'
        self.port = 23301
        self.version = 0.1
        self.name = 'task'
        self.debug = False

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


def get_config(config_yml=None):
    if config_yml is None:
        return Configs()


c = get_config()

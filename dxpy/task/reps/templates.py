from dxpy.task.reps.taskpy import Task


class UnknownTemplateNameError(Exception):
    def __init__(self, ukn_name, supp_name):
        super(__class__, self).__init__("Unknown task template name {name}, suppoted names are {supp}.".format(
            name=ukn_name, supp=[k for k in supp_name]))


class TaskCommand(Task):
    def __init__(self, *args, **kwargs, command):
        super(__class__, self).__init__(*args, **kwargs)
        self.command = command

    def run(self):
        return os.popen(self.command)


class TaskPyFunc(Task):
    def __init__(self, *args, **kwargs, func, func_args, func_kwargs):
        super(__class__, self).__init__(*args, **kwarg)
        self.func = func
        self.func_args = func_args
        self.func_kwargs = func_kwargs

    def run(self):
        return self.func(*self.func_args, **self.func_kwargs)


TEMPLATE_NAME_MAP = {
    'TASK': Task,
    'COMMAND': TaskCommand,
    'PYFUNC': TaskPyFunc
}


def get_task_tpl(tpl_name):
    tpl_name = tpl_name.upper()
    task_tpl = TEMPLATE_NAME_MAP.get(tpl_name)
    if task_tpl is None:
        raise UnknownTemplateNameError(task_tpl_name, TEMPLATE_NAME_MAP.keys())
    return task_tpl


def create(task_tpl_name, *args, **kwargs):
    return get_task_tpl(task_tpl_name)(*args, **kwargs)

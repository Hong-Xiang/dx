"""
Task templates of frequently used ones.
"""
import rx
from dxpy.file_system.path import Path
from dxpy.task.reps.taskpy import TaskPy


class TaskCommand(TaskPy):
    def __init__(self, command, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.command = command

    def run(self):
        cmd = "cd {dir} && {cmd}".format(
            dir=self.workdir.abs, cmd=self.command)
        return os.popen(cmd)


class TaskScript(TaskPy):
    def __init__(self, file,  *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.file = Path(file)

    def run(self, interp=''):
        cmd = "cd {dir} && {interp} {file}".format(
            interp=interp, file=self.file.abs)
        return os.popen(cmd)


class TaskPyFunc(TaskPy):
    def __init__(self, func, func_args, func_kwargs, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwarg)
        self.func = func
        self.func_args = func_args
        self.func_kwargs = func_kwargs

    def run(self):
        return self.func(*self.func_args, **self.func_kwargs)


TEMPLATE_NAME_MAP = {
    'TASK': TaskPy,
    'COMMAND': TaskCommand,
    'PYFUNC': TaskPyFunc
}


class UnknownTemplateNameError(Exception):
    def __init__(self, ukn_name):
        super(__class__, self).__init__("Unknown task template name {name}, suppoted names are {supp}.".format(
            name=ukn_name, supp=[k for k in TEMPLATE_NAME_MAP.keys()]))


def create_by_cls(template_class, *args, **kwargs):
    return template_class(*args, **kwargs)


def create_by_name(template_name, *args, **kwargs):
    def template_class(name):
        name = name.upper()
        template_class = TEMPLATE_NAME_MAP.get(name)
        if template_class is None:
            raise UnknownTemplateNameError(name)
        return template_class

    return create_by_cls(template_class(template_name), *args, **kwargs)


def create(template_class_or_name, *args, **kwargs):
    if issubclass(template_class_or_name, TaskPy):
        return create_by_cls(template_class_or_name, *args, **kwargs)
    else:
        return create_by_name(template_class_or_name, *args, **kwargs)

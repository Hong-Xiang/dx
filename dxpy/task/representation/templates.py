"""
Task templates of frequently used ones.
"""
import rx
import os
from dxpy.file_system.path import Path
from .taskpy import TaskPy
from ..exceptions import UnknownTemplateNameError


class TaskCommand(TaskPy):
    def __init__(self, command, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.command = command

    def plan(self, command_func=None):
        if command_func is None:
            command = 'cd {0} && {1}'.format(self.workdir.abs, self.command)
        else:
            command = command_func(workdir=self.workdir, command=self.command)

        return command


class TaskScript(TaskPy):
    def __init__(self, file,  *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.file = Path(file)

    def plan(self, command_func=None):
        if command_func is None:
            command = 'cd {0} && {1}'.format(self.workdir.abs, self.file.abs)
        else:
            command = command_func(workdir=self.workdir, file=self.file)

        return command


class TaskPyFunc(TaskPy):
    def __init__(self, func, func_args, func_kwargs, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwarg)
        self.func = func
        self.func_args = func_args
        self.func_kwargs = func_kwargs

    def plan(self, i_worker=None, *args, **kwargs):
        # TODO: change to observable
        raise NotImplementedError
        if i_worker is None:
            return self.func(*self.func_args, **self.func_kwargs)
        else:
            return self.func(*self.func_args, **self.func_kwargs, i_worker=i_worker)


TEMPLATE_NAME_MAP = {
    'TASK': TaskPy,
    'SCRIPT': TaskScript,
    'COMMAND': TaskCommand,
    'PYFUNC': TaskPyFunc
}


def template_class(name):
    name = name.upper()
    template_class = TEMPLATE_NAME_MAP.get(name)
    if template_class is None:
        raise UnknownTemplateNameError(name)
    return template_class

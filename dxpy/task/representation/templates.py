"""
Task templates of frequently used ones.
"""
import rx
from dxpy.file_system.path import Path
from .taskpy import TaskPy
from ..exceptions import UnknownTemplateNameError


class TaskCommand(TaskPy):
    def __init__(self, command, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.command = command

    def plan(self, i_worker=None, pre_cmd=None, post_cmd=None):
        def add_pre(x):
            if pre_cmd is not None:
                return '{pre} && {cmd}'.format(pre=pre_cmd, cmd=x)
            else:
                return x

        def add_chdir(x):
            return 'cd {dir} && {cmd}'.format(dir=self.workdir.abs, cmd=x)

        def add_post(x):
            if pre_cmd is not None:
                return '{cmd} && {post}'.format(post=post_cmd, cmd=x)
            else:
                return x

        def sub_i_worker(x):
            if i_worker is None:
                return x
            else:
                return x.format(i_worker=i_worker)

        return (rx.Observable.just(self.command)
                .map(sub_i_worker)
                .map(add_pre)
                .map(add_chdir)
                .map(add_post)
                .map(os.popen))


class TaskScript(TaskPy):
    def __init__(self, file,  *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.file = Path(file).abs

    def plan(self, i_worker=None, interp=None):
        def add_chdir(x):
            return 'cd {dir} && {cmd}'.format(dir=self.workdir.abs, cmd=x)

        def add_interp(x):
            if interp is not None:
                return '{interp} {file}'.format(interp=interp, file=x)
            else:
                return x

        def sub_i_worker(x):
            if i_worker is None:
                return x
            else:
                return x.format(i_worker=i_worker)

        return (rx.Observable.just(self.file)
                .map(sub_i_worker)
                .map(add_interp)
                .map(add_chdir)
                .map(os.popen))


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

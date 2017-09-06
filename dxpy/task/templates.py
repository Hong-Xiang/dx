import re
from dxpy.task.service import TaskStoreService
from dxpy.task.task import TaskCommand, TaskSbatch


class UnknownTemplateNameError(Exception):
    pass


class TaskTemplates:
    @staticmethod
    def sleep(path, name, *args, **kwargs):
        command = 'echo TaskSleep.{name}.start && sleep 1 && echo TaskSleep.{name}.end'
        tid = TaskStoreService.create(TaskCommand, path, name, command=command)
        return tid

    @staticmethod
    def sleep_chain(path, name, *args, **kwargs):
        nb_chain = 3
        tsks = []
        for i in range(nb_chain):
            tname = 'TaskSleep.{name}.{idx}'.format(name=name, idx=i)
            command = 'echo {tn}.start && sleep 1 && echo {tn}.end'.format(
                tn=tname)
            tid = TaskStoreService.create(
                TaskCommand, path, name, command=command)
            if len(tsks) > 0:
                TaskStoreService.get(tid).wait(TaskStoreService.get(tsks[-1]))
            tsks.append(tid)
        return tid

    @staticmethod
    def sbatch(path, name, sfile, *args, **kwargs):
        return TaskStoreService.create(TaskSbatch, path, name, sfile=sfile)


def create(tpl_name, *args, **kwargs):
    print('DEEEEEBUG')
    print(args)
    print(kwargs)
    if not hasattr(TaskTemplates, tpl_name):
        raise UnknownTemplateNameError(tpl_name)
    return getattr(TaskTemplates, tpl_name)(*args, **kwargs)

from dxpy.task.service import TaskStoreService
from dxpy.task.task import TaskCommand, TaskSbatch


class TaskTemplates:
    @staticmethod
    def sleep(path, name):
        command = 'echo TaskSleep.{name}.start && sleep 1 && echo TaskSleep.{name}.end'
        tid = TaskStoreService.create(TaskCommand, path, name, command=command)
        return tid

    @staticmethod
    def sleep_chain(path, name):
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
    def sbatch(path, name, sfile):
        return TaskStoreService.create(TaskSbatch, path, name, sfile=sfile)

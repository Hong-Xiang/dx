""" Tasks example """

from dxpy.task.task import Task, TaskCommand
from dxpy.task.service import TaskStoreService

class TaskSleep(TaskCommand):
    COMMAND = 'echo TaskSleep.{name}.start && sleep 1 && echo TaskSleep.{name}.end'

    def __init__(self, *args, **kwargs):
        super(TaskSleep, self).__init__(
            *args, **kwargs)
        self.command = TaskSleep.COMMAND.format(name=self.name)


# class TaskSleepChain(Task):
#     def __init__(self, *args, **kwargs):
#         super(TaskSleepChain, self).__init__(*args, **kwargs)
#         ts = []
#         for i in range(3):
#             path = task_service.get_path(self.id)
#             ts.append(task_service.create(TaskSleep, path, 'chain sleep {:d}'.format(i)))            
#         for tid in ts:
#             self.wait(task_service.get(tid))

#     def run(self):
#         return None

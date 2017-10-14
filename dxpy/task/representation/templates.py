from .task import Task

class TaskCommand(Task):
    def __init__(self, command, *args, **kwargs):
        super(__class__,self).__init__(*args, **kwargs):
            self.command = command

    def plan(self):
        pass
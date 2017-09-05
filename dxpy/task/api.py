""" Export APIs for task service. """
from dxpy.task.service import create_datebase
from dxpy.task.service import TaskStoreService
from dxpy.task.templates import TaskTemplates


class TaskSerivce:
    """ TaskService APIs for python.
    Functions:
    ==========
    #. create_from_template(task_template_cls, args, kwargs):
        Create a task from task template class/type, with given args and kwargs. 
        The task will be written to task database.

    #. get(id):
        Get task object by id.

    #. all(filter_func):
        Get all tasks satisfies filter_function.
    """
    @classmethod
    def create_from_template(cls, task_template_name, *args, **kwargs):
        return getattr(TaskTemplates, task_template_name)(*args, **kwargs)

    @classmethod
    def get(cls, id_):
        """ Get tasks
        """
        return TaskStoreService.get(id_)

    @classmethod
    def submit(cls, id_):
        return TaskStoreService.submit(id_)

    @classmethod
    def delete(cls, id_):
        TaskStoreService.delete(id_)

    @classmethod
    def all(cls, filter_func=None):
        return TaskStoreService.all(filter_func)






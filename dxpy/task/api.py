""" TaskService (exported) API.
Functions:
==========
#. create(task_template_cls, args, kwargs):
    Create a task from task template class/type, with given args and kwargs. 
    The task will be written to task database.

#. get(id):
    Get ???serilized or not??? task object by id.

#. get_all(filter_function):

"""

class TaskSerivce:
    @classmethod
    def create(cls, task_template_cls, args, kwargs):
        pass

    @classmethod
    def get(cls, id):
        """ Get tasks
        """
        pass

    @classmethod
    def get_all(cls, filter_function):
        pass

class TaskServiceResource:
    pass



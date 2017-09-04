import logging
import yaml
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dxpy.file_system.path import Path
from dxpy.task.task import Task
logger = logging.getLogger(__name__)

PATH_DATEBASE = 'sqlite:////home/hongxwing/Workspace/databases/tasks.db'

Base = declarative_base()
engine = create_engine(PATH_DATEBASE)
DBSession = sessionmaker(bind=engine)


class TaskDBModel(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    path = Column(String)
    active = Column(Boolean)

    def __repr__(self):
        return "<TaskDBModel: id: {0}, name: {1}, path:{2}>".format(self.id, self.name, self.path)


def create_datebase(is_overwrite=False):
    """ Helper function to create new engine """
    from pathlib import Path
    db_file = Path(PATH_DATEBASE)
    if not db_file.exists or is_overwrite:
        Base.metadata.create_all(engine)


class TaskDBService:

    def __init__(self):
        self.session = DBSession()

    def add(self, name=None, path=None, active=True):
        new_task = TaskDBModel(name=name, path=Path(path).abs, active=active)
        self.session.add(new_task)
        self.session.commit()
        return new_task.id

    def get(self, id):
        return self.session.query(TaskDBModel).get(id)

    def all(self):
        return self.session.query(TaskDBModel).all()


class TaskFileService:
    """
    Manipulation of task *representation* objects.

    Functions:
    ----------

    new(task_type, *args, **kwargs):

    """

    def add(self, path, task):
        with open(path, 'w') as fout:
            yaml.dump(task, fout)

    # def append(self, path, task):
    #     try:
    #         tasks = self.get(path)
    #     except FileNotFoundError:
    #         tasks = []
    #     tasks = [task] + tasks
    #     with open(path, 'w') as fout:
    #         yaml.dump(tasks, fout)

    def get(self, path):
        """
        Return:
            tasks: list of Task objects.
        """
        try:
            with open(path, 'r') as fin:
                tasks = yaml.load(fin)
        except FileNotFoundError:
            return []
        except Exception as e:
            logger.error(e.msg, e.args, exc_info=1)
        if tasks is None:
            return []
        if not isinstance(tasks, (list, tuple)):
            return [tasks]
        return tasks

    def append(self, path, task):
        tasks = self.get(path)
        found = False
        for i, t in enumerate(tasks):
            if t.id == task.id:
                tasks[i] = task
                found = True
                break
        if not found:
            tasks.append(task)
        with open(path, 'w') as fout:
            yaml.dump(tasks, fout)

    # @classmethod
    # def get(cls, id=None):
    #     """ Get task path from database """
    #     return TaskService.TASKS[id]

    # @classmethod
    # def get_all(cls, filter_func=None):
    #     if filter_func is None:
    #         return TaskService.TASKS
    #     else:
    #         return [t for t in TaskService.TASKS if filter_func(t)]

    # @classmethod
    # def put(cls, id, task):
    #     while len(TaskService.TASKS) < id + 1:
    #         TaskService.TASKS.append(None)
    #     TaskService.TASKS[id] = task

    # # TODO: delete?
    # @classmethod
    # def update_state(cls, id,  new_state):
    #     task = TaskService.get(id)
    #     if isinstance(new_state, str):
    #         new_state = TaskState.parse(new_state)
    #     task.state = new_state
    #     task.push()
    #     return TaskService.get(id)

    # # TODO: delete?
    # @classmethod
    # def add_wait(cls, id_post, id_pre):
    #     task_post = TaskService.get(id_post)
    #     task_pre = TaskService.get(id_pre)
    #     task_post.wait(task_pre)
    #     task_post.push()
    #     return TaskService.get(id_post)

    # @classmethod
    # def delete(cls, id):
    #     TaskService.TASKS.pop(id)


class TaskService:
    from dxpy.task.service import TaskDBService, task_file_service

    def create(self, task_cls, path, name, *args, **kwargs):
        """
        Returns:
            tid: int, task id.
        """
        tid = TaskService.TaskDBService().add(name, path)
        if isinstance(task_cls, str):
            task_cls = get_task_cls(task_cls)
        task = task_cls(tid, name, *args, **kwargs)
        TaskService.task_file_service.append(path, task)
        return tid

    def get(self, id):
        """
        Returns:
            task: Task.
        Raises:
            FileNotFoundError:
        """
        return get_task(id)

    def get_path(self, id):
        """
        Returns:
            path: str, path of .yaml file saving task.
        """
        return TaskService.TaskDBService().get(id).path

    def submit(self, id):
        task = self.get(id)
        task.submit()

    def delete(self, id):
        pass

    def run_cycle(self):
        task_run_service.run()

    def submit_cycle(self):
        task_run_service.submit()

    def print_all(self):
        for t in [get_task(t.id) for t in TaskDBService().all()]:
            print(t)


task_service = TaskService()


task_file_service = TaskFileService()


def get_task(id):
    tasks = TaskService.task_file_service.get(TaskDBService().get(id).path)
    for t in tasks:
        if t.id == id:
            return t
    return None


# Modify this function to add tasks.
def get_task_cls(task_type_name):
    """

    """
    from dxpy.task.task import Task
    from dxpy.task.task_ex import TaskSleep, TaskSleepChain
    mapping = {
        'Task': Task,
        'TaskSleep': TaskSleep,
        'TaskSleepChain': TaskSleepChain
    }
    return mapping[task_type_name]


class TaskRunService:
    """ run commands of tasks
    """

    def all(self):
        tasks = [get_task(t.id) for t in TaskDBService().all()]
        return [t for t in tasks if t is not None]

    def submit(self):
        for t in self.all():
            if t.state.run == t.state.RunState.Pending:
                if not t.is_to_run:
                    for tp in t.tasks_to_run():
                        if tp.state.run == tp.state.RunState.WaitingToSubmit:
                            tp.submit()

    def run(self):
        logger.debug('TaskRunService.run called.')
        for t in self.all():
            print(t)
            if t.is_to_run:
                t.run()

    def mark_as_finish(self, id_or_task):
        if isinstance(id_or_task, int):
            task = self.get(id_or_task)
        else:
            task = id_or_task
        task.finish()


task_run_service = TaskRunService()

import logging
import yaml
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from rx import Observable
from dxpy.file_system.path import Path
import filelock

logger = logging.getLogger(__name__)

PATH_DATEBASE_FILE = '/home/hongxwing/Workspace/databases/tasks.db'
PATH_DATABASE_ROOT = 'sqlite:///'
PATH_DATEBASE = PATH_DATABASE_ROOT + PATH_DATEBASE_FILE


Base = declarative_base()
engine = create_engine(PATH_DATEBASE)
DBSession = scoped_session(sessionmaker(bind=engine))


class _TaskDBModel(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    path = Column(String)
    active = Column(Boolean)

    def __repr__(self):
        return "<_TaskDBModel: id: {0}, name: {1}, path:{2}>".format(self.id, self.name, self.path)


def create_datebase(is_overwrite=False):
    """ Helper function to create new engine """
    from pathlib import Path
    db_file = Path(PATH_DATEBASE_FILE)
    if is_overwrite and db_file.exists:
        db_file.unlink()
    Base.metadata.create_all(engine)


class _DatabaseService:

    def __init__(self):
        self.session = DBSession()

    def add(self, path=None, name=None, active=True):
        new_task = _TaskDBModel(name=name, path=Path(path).abs, active=active)
        self.session.add(new_task)
        self.session.commit()
        return new_task.id

    def get(self, id_):
        return self.session.query(_TaskDBModel).get(id_)

    def all(self):
        """ 
        () -> Observable<_TaskDBModel[]>
        """
        return Observable.from_(self.session.query(_TaskDBModel).all())

    def delete(self, id_):
        self.session.delete(self.session.query(_TaskDBModel).get(id_))
        self.session.commit()


class _FileService:
    """
    """

    @classmethod
    def overwrite(cls, path, tasks, is_lock=True):
        if is_lock:
            lock = filelock.FileLock(path + '.lock')
            with lock:
                with open(path, 'w') as fout:
                    yaml.dump(tasks, fout)
        else:
            with open(path, 'w') as fout:
                yaml.dump(tasks, fout)

    @classmethod
    def get(self, path, is_lock=True):
        """
        Return:
            tasks: list of Task objects.
        """
        if path is None:
            return []
        try:
            if is_lock:
                lock = filelock.FileLock(path + '.lock')
                with lock:
                    with open(path, 'r') as fin:
                        tasks = yaml.load(fin)
            else:
                with open(path, 'r') as fin:
                    tasks = yaml.load(fin)
        except FileNotFoundError:
            return []
        # except Exception as e:
        #     logger.error(e.msg, e.args, exc_info=1)

        if tasks is None:
            return []
        if not isinstance(tasks, (list, tuple)):
            return [tasks]
        return tasks

    @classmethod
    def append(cls, path, task):
        lock = filelock.FileLock(path + '.lock')
        with lock:
            tasks = _FileService.get(path, is_lock=False)
            found = False
            for i, t in enumerate(tasks):
                if t.id == task.id:

                    tasks[i] = task
                    found = True
                    break
            if not found:
                tasks.append(task)
            _FileService.overwrite(path, tasks, is_lock=False)

    @classmethod
    def delete(cls, path, task):
        lock = filelock.FileLock(path + '.lock')
        with lock:
            tasks = _FileService.get(path, is_lock=False)
            for i, t in enumerate(tasks):
                if t.id == task.id:
                    tasks.pop(i)
            _FileService.overwrite(path, tasks, is_lock=False)
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


class TaskStoreService:
    """ Task
    """
    @classmethod
    def create(cls, task_cls, path, name, *args, **kwargs):
        """ Create a single task
        Returns:
            tid: int, task id.
        """
        tid = _DatabaseService().add(path, name)
        # if isinstance(task_cls, str):
        #     task_cls = get_task_cls(task_cls)
        task = task_cls(tid, name, *args, **kwargs)
        _FileService.append(path, task)
        return tid

    @classmethod
    def get_path(cls, id_):
        """
        Returns:
            path: str, path of .yaml file saving task.
        """
        tdb = _DatabaseService().get(id_)
        if tdb:
            return tdb.path
        else:
            return None

    @classmethod
    def get(cls, id_):
        """
        Returns:
            task: Task.
        Raises:
            FileNotFoundError:            
        """
        for t in _FileService.get(TaskStoreService.get_path(id_)):
            if t.id == id_:
                return t
        return None

    @classmethod
    def all(cls, filter_func=None):
        """
        (filter_func) -> Observable<Task[]>
        """
        if filter_func is None:
            def filter_func(x): return x is not None
        return (_DatabaseService().all()
                .map(lambda tdb: TaskStoreService.get(tdb.id))
                .filter(filter_func))

    @classmethod
    def update(cls, task):
        _FileService.append(TaskStoreService.get_path(task.id),
                            task)

    @classmethod
    def submit(self, id_):
        tsk = TaskStoreService.get(id_)
        tsk.submit()
        _FileService.append(TaskStoreService.get_path(id_),
                            tsk)

    @classmethod
    def delete(self, id_):
        tsk = TaskStoreService.get(id_)
        _FileService.delete(TaskStoreService.get_path(id_),
                            TaskStoreService.get(id_))
        _DatabaseService().delete(tsk.id)

# Modify this function to add tasks.


# def get_task_cls(task_type_name):
#     """

#     """
#     from dxpy.task.task import Task
#     from dxpy.task.task_ex import TaskSleep, TaskSleepChain
#     mapping = {
#         'Task': Task,
#         'TaskSleep': TaskSleep,
#         'TaskSleepChain': TaskSleepChain
#     }
#     return mapping[task_type_name]


class TaskRunService:
    """ run commands of tasks
    """
    @classmethod
    def check_complete(cls):
        from dxpy.task.task import TaskSbatch
        (
            TaskStoreService.all()
            .filter(lambda t: t.state.run == t.state.RunState.Runing)
            .filter(lambda t: isinstance(t, TaskSbatch))
            .subscribe(lambda t: t.check_complete())
        )

    @classmethod
    def submit(cls):
        (
            TaskStoreService.all()
            .filter(lambda t: t.state.run == t.state.RunState.Pending)
            .filter(lambda t: not t.is_to_run)
            .flat_map(lambda t: t.dependence())
            .filter(lambda t: t.state.is_waiting_to_submit)
            .subscribe(lambda t: t.submit())
        )

    @classmethod
    def run(cls):
        (
            TaskStoreService.all()
            .filter(lambda t: t.is_to_run)
            .subscribe(lambda t: t.run())
        )

    @classmethod
    def cycle(cls):
        TaskRunService.check_complete()
        TaskRunService.submit()
        TaskRunService.run()

    @classmethod
    def launch_deamon(cls, interval=10000):
        Observable.interval(interval).start_with(0).subscribe(
            on_next=lambda t: TaskRunService.cycle(), on_error=lambda e: print(e))

    @classmethod
    def mark_as_finish(self, id_or_task):
        if isinstance(id_or_task, int):
            task = self.get(id_or_task)
        else:
            task = id_or_task
        task.finish()

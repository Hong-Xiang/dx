import json
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from dxpy.file_system.path import Path
from dxpy.time.utils import now
from dxpy.task.misc import TaskState
from dxpy.task.database.config import path_database


Base = declarative_base()
engine = create_engine(path_database())
DBSession = sessionmaker(bind=engine)


class TaskDB(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    desc = Column(String)
    body = Column(String)
    dependency = Column(String)
    time_create = Column(DateTime)
    state = Column(String)

    def __init__(self, desc, body, state=None, time_create=None, depens=None):
        """
            workdir: path
        """
        self.desc = desc
        self.body = body
        if time_create is None:
            time_create = now()
        self.time_create = time_create
        if state is None:
            state = TaskState.BeforeSubmit.name
        self.state = state
        if depens is None:
            depens = ''
        self.dependency = depens

    def __repr__(self):
        return '<Task {:d}>'.format(self.id)


def create_datebase(is_overwrite=False):
    """ Helper function to create new engine """
    # from pathlib import Path
    # db_file = Path(path_database())
    # if is_overwrite and db_file.exists:
    #     db_file.unlink()
    Base.metadata.create_all(engine)


# def db2yaml(task):
#     return task.body


# def db2py(task):
#     return yaml.load(db2yaml(task))

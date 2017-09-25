import json
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

from dxpy.file_system.path import Path
from dxpy.time.utils import now
from dxpy.task.misc import TaskState

Base = declarative_base()


def engine(path=None):
    from ..import provider
    config_service = provider.get_or_create_service('config')
    if path is not None:
        c = config_service.get_config('database')
    else:
        c = config_service.get_config_cls('database')()
        c.file = path
    return create_engine(c.path)


def session_maker(path=None):
    return sessionmaker(bind=engine(path))


class TaskDB(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    desc = Column(String)
    body = Column(String)
    dependency = Column(String)
    time_create = Column(DateTime)
    state = Column(String)
    is_root = Column(Boolean)

    def __init__(self, desc, body, state=None, time_create=None, depens=None, is_root=True):
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
        self.is_root = is_root

    def __repr__(self):
        return '<Task {:d}>'.format(self.id)


def create_datebase(path=None):
    Base.metadata.create_all(engine(path))


def drop_database(path=None):
    TaskDB.__table__.drop(engine(path))

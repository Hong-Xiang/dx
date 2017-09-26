import json
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

from dxpy.file_system.path import Path
from dxpy.time.utils import now
from dxpy.task.misc import TaskState

Base = declarative_base()


class Database:
    engine = None

    @classmethod
    def create_engine(cls):
        from ..import provider
        c = provider.get_or_create_service('config').get_config('database')
        cls.engine = create_engine(c.path, echo=c.echo)

    @classmethod
    def get_or_create_engine(cls):
        if cls.engine is None:
            cls.create_engine()
        return cls.engine

    @classmethod
    def session_maker(cls):
        return sessionmaker(bind=cls.get_or_create_engine())

    @classmethod
    def create(cls):
        Base.metadata.create_all(cls.get_or_create_engine())

    @classmethod
    def drop(cls):
        # TaskDB.__table__.drop(cls.get_or_create_engine())
        # cls.engine = None
        sess = cls.session_maker()()
        records = sess.query(TaskDB).delete()
        sess.commit()
        # cls.create()

    @classmethod
    def clear(cls):
        cls.engine = None

    @classmethod
    def session(cls):
        return cls.session_maker()()


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

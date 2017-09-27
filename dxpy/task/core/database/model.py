import json
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from dxpy.time.timestamps import TaskStamp
from ...representation.task import Task


Base = declarative_base()


class TaskDB(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    desc = Column(String)
    workdir = Column(String)
    worker = Column(String)
    time_create = Column(DateTime)
    time_start = Column(DateTime)
    time_end = Column(DateTime)
    dependency = Column(String)
    ttype = Column(String)
    state = Column(String)
    is_root = Column(Boolean)
    data = Column(String)

    def __init__(self, tid, desc, workdir, worker, ttype, state, time_stamp, dependency, is_root, data):
        self.id = tid
        self.desc = desc
        self.workdir = workdir
        self.worker = worker
        self.ttype = ttype
        self.state = state
        self.time_create = time_stamp.create
        self.time_start = time_stamp.start
        self.time_end = time_stamp.end
        self.state = state
        self.dependency = depens
        self.is_root = is_root

    def __repr__(self):
        return '<Task {:d}>'.format(self.id)

    @classmethod
    def create_from_json(cls, s):
        t = Task.from_json(s)
        ts = Task.serialization(t)
        return TaskDB(t.id, ts['desc'], ts['workdir'], ts['worker'], ts['type'], ts['state'], t.time_stamp, ts['dependency'], t.is_root. ts['data'])

    def to_json(self):
        dct = {'__task__': True,
               'id': self.id,
               'desc': self.desc,
               'workdir': self.workdir,
               'worker': self.worker,
               'ttype': self.type,
               'state': self.state,
               'time_stamp': TaskStamp(self.create, self.start, self.end).to_json(),
               'dependency': self.dependency,
               'is_root': self.is_root,
               'data': json.loads(self.data)}
        return json.dumps(dct)


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
        sess = cls.session_maker()()
        records = sess.query(TaskDB).delete()
        sess.commit()

    @classmethod
    def session(cls):
        return cls.session_maker()()

"""
==================
Task system design
==================

Task
====

Overview
--------
Task object is a *representation* of a logical task, which is designed to be:
#. 
#. 

Features
--------
#. self content
    A task object contains **ALL** information to perform a task with the help of task server.
#. subtask list
    A task may be consisted by multiple subtasks. There are two type of tasks, 
#. task state inspect
#. task serilization, database support (Optional)
    retrieve task from file, or database


Task server
-----------
#. Task factory
#. Task query
    #. on running
    #. history (recent)

#. List of tasks
#. Create(Load Tasks):
    #. create from scrach
    #. from file
        #. given path
        #. from database 




SLURM => Resource Unlimited
(Pending system)
OS, Hardware => Resource Limited
"""


import json
import time
import yaml
from dxpy.file_system.path import Path
from dxpy.tasks.progbar import ProgBar

class Task(yaml.YAMLObject):
    yaml_tag = '!task'
    yaml_flow_style = False

    def __init__(self, tid, name=None, workdir=None, command=None, *, desc=None, sub_tasks=None):
        self.id = tid
        self.name = name or '<undifined>'
        self.workdir = workdir or Path('.')
        self.command = command or '<undifined>'
        self.sub_tasks = sub_tasks
        self.desc = desc or '<undifined>'

    def __str__(self):
        return yaml.dump(self)

    def _solve_dependencies(self):
        pass

    def __iter__(self):
        pass


# class Task_:
#     def __init__(self,
#                  task_id,
#                  path_work,
#                  path_json=None,
#                  name=None,
#                  desc=None,
#                  prog_bar=None):
#         self.id = task_id
#         self.path_work = str(Path(path).absolute())
#         self.path_json = path_json or "t{id}.json".format(id=self.id)
#         self.name = name or "task_{0:d}".format(_id)
#         self._prog_bar = prog_bar or ProgBar(
#             1, message='ProgBar of task {tname}.'.format(name=self._name))
#         self.desc = desc or ""

#     @property
#     def prog_bar(self):
#         return self._prog_bar

#     class _JSONEncoder(json.JSONEncoder):
#         """ JSON encoder of ProgBar cls """

#         def default(self, obj):
#             if isinstance(obj, Task):
#                 dct = {
#                     '__Task__': True,
#                     'name': obj.name,
#                     'id': obj.id,
#                     'prog_bar': obj.prog_bar.to_json()
#                     'path': obj.path
#                 }
#             return dct
#             return json.JSONEncoder.default(self, obj)

#     @staticmethod
#     def json_decoder(dct):
#         """ JSON decoder of ProgBar cls """
#         if '__Task__' in dct:
#             task_id = dct['id']
#             task_path = dct['path']
#             name = dct.get('name')
#             prog_bar = ProgBar.from_json(dct['prog_bar'])
#             return Task(task_id=task_id, path=task_path, name=name, prog_bar=prog_bar)
#         else:
#             return dct

#     def to_json(self):
#         return json.dumps(self, cls=Task._JSONEncoder)

#     @staticmethod
#     def from_json(s):
#         return json.loads(s, object_hook=Task.json_decoder)

#     # For test only, time stamp is not intend to save to database
#     db_model = None

#     @staticmethod
#     def get_db_model(db):
#         if Task.db_model is None:
#             class TaskDatabaseModel(db.Model):
#                 name = db.Column(db.String(255))
#                 path_work = db.Column(db.String(512))
#                 path_json = db.Column(db.String(512))
#                 prog = db.Column(db.Float)
#                 start = db.Column(db.Float)
#                 desc = db.Column(db.Text)

#                 def __init__(self, name, path_json, path_work, prog, start, desc):
#                     self.name = name
#                     self.path_json = path_json
#                     self.path_work = path_work
#                     self.prog = prog
#                     self.start = start
#                     self.desc = desc
#             Task.db_model = TaskDatabaseModel
#             return TaskDatabaseModel
#         else:
#             return Task.db_model

#     @staticmethod
#     def from_dbobj(obj):
#         path_json = obj.path_json
#         return Task.from_json(path_json)

#     def to_dbobj(self, db):
#         return self.get_db_model(db)(self.name, self.path_json, self.path_work, self.prog_bar.progress, self.prog_bar.start, self.desc)

#     def update_dbobj(self, db):
#         tsk = Task.get_db_model(db).query.get(self.id)
#         tsk['name'] = self.name
#         tsk['path_json'] = self.path_json
#         tsk['path_work'] = self.path_work
#         tsk['progress'] = self.prog_bar.progress
#         tsk['start'] = self.prog_bar.start
#         tsk['desc'] = self.desc
#         db.session.commit()

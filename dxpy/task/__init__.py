"""
==================
Task system design
==================

User
====

TaskAPI
=======
Functions:
----------
#. create(TaskTemplate, args, kwargs) ->
#. get(id)



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
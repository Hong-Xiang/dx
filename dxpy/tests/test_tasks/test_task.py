import unittest
from dxpy.tasks.task import Task


class TestTask(unittest.TestCase):
    def test_str(self):
        t = Task(id=1, name='test_str', desc='Test task for str.')
        assert str(t) == """<Task #1:
        name: test_str,
        workdir: None,
        sub_tasks: None,
        command: None,
        desc: Test task for str,
        >"""

    def test_add_sub_task(self):
        t = Task(id=1, name='main task')
        st1 = Task(id=2, name='sub task1')
        st2 = Task(id=3, name='sub task2')
        t.add(st1)
        t.add(st2)
        assert t.sub_tasks.size = 2
        assert t.sub_tasks.get(2).name == 'sub 1'
        assert t.sub_tasks.get(3).name == 'sub 2'

    def test_add_chain_task(self):
        t = (Task(1, 'main task')
             .add(Task(2, 'sub 1'))
             .add(Task(3, 'sub 2'))
             )
        assert t.sub_tasks.size = 2
        assert t.sub_tasks.get(2).name == 'sub 1'
        assert t.sub_tasks.get(3).name == 'sub 2'

    def test_add_task_dependency(self):
        tpre = Task(1, 'pre task')
        tinc = Task(2, 'inc task').wait([tpre])
        assert tinc.denpendencies == [tpre]
    
    def test_task_generator(self):
        t = Task(1, 'main task')
        t1 = Task(2, 'sub task 1')
        t2 = Task(3, 'sub task 2')
        t.add(t1).add(t2)
        assert next(t).name == 'sub task 1'
        assert next(t).name == 'sub task 2'
    


import unittest
from dxpy.task.representation import factory
from dxpy.task.representation.taskpy import TaskPy


class TestFactory(unittest.TestCase):
    def test_create(self):
        t = factory.create('Task')
        self.assertIsInstance(t, TaskPy)

    def test_create_graph(self):
        tasks = [factory.create('Task') for _ in range(3)]
        g = factory.create_task_graph(tasks, [None, 0, 1])
        self.assertTrue(g.is_depens_on(tasks[1], tasks[0]))
        self.assertFalse(g.is_depens_on(tasks[0], tasks[1]))

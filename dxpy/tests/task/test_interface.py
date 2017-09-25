import unittest
from unittest.mock import Mock

import dxpy.task.interface as ti


class TestInterface(unittest.TestCase):
    def setUp(self):
        pass

    def test_parset_json(self):
        from dxpy.task.representation import TaskPy
        s = '[{"id": 1, "desc": "sleep task", "body": "!!python/object:dxpy.task.representation.templates.TaskCommand\\nactivity: true\\ncommand: sleep 10\\ndependency: []\\ndesc: sleep task\\nid: 1\\nis_root: true\\nstate: !task_state \'BeforeSubmit\'\\ntime_stampes: !!python/object:dxpy.time.timestamps.Start\\n  time_stamps: {start: !!timestamp \'2017-09-22 12:57:44.036185\'}\\nworkdir: !path \'/home/hongxwing/Workspace/jpyn\'\\nworkers: !!python/object:dxpy.task.misc.Workers {info: null, nb_workers: 1, type: !worker_type \'MultiThreading\'}\\n", "dependency": [], "time_create": "2017-09-22 12:57:44.036185", "state": "BeforeSubmit", "is_root": true}]'
        self.assertEqual(ti.parse_json(s).id == 1)
        self.assertIsInstance(ti.parse_json(s), TaskPy)

    def test_read(self):
        ti.parse_json = Mock()
        ti.db = Mock()
        ti.read(0)
        ti.db.assert_called_with(0)
        ti.parse_json.assert_called()

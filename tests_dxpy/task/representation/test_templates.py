import unittest
import rx
from unittest.mock import Mock
from dxpy.file_system.path import Path
from dxpy.task.representation import templates


class TestTemplates(unittest.TestCase):
    def test_command(self):
        p = Path('/tmp/test')
        task = templates.TaskCommand(command='ls', workdir=p)
        self.assertEqual(task.plan(), 'cd /tmp/test && ls')

    def test_script(self):
        p = Path('/tmp/test')
        task = templates.TaskScript(file=p / 'run.sh', workdir=p)
        self.assertEqual(task.plan(), 'cd /tmp/test && /tmp/test/run.sh')

    def test_script_sbatch(self):
        p = Path('/tmp/test')
        task = templates.TaskScript(file=p / 'run.sh', workdir=p)

        def sbatch_command(workdir, script_file):
            return 'cd {0} && sbatch {1}'.format(workdir, script_file)
        self.assertEqual(task.plan(sbatch_command),
                         'cd /tmp/test && sbatch /tmp/test/run.sh')

#!/home/hongxwing/anaconda3/bin/python
import click


class CLI(click.MultiCommand):
    commands = {'code': None,
                'task': None,
                'batch': None,
                'run': None,
                'ln': None,
                'pj': None,
                'mi': None}

    def __init__(self):
        super(__class__, self).__init__(name='dxl', help='DXL CLI tools.')

    def list_commands(self, ctx):
        return sorted(self.commands.keys())

    def get_command(self, ctx, name):
        from ..task import cli as task
        from ..code import cli as code
        from ..batch.api.cli import batch
        from ..run import run_cli
        from ..learn.run.cli import main as learn 
        from ..projects.cli import main as pj
        from ..medical_image_processing.run.cli import main as mi
        if name in self.commands:
            if self.commands[name] is None:
                mapping = {
                    'code': code,
                    'task': task,
                    'batch': batch,
                    'run': run_cli,
                    'ln': learn,
                    'pj': pj,
                    'mi': mi, 
                }
                self.commands[name] = mapping.get(name)
        return self.commands.get(name)


cli = CLI()

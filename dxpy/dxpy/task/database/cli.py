import click


@click.group()
def db():
    pass


@click.command()
def start():
    from . import web
    """ start task database web service """
    web.launch_database_server()


db.add_command(start)
import click


class CLI(click.MultiCommand):
    """
    Tasks cli tools.
    """
    commands = {'start': None}

    def __init__(self):
        super(__class__, self).__init__(name='task', help=__class__.__doc__)

    def list_commands(self, ctx):
        return sorted(self.commands.keys())

    def get_command(self, ctx, name):
        from ..database.cli import db
        from ..run.cli import run
        from .commands import ui
        if name in self.commands:
            if self.commands[name] is None:
                mapping = {
                    'db': db,
                    'run': run,
                    'ui': ui
                }
                self.commands[name] = mapping.get(name)
        return self.commands.get(name)


db = CLI()

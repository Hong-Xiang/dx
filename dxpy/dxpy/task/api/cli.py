import click


@click.group()
def ui():
    pass


@ui.command()
def start():
    from . task import web
    web.lauch_database_server()


class CLI(click.MultiCommand):
    """
    Tasks cli tools.
    """
    commands = {'db': None, 'run': None, 'ui': None}

    def __init__(self):
        super(__class__, self).__init__(name='task', help=__class__.__doc__)

    def list_commands(self, ctx):
        return sorted(self.commands.keys())

    def get_command(self, ctx, name):
        from ..database.cli import db
        from ..run.cli import run
        if name in self.commands:
            if self.commands[name] is None:
                mapping = {
                    'db': db,
                    'run': run,
                    'ui': ui
                }
                self.commands[name] = mapping.get(name)
        return self.commands.get(name)


task = CLI()

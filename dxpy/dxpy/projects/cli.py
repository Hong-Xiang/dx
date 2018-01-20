import click

class CLI(click.MultiCommand):
    """
    Helper of projects specified CLI module.
    """
    commands = {'sr': None}

    def __init__(self):
        super().__init__(name='pjs', help=__class__.__doc__)

    def list_commands(self, ctx):
        return sorted(self.commands.keys())

    def get_command(self, ctx, name):
        from .super_resolution.cli import main as main_sr
        mapped = {'sr': main_sr}
        if name in self.commands and self.commands[name] is None:
            self.commands[name] = mapped[name]
        return self.commands.get(name)

main = CLI()

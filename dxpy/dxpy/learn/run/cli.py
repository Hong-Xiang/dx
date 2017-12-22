import click

class CLI(click.MultiCommand):
    """
    Helper of learn module.
    """
    commands = {'train': None, 'dataset': None, 'main': None, 'train2': None, 'train_dist': None}

    def __init__(self):
        super(__class__, self).__init__(name='tf', help=__class__.__doc__)

    def list_commands(self, ctx):
        return sorted(self.commands.keys())

    def get_command(self, ctx, name):
        from . import commands
        if name in self.commands and self.commands[name] is None:
            self.commands[name] = getattr(commands, name)
        return self.commands.get(name)


main = CLI()

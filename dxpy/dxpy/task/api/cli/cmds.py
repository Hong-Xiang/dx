import click


@click.group()
def ui():
    pass


@ui.command()
def start():
    click.echo('Starting task operation server...')
    from ..web import lauch_database_server
    lauch_database_server()


from ...database import cli as db
from ...run.cli import run

import click
from . import web


@click.group()
def db():
    pass


@click.command()
def start():
    """ start task database web service """
    web.launch_database_server()


db.add_command(start)

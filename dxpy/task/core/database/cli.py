import click
from .resource import lauch_database_server
@click.group()
def db():
    pass

@click.command()
def start():
    """ start task database web service """
    lauch_database_server()

db.add_command(start)

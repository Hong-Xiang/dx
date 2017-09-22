import click
from .database.web.cli import db


@click.group()
def task():
    pass


task.add_command(db)

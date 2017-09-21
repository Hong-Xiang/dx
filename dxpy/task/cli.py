import click
from dxpy.task.database.cli import db

@click.group()
def task():
    pass

task.add_command(db)


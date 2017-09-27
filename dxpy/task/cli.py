import click
from .database.web.cli import db
from .run.cli import run

@click.group()
def task():
    pass


task.add_command(db)
task.add_command(run)

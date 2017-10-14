import click
from dxpy.task.database.cli import db
from dxpy.task.run.cli import run
from dxpy.task import web


@click.group()
def task():
    pass


@click.group()
def ui():
    pass


@ui.command()
def start():
    web.lauch_database_server()


task.add_command(db)
task.add_command(run)
task.add_command(ui)

if __name__ == "__main__":
    task()

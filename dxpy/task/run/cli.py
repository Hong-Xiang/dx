import click
from .service import launch_deamon

@click.group()
def run():
    pass

@click.command()
def start():
    """ start task database web service """
    launch_deamon()
    input("Press any key to exit\n")

run.add_command(start)

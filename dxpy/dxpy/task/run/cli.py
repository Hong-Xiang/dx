import click


@click.group()
def run():
    pass


@click.command()
def start():
    """ start task database web service """
    from . service import launch_deamon
    launch_deamon()
    input("Press any key to exit\n")


run.add_command(start)

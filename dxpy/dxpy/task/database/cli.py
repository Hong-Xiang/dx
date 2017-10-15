import click


@click.group()
def db():
    pass


@click.command()
def start():
    from . import web
    """ start task database web service """
    web.launch_database_server()


db.add_command(start)

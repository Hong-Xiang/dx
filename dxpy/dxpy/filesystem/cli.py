import click
from hqlf.filesystem.service import launch_web_ui


@click.group()
def filesystem():
    pass


@filesystem.command()
@click.option('--host', type=str, default='0.0.0.0')
@click.option('--port', type=int, default=5000)
@click.option('--debug', is_flag=True)
def start(host, port, debug):
    click.echo('START CALLED')
    launch_web_ui(host, port, debug=debug)


if __name__ == "__main__":
    filesystem()

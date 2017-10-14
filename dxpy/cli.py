import click
from dxpy.task.cli import task


@click.group()
def dxl():
    pass

dxl.add_command(task)

if __name__ == "__main__":
    dxl()
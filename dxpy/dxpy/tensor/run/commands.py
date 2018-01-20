import click


@click.group()
def npz():
    pass


@npz.command()
@click.argument('filename')
def ls(filename):
    from ..npz import list_npz
    list_npz(filename)

@npz.command()
@click.argument('filename')
@click.option('--output', '-o', type=str, help='Outputname, use same name and change suffix to mat if not given.')
def tomat(filename, output):
    from ..npz import npz2mat
    if output is None:
        output = filename[:-3] + 'mat'
    npz2mat(filename, output)

@npz.command()
@click.argument('filename', nargs=-1)
@click.argument('output')    
def cat(filename, output):
    from ..npz import concatenate
    concatenate(filename, output)


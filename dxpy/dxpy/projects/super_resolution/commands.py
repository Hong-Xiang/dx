import click

@click.command()
def hello():
    click.echo('HELLO FROM SR.HELLO!')

@click.command()
@click.option('--input', '-i', type=str)
@click.option('--output', '-o', type=str)
def analysis(input, output):
    from .analysis import analysis_result
    analysis_result(input, output)

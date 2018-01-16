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

@click.command()
@click.option('--input', '-i', type=str)
@click.option('--output', '-o', type=str)
def npz2mat(input, output):
    import numpy as np
    from scipy.io import savemat
    data = np.load(input)
    data = {k: data[k] for k in data}
    savemat(output, data)
    
# @click.command()
# @click.option('--input', '-i', type=str)
# @click.option('--output', '-o', type=str)
# @click.option('--metrices', '-m', type=str, )
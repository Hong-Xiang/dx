import click


@click.command()
@click.option('--input', '-i', type=str)
@click.option('--output', '-o', type=str)
@click.option('--skip_keys', '-s', type=str)
@click.option('--phantom_x', '-x', type=int)
@click.option('--phantom_y', '-y', type=int)
@click.option('--sen_width', '-w', type=float)
def reconnpz(input, output, skip_keys, phantom_x, phantom_y, sen_width):
    from dxpy.tensor.io import load_npz

    from .dataset import dataset_dist
    from dxpy.learn.utils.general import load_yaml_config
    load_yaml_config(config)
    dataset_dist(name)
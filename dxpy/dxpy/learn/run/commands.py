import click

def get_main_net(net_name):
    from dxpy.learn.net.zoo.srms.train import main as srms
    if net_name == "srms":
        return srms

@click.command()
@click.option('--config', '-c', type=str, help='configs .yml filename')
@click.option('--net', '-n', type=str, help='name of main net', default=None)
def train(net, config):    
    main_net_train = get_main_net(net)
    main_net_train()

@click.command()
@click.option('--config', '-c', type=str, help='configs .yml filename', default='dxln.yml')
@click.option('--name', '-n', type=str, help='cluster name of dataset in config file, e.g. cluster/dataset/task0.')
def dataset(name, config):
    from .dataset import dataset_dist
    from dxpy.learn.utils.general import load_yaml_config
    load_yaml_config(config)
    dataset_dist(name)
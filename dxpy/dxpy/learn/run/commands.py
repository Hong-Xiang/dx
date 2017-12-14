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

@click.command()
@click.option('--name', '-n', type=str, help='name of network')
@click.option('--config', '-c', type=str, help='configs .yml filename', default='dxln.yml')
@click.option('--job_name', '-j', type=str)
@click.option('--task_index', '-t', type=int)
@click.option('--run', '-r', type=str, help='run task', default='train')
def main(name, job_name, task_index, run, config):
    from dxpy.learn.utils.general import load_yaml_config
    load_yaml_config(config)
    if name == 'sin':
        from .zoo.sin.main import main
        main(run, job_name, task_index)
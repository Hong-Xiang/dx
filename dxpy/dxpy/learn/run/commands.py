import click


def get_main_net(net_name):
    from dxpy.learn.net.zoo.srms.train import main as srms
    if net_name == "srms":
        return srms


def get_main_func(net_name):
    pass


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
    elif name == 'srms':
        from .zoo.srms.main import main
        main(run, job_name, task_index)
    else:
        raise ValueError("Unknown name {} for dxpy.ln.main CLI.".format(name))


@click.command()
@click.option('--train_config_name', '-t', type=str)
@click.option('--dataset_maker_name', '-d', type=str)
@click.option('--network_maker_name', '-n', type=str)
@click.option('--summary_maker_name', '-s', type=str)
@click.option('--config', '-c', type=str, default='dxln.yml')
def train2(train_config_name, config, dataset_maker_name=None, network_maker_name=None, summary_maker_name=None):
    if dataset_maker_name is None:
        dataset_maker_name = train_config_name
    if network_maker_name is None:
        network_maker_name = train_config_name
    if summary_maker_name is None:
        summary_maker_name = train_config_name
    from .base import DxlnRunEnvrionment
    with DxlnRunEnvrionment(config):
        from dxpy.learn.dataset.api import get_dataset
        from dxpy.learn.net.api import get_network, get_summary
        dataset = get_dataset(dataset_maker_name)
        network = get_network(network_maker_name, dataset=dataset)
        result = network()
        summary = get_summary(summary_maker_name, dataset, network, result)
        from .train import train_with_monitored_session
        train_with_monitored_session(network)

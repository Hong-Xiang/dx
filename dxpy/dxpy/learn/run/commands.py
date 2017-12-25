import click
import warnings


def get_main_net(net_name):
    warnings.warn(DeprecationWarning("Deprecated, no suggestion."))
    from dxpy.learn.net.zoo.srms.train import main as srms
    if net_name == "srms":
        return srms


def get_main_func(net_name):
    warnings.warn(DeprecationWarning("Deprecated, no suggestion."))
    pass


@click.command()
@click.option('--config', '-c', type=str, help='configs .yml filename')
@click.option('--net', '-n', type=str, help='name of main net', default=None)
def train(net, config):
    warnings.warn(DeprecationWarning("Deprecated, use train2."))
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
    from .train import train_task_local
    with DxlnRunEnvrionment(config):
        train_task_local(dataset_maker_name,
                         network_maker_name,
                         summary_maker_name)


@click.command()
@click.option('--cluster_file', '-f', type=str, default='cluster.yml', help='cluster config file name.')
@click.option('--config', '-c', type=str, help='configs .yml filename', default='dxln.yml')
@click.option('--job_name', '-j', type=str)
@click.option('--task_index', '-t', type=int)
def train_dist(cluster_file, job_name, task_index, config):
    """
    Run dist tasks
    """
    from dxpy.learn.distribute.cluster import get_cluster_spec
    from .base import DxlnRunEnvrionment
    cluster = get_cluster_spec(cluster_file)
    from .train import train_task_dist
    with DxlnRunEnvrionment(config):
        train_task_dist(name='cluster/{}/task{}'.format(job_name, task_index),
                        cluster=cluster)

import click
def get_main_net(net_name):
    from dxpy.learn.net.zoo.srms.train import main as srms
    if net_name == "srms":
        return srms

@click.command()
@click.option('--config', '-c', type=str, help='configs .yml filename')
@click.option('--net', '-n', type=str, help='name of main net')
def train(net, config):    
    main_net_train = get_main_net(net)
    main_net_train()

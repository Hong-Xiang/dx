import click


@click.group()
def tf():
    pass


@tf.command()
@click.option('--config', '-c', type=str, help='configs .yml filename')
@click.option('--net', '-n', type=str, help='name of main net')
def train(net, config):    
    main_net = get_main_net(net)
    main_net.train()

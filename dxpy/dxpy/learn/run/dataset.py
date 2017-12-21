import click
from dxpy.configs import configurable, ConfigsView
import dxpy.learn.config as config


def dataset_dist(cluster_name):
    from dxpy.learn.distribute.dataset import start_dataset_server
    start_dataset_server(name=cluster_name)

from dxpy.filesystem import Path
import os

config = dict()


def get_config():
    from dxpy.configs import ConfigsView
    return ConfigsView(config)


def clear_config():
    global config
    config = dict()

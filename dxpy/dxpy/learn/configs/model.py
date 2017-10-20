from dxpy.filesystem.path import Path
from dxpy.configs.base import Configs
from ruamel.yaml import YAML


class ConfigsSave(Configs):
    _names = ('frequency', 'method')
    defaults = {
        'frequency': 100,
        'method': 'step'
    }

    def __init__(self, **kwargs):
        super(__class__, self).__init__(**kwargs)


ConfigsSave.add_yaml_support()


class ConfigsLoad(Configs):
    _names = ('is_load', 'step')
    defaults = {
        'is_load': True,
        'step': -1
    }

    def __init__(self, **kwargs):
        super(__class__, self).__init__(**kwargs)


ConfigsLoad.add_yaml_support()


class ConfigsModelFS(Configs):
    _names = ('path_model', 'ckpt_name')
    defaults = {
        'path_model': './model',
        'ckpt_name': 'save'
    }

    def __init__(self, **kwargs):
        super(__class__, self).__init__(**kwargs)


ConfigsModelFS.add_yaml_support()


class ConfigsTrain(Configs):
    _names = ('model_fs', 'load', 'save')
    defaults = {
        'model_fs': ConfigsModelFS(),
        'load': ConfigsLoad(),
        'save': ConfigsSave()
    }

    def __init__(self, **kwargs):
        super(__class__, self).__init__(**kwargs)


ConfigsTrain.add_yaml_support()

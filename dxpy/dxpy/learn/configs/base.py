from dxpy.collections import TreeDict
from ruamel.yaml import YAML
yaml = YAML()

config = TreeDict()

from dxpy.configs import ConfigsView


# TODO: Add support for global configs
# def load_default():
#     from dxpy.code import path_of_global_defaults
#     path_global_config = Path(path_of_global_defaults / 'xlean.yml').abs
#     with open('path')
#     global_config = yaml.load(path)


import copy
from dxpy.collections.dicts import DXDict


class Configs(DXDict):
    """
    A configs object is a *imutable* dict like collection. elements of the collection can be one of the following:
    #. basic types (str, int, bool)
    #. list or dict of basic types
    #. Configs object
    #. list or dict of Configs
    """
    _names = tuple()
    default_configs = {}

    def __init__(self, **kwargs):
        super(__class__, self).__init__(**kwargs)
        self.apply_default(self.default_configs)

    @classmethod
    def names(cls):
        """ All keys of a configs class.
        """
        return cls._names

    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        else:
            return self.default_dict[key]

    @classmethod
    def add_yaml_support(cls):
        from ruamel.yaml import YAML
        yaml = YAML()
        yaml.register_class(cls)


Configs.add_yaml_support()

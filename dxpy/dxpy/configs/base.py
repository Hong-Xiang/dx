import copy


class Configs:
    """
    A configs object is a *imutable* dict like collection. elements of the collection can be one of the following:
    #. basic types (str, int, bool)
    #. list or dict of basic types
    #. Configs object
    #. list or dict of Configs
    """
    keys = tuple()
    defaults = {}

    @classmethod
    def keys(cls):
        """ All keys of a configs class.
        """
        return cls.keys

    @classmethod
    def defaults(cls):
        """
        Note: keys not exists in cls.keys() are ignored.
        """
        return cls.defaults

    def __init__(self, **kwargs):
        for k in kwargs:
            self.k = kwargs[k]

    def get(self, key):
        if not hasattr(self, k):
            return None
        else:
            return copy.deepcopy(self.k)

    def apply_defaults(self, recursive=True):
        results = {}
        for k in self.keys():
            if self.get(k) is None:
                results.update({k: self.defaults().get(k)})
            elif isinstance(self.k, Configs) and recursive:
                results.update({k: self.k.apply_defaults(recursive)})
            else:
                results.update({k: self.k})
        return type(self)(**results)

    def append_update(self, configs, extend_keys=False):
        results = {}
        for k in self.keys():
            if self.get(k) is None:
                results.update({k: configs.get(k)})
            else:
                results.update({k: self.get(k)})
        return type(self)(**results)

    @classmethod
    def add_yaml_support(cls):
        from ruamel.yaml import YAML
        yaml = YAML()
        yaml.register_class(cls)


Configs.add_yaml_support()

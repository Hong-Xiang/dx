from collections import UserDict
from dxpy import serialization
from dxpy.filesystem import Path


class DXDict(UserDict):
    yaml_tag = '!dxdict'

    def __init__(self, *args, default_dict=None, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        if default_dict is not None:
            self.default_dict = DXDict(default_dict)
        else:
            self.default_dict = None

    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        elif self.default_dict is not None:
            return self.default_dict[key]
        return None

    def keys(self):
        from itertools import chain
        if self.default_dict is not None:
            return chain(self.data.keys(), self.default_dict.keys())
        else:
            return self.data.keys()

    def apply_default(self, default_dict):
        if self.default_dict is None:
            return DXDict(self.data, default_dict=default_dict)
        else:
            return DXDict(self.data, default_dict=self.default_dict.apply_default(default_dict))


serialization.register(DXDict)

from .trees import PathTree


class TreeDict(PathTree):
    yaml_tag = '!treedict'

    def __init__(self, *args, **kwargs):
        pass

    def compile(self):
        pass

    def _push_dict(self, path, dct):
        new_dict = self.get_data(path).apply_default(dct)
        self.get_node(path).data = new_dict
        nodes = self.tree.children(path)
        for n in nodes:
            self._push_dict(n.indentifier, self.get_node(path).data)

    def __getitem__(self, path):
        return self.get_data(path)

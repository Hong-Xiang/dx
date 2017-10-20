from collections import UserDict


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


from dxpy import serialization
serialization.register(DXDict)

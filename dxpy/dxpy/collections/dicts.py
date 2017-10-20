from collections import UserDict


class DXDict(UserDict):
    def __init__(self, *args, default_dict=None, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.default_dict = default_dict

    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        else:
            return self.default_dict[key]

    def apply_default(self, default_dict):
        if self.default_dict is None:
            return DXDict(self.data, default_dict=default_dict)
        else:
            return DXDict(self.data, default_dict=self.default_dict.apply_default(default_dict))

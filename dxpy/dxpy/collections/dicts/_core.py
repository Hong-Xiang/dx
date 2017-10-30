from collections import UserDict
from dxpy import serialization
from dxpy.filesystem import Path
from ._exceptions import NotDictError


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

# from .trees import PathTree


# class TreeDict(PathTree):
#     yaml_tag = '!treedict'

#     def __init__(self, *args, **kwargs):
#         super(__class__, self).__init__()

#     def compile(self):
#         self._push_dict()

#     def _push_dict(self, path=None, dct=None):
#         if dct is None:
#             dct = DXDict()
#         if path is None:
#             path = '/'
#         if self.get_data(path) is None:
#             self.get_node(path).data = DXDict(dct)
#             new_dict = self.get_node(path).data
#         else:
#             new_dict = self.get_data(path).apply_default(dct)
#         self.get_node(path).data = new_dict
#         nodes = self.tree.children(path)
#         for n in nodes:
#             self._push_dict(n.indentifier, self.get_node(path).data)

#     def __getitem__(self, path):
#         return self.get_data(path)

#     def add_dict(self, name, parent, dct):
#         self.create_node(name, parent, data=DXDict(dct))


# TODO: Add yaml support.
class TreeDict(UserDict):
    """
    A dict with tree struct:
        1. Supports three different access method:
            1. a['key1']['key2']
            2. a['/key1/key2']
            3. a.get(['key1','key2'])
            4. a.get('key1')
        2. Autogenerate for missing layers
            If there is no a['name1'] dict while setting a['name1']['name2'],
            an empty TreeDict will be created on a['name1']
        3. Inherence values
            If we are accessing a['name1']['name2'], but there is not 'name2' key in a['name1'],
            the dict will try to find if there is 'name2' in a (root).
        4. KeyError only happens when need a dict but got a object which is not dict,
           For those keys are not defined in the TreeDict, return a empty TreeDict object.
    """
    yaml_tag = '!dxdict'

    def __init__(self, dct=None, fa=None):
        """

        Inputs:
            - dct: dict like object, dict, Userdict or TreeDict,
            - fa: father node, object of TreeDict,

        Raises:
            None

        """
        # if dct is not None and not isinstance(dct, (dict, UserDict)):
        #     raise NotDictError(type(dct))
        super(__class__, self).__init__(dct)
        self.fa = fa
        for k in self.data:
            self._unfied_dict_element(k, False)

    def get(self, key):
        keys = self._unified_and_processing_input_key(key)
        return self._get(keys)

    def __getitem__(self, key):
        return self.get(key)

    def set(self, key, value):
        keys = self._unified_and_processing_input_key(key)
        self._set(keys, value)

    def __setitem__(self, key, value):
        self.set(key, value)

    def _ensure_mid_layers(self, keys):
        if len(keys) > 1:
            if not keys[0] in self.data:
                self.data[keys[0]] = TreeDict(fa=self)
            else:
                self._unfied_dict_element(keys[0], True)

    @classmethod
    def _unified_keys(cls, key_or_keys_or_path):
        if isinstance(key_or_keys_or_path, (list, tuple)):
            return tuple(key_or_keys_or_path)
        elif isinstance(key_or_keys_or_path, str):
            result = tuple(Path(key_or_keys_or_path).parts)
            if len(result) > 0 and result[0] == '/':
                result = result[1:]
            return result
        else:
            raise TypeError(
                "Key not supported {}.".format(key_or_keys_or_path))

    def _update_child_dct(self, dct, key=None):
        if isinstance(dct, TreeDict):
            if dct.fa is None:
                dct.fa = self
            return dct
        if isinstance(dct, (dict, UserDict)):
            result = TreeDict(dct, fa=self)
            if key is not None:
                self.data[key] = result
            return self.data[key]
        else:
            return None

    def _unfied_dict_element(self, key, required=False):
        from ._exceptions import KeyNotDictError
        result = self._update_child_dct(self.data[key], key)
        if result is None and required:
            raise KeyNotDictError(key, type(self.data[key]))
        return result

    def _unified_and_processing_input_key(self, key_or_keys_or_path):
        keys = self._unified_keys(key_or_keys_or_path)
        self._ensure_mid_layers(keys)
        return keys

    def _get_value_by_key_from_inherence(self, key):
        if self.fa is None:
            result = None
        else:
            result = self.fa._get_value_by_key(key)

        if result is None:
            self.data[key] = TreeDict()
            result = self.data[key]
        return result

    def _get_value_by_key(self, key):
        if key in self.data:
            return self.data[key]
        return self._get_value_by_key_from_inherence(key)

    def _get(self, keys):
        if len(keys) == 0:
            raise ValueError(
                "TreeDict requires positve len(keys), probably using key = None?")
        if len(keys) == 1:
            return self._get_value_by_key(keys[0])
        result = self._unfied_dict_element(keys[0], True)
        return result.get(keys[1:])

    def _set(self, keys, value):
        if len(keys) == 1:
            self.data[keys[0]] = value
            self._unfied_dict_element(keys[0], False)
        else:
            self.data[keys[0]].set(keys[1:], value)

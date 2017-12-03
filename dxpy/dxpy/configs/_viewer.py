from dxpy.core.path import Path


class ConfigsView:
    def __init__(self, dct, base_path=''):
        self.data = dct
        self.base = Path(base_path)

    def __unified_keys(self, path_or_keys):
        if isinstance(path_or_keys, (list, tuple)):
            return list(self.base.parts()), list(path_or_keys)
        else:
            return list(self.base.parts()), list(Path(path_or_keys).parts())

    def _get_value_raw(self, keys):
        result = self.data
        for k in keys:
            if result is None:
                return result
            result = result.get(k)
        return result

    def _form_path(self, keys):
        return '/'.join(keys)

    def _query(self, base_keys, local_keys):
        # if len(local_keys) <= 1:
        result = self._get_value_raw(base_keys + local_keys)
        # else:
            # path = self.base / local_keys[0]
            # key_path = self._form_path(local_keys[1:])
            # result = ConfigsView(self.data, path)._query(key_path)
        return result

    def _search(self, key):
        base_keys, local_keys = self.__unified_keys(key)
        result = self._query(base_keys, local_keys)
        path = self._form_path(base_keys + local_keys)
        if result is None and len(base_keys) > 0:
            new_path = self._form_path(base_keys[:-1] + local_keys)
            result, _ = ConfigsView(self.data)._search(new_path)
        return result, path

    def _post_processing(self, result, path, default, restrict):
        if isinstance(result, dict) or (result is None and default is None and not restrict):
            result = ConfigsView(self.data, path)
        elif result is None:
            result = default
        return result

    def to_dict(self):
        result, path = self._search(str(self.base))
        if isinstance(result, dict):
            return result
        else:
            raise ValueError("Configs view on base path is not dict.")

    def get(self, key, default=None, *, restrict=False):
        result, path = self._search(key)
        return self._post_processing(result, path, default, restrict)

    def __getitem__(self, key):
        return self.get(key, restrict=True)


def child_view(configs_view, extend_path):
    return ConfigsView(configs_view.base_path / str(extend_path), configs_view.data)

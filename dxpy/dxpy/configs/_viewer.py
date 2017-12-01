from dxpy.core.path import Path


class ConfigsView:
    def __init__(self, dct, base_path=''):
        self.data = dct
        self.base = Path(base_path)

    def __unified_keys(self, path_or_keys):
        if isinstance(path_or_keys, (list, tuple)):
            return tuple(list(self.base.parts()) + list(path_or_keys))
        else:
            return Path(self.base / path_or_keys).parts()

    def _query_hard(self, key):
        from dxpy.debug.utils import dbgmsg
        dbgmsg(self.data)
        dbgmsg(str(self.base))
        dbgmsg(key)
        keys = self.__unified_keys(key)
        if len(keys) == 1:
            result = self.data.get(keys[0])
        else:
            path = self.base / keys[0]
            key_path = '/'.join(keys[1:])
            result = ConfigsView(self.data, path)._query_hard(key_path)
        return result

    def __query(self, key, default=None):
        result = self._query_hard(key)
        if isinstance(result, dict):
            result = ConfigsView(self.data, self.base / key)
        path = Path(self.base)
        if result is None and len(path.parts()) > 0:
            path = path.parent()
            result = ConfigsView(self.data, path)._query_hard(key)
        if result is None:
            result = default
        return result

    def get(self, key, default=None):
        return self.__query(key, default)

    def __getitem__(self, key):
        return self.get(key)


def child_view(configs_view, extend_path):
    return ConfigsView(configs_view.base_path / str(extend_path), configs_view.data)

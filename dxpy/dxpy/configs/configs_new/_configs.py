from ..path import Path


class Configs:
    def __init__(self, base_path, dct_or_config_viewer):
        if isinstance(dct_or_config_viewer, Configs):
            base_path = dct_or_config_viewer.base / str(Path(base_path))
            self.data = dct_or_config_viewer.data
        else:
            self.data = dct_or_config_viewer
        self.base = Path(base_path)

    def __get_by_keys(self, keys):

        while result is None:
            result = self
        for k in keys:
            result =

    def get(self, key):
        keys = self._unified_and_processing_input_key(key)

    def __getitem__(self, key):
        return self.get(key)


class ConfigsSetter:
    def __init__(self, config_dict):
        self._data = config_dict

    def update(self, path, dct):
        target = self._get_item(Path(path).parent())
        target[Path(path).basename].update(dct)

    def join(self, path, dct):
        target = self._get_item(Path(path).parent())
        for k in target[Path(path).basename]:

        target[Path(path).basename] = dct

    def _get_item(self, path):
        result = self
        for k in Path(path).parts():
            result = result[k]
        return result

    def __getitem__(self, key):
        from ..code import DXPYTypeError
        if not key in self._data:
            self._data[key] = dict()
            return ConfigsSetter(self._data[key])
        elif isinstance(self._data[key], dict):
            return ConfigsSetter(self._data[key])
        else:
            raise DXPYTypeError(dict, self._data[key],
                                'Value of Key {}'.format(key))

    def __setitem__(self, key, value):
        self._data[key] = value

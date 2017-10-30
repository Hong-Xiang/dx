from ruamel.yaml import YAML
yaml = YAML()


class ModuleConfigs:
    def __init__(self, module_name=None, path_user=None, path_workspace=None):
        from dxpy.collections import TreeDict
        self.module_name = module_name
        self.path_user = self._path_config_file(path_user)
        self.path_workspace = self._path_config_file(path_workspace)
        self.data = TreeDict(self._load_configs(self.path_user))
        self.data['__WORKSPACE__'] = TreeDict(
            self._load_configs(self.path_workspace))

    def _path_config_file(self, path):
        from dxpy.filesystem import Path
        from dxpy.filesystem import Directory, File
        if path is None:
            return None
        filename = Path(path)
        if self.module_name is not None and Directory(filename).exists:
            possible_suffix = ['', '.yml', '.yaml', '.json']
            for sfx in possible_suffix:
                name = '{0}{1}'.format(self.module_name, sfx)
                if File(filename / name).exists:
                    filename = filename / name
                    break
        return Path(filename).abs

    def _load_configs(self, path):
        if path is None:
            return dict()
        with open(path) as fin:
            return yaml.load(fin)

    def get_config(self):
        return self.data.get(['__WORKSPACE__'])    

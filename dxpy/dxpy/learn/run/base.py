class DxlnRunEnvrionment:
    def __init__(self, config_file_name='dxln.yml'):
        self._config = config_file_name
        pass

    def __enter__(self):
        from dxpy.learn.utils.general import pre_work, load_yaml_config
        load_yaml_config(self._config)
        # pre_work()
        return self

    def __exit__(self, type, value, trackback):
        pass

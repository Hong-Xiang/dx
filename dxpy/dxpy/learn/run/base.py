class DxlnRunEnvrionment:
    def __init__(self, config_file_name='dxln.yml', with_pre_work=False):
        self._config = config_file_name
        self._with_pre_work = with_pre_work
        pass

    def __enter__(self):
        from dxpy.learn.utils.general import pre_work, load_yaml_config
        load_yaml_config(self._config)
        if self._with_pre_work:
            pre_work()
        return self

    def __exit__(self, type, value, trackback):
        pass

default_engine = None


class MatlabEngine:
    def __init__(self):
        self.eng = None
        self.pre = None

    def __enter__(self):
        global default_engine
        import matlab.engine
        import os
        from dxpy.core.path import Path
        self.eng = matlab.engine.start_matlab()
        path_dxmat = os.environ['PATH_DXL_DXMAT']
        path_gen = Path(path_dxmat) / 'phantom'
        self.eng.addpath(str(path_gen))
        self.pre = default_engine
        default_engine = self.eng
        return self.eng

    def __exit__(self, type, value, trackback):
        global default_engine
        default_engine = self.pre
        self.eng.quit()

    @staticmethod
    def get_default_engine():
        return default_engine


def call_matlab_api(func):
    if MatlabEngine.get_default_engine() is None:
        with MatlabEngine() as eng:
            return func(eng)
    else:
        return func(MatlabEngine.get_default_engine())

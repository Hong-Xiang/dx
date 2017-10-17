from dxpy.filesystem.directory import Directory
class Save:
    def __init__(self, frequency, method):
        self.frequency = frequency
        self.method = method


class Load:
    def __init__(self, is_load, step):
        self.is_load = is_load
        self.step = step

class ModelDir(Directory):
    

class Serilization:
    def __init__(self, model_dir, is_load, load_step, save_freq, save_type, ckpt_name):
        self.model_dir = None,
        is_load = False,
        load_step = None,
        save_freq = 100,
        save_type = 'time',
        ckpt_name = 'model.ckpt',

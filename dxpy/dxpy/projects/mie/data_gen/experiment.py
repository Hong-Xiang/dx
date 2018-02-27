import typing as tp
from ..config import DEFAULT_CONFIG_FILENAME
import ruamel.yaml
yaml = ruamel.yaml.YAML()


class Crystal:
    def __init__(self):
        pass

    def make_mac(self)->str:
        """
        return str for Geometry.mac
        """
        pass


class CrystalCubic(Crystal):
    yaml_tag = '!cubic_crystal'

    def __init__(self, hx, hy, hz, cx=.0, cy=.0, cz=.0, rx=0.0, ry=0.0, rz=0.0):
        self.hx = hx
        self.hy = hy
        self.hz = hz
        self.cx = cx
        self.cy = cy
        self.cz = cz
        self.rx = rx
        self.ry = ry
        self.rz = rz

    def __str__(self):
        from io import StringIO
        output = StringIO()
        yaml.dump(self, output)
        return output.getvalue()

    @classmethod
    def to_yaml(cls, representer, data):
        return representer.represent_mapping(cls.yaml_tag,
                                             {'hx': data.hx, 'hy': data.hy, 'hz': data.hz,
                                              'cx': data.cx, 'cy': data.cy, 'cz': data.cz,
                                              'rx': data.rx, 'ry': data.ry, 'rz': data.rz})

    @classmethod
    def from_yaml(cls, constructor, node):
        return cls(*node.value)


yaml.register_class(CrystalCubic)


class Experiment:
    def __init__(self):
        self.crystal_shape = None
        self.source = None
        self.surface = None
        self.detectors = None
        self.nb_runs = None
        self.target_path = None

    def _make_data_processing(self):
        pass

    def make(self):
        """
        Generate all files needed to run experiment and data processing.
        """
        pass

    def load_yml(self, filename=DEFAULT_CONFIG_FILENAME):
        """
        Load configurations from .yml.
        """
        import yaml
        with open(filename, 'r') as fin:
            cfg = yaml.load(fin)
        self.crystal_shape = cfg.get('shape', self.crystal_shape)

        pass

from fs.osfs import OSFS
from .path import Path
from .fsauto import FileSystemAuto


class File:
    def __init__(self, path, filesystem=None):
        self.path = Path(path)
        self.fs = filesystem

    def exists(self) -> bool:
        with FileSystemAuto(self.fs) as fs:
            return fs.exists(self.path.s) and fs.isfile(self.path.s)

    def load(self):
        if not self.exists():
            raise FileNotFoundError(self.path.abs)
        if depth == 0:
            return
        with FS(self.fs) as fs:
            with fs.open(self.path.abs, 'rb') as fin:
                self.contents = fin.read()

    def save(self, data):
        with FS(self.fs) as fs:
            with fs.open(self.path.abs, 'wb') as fout:
                self.contents = fout.write(data)

    def to_serializable(self):
        try:
            cont = self.contents.decode() if self.contents else None
        except UnicodeDecodeError:
            cont = '!!binary' + str(self.contents)
        return {'path': self.path.abs,
                'name': self.path.name,
                'is_dir': False,
                'contents': cont}

    def __str__(self):
        import json
        return json.dumps(self.to_serializable(), sort_keys=True, separators=(',', ':'), indent=4)

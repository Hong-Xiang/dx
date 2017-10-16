from fs.osfs import OSFS
from ..exceptions import DirectoryNotFoundError
from ..path.model import Path
from ..file.model import File


class Directory:
    def __init__(self, path, load_depth=0):
        self.path = Path(path)
        if load_depth > 0:
            self.load(load_depth)
        else:
            self.children = None

    def load(self, depth):
        self.children = None
        if depth < 0:
            return
        if not self.exists:
            raise DirectoryNotFoundError(self.path.abs)
        if depth == 0:
            return
        self.children = []
        with OSFS('/') as fs:
            for f in fs.listdir(self.path.rel):
                fp = self.path / f
                if fs.isdir(fp.rel):
                    self.children.append(Directory(fp, depth - 1))
                else:
                    self.children.append(File(fp, 0))

    @property
    def exists(self):
        with OSFS('/') as fs:
            return fs.exists(self.path.rel)

    def to_serializable(self):
        return {'path': self.path.abs,
                'name': self.path.name,
                'is_dir': True,
                'children': [c.to_serializable() for c in self.children] if self.children is not None else None
                }

    def __str__(self):
        import json
        return json.dumps(self.to_serializable(), sort_keys=True, separators=(',', ':'), indent=4)

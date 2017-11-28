import fs.path as fp


class Path:
    """
    Properties returns simple and basic types: str or bool
    """

    def __init__(self, path, ptype=None):
        """
        Args:
            path: any object which is convertable to Path, including:
                str: raw path, url path, 
        """
        self._path = fp.normpath(str(path))

    def __str__(self):
        return self._path

    @property
    def raw(self):
        return self._path

    @property
    def abs(self):
        return fp.abspath(self._path)

    @property
    def rel(self):
        return fp.relpath(self._path)

    @property
    def is_abs(self):
        return fp.isabs(self._path)

    @property
    def basename(self):
        return fp.basename(self._path)

    @property
    def suffix(self):
        return fp.splitext(self._path)[1]

    def parts(self):
        result = tuple(fp.iteratepath(self._path))
        slash = fp.abspath('x')[:-1]
        if self.is_abs and result[0] != slash:
            result = tuple([slash] + list(result))
        return result

    def parent(self):
        return Path(fp.dirname(self._path))

    def __truediv__(self, name):
        return Path(fp.combine(self._path, name))

    def __add__(self, suffix):
        return Path(self._path + suffix)

    def __eq__(self, path):
        return self._path == str(Path(path))

    def __hash__(self):
        return hash(self._path)

from fs import path as fp
from typing import Tuple


class Path:
    """ Unified path for posix/windows/url/url_quoted paths.
    For the purpose of unified process, %,: and @ are preserved, please make sure there is not such characters in raw path.
    This class is an 'abstract' path object, which means it only normalize its representation for different platform,
    and provide functionalities of pure path calculations, without any relation to the true file system.
    Thus this class does **NOT** provide methods like `exists()` or `is_dir()`, please refer `dxpy.file_syste.file.File` for these functions.
    """

    @classmethod
    def _divide_protocol(cls, p: str) -> (str, str):
        n = p.find('@')
        if n >= len(p) - 1:
            return p[:], ''
        if n == -1:
            return None, p
        else:
            return p[:n + 1], p[n + 1:]

    @classmethod
    def _decode_url(self, p: str):
        from urllib.parse import unquote_plus
        return unquote_plus(unquote_plus(p))

    @classmethod
    def _unified_path(cls, p) -> str:
        if isinstance(p, Path):
            return p._p
        if not isinstance(p, str):
            raise TypeError(
                "{} is not convertable to {}.".format(type(p), __class__))
        protocol, raw_path = cls._divide_protocol(p)
        raw_path = cls._decode_url(raw_path)
        raw_path = fp.normpath(raw_path)
        if protocol is None:
            return raw_path
        return protocol + raw_path

    @classmethod
    def _unified_protocol(cls, p: str) -> str:
        if not p.endswith('@'):
            return p + '@'
        return p

    def __init__(self, path, protocol=None):
        if protocol is not None:
            path = self._unified_protocol(protocol)
        self._p = self._unified_path(path)

    @property
    def protocol(self) -> str:
        return self._divide_protocol(self._p)[0]

    @property
    def raw(self) -> str:
        return self._divide_protocol(self._p)[1]

    def raw_path(self) -> 'Path':
        return Path(self.raw, self.protocol)

    @property
    def s(self) -> str:
        "Alias of self.raw_path"
        return self.raw

    @property
    def a(self) -> str:
        return fp.abspath(self.s)

    def absolute(self) -> 'Path':
        return Path(self.a, self.protocol)

    @property
    def r(self) -> str:
        return fp.relpath(self.s)

    def relative(self) -> 'Path':
        return Path(self.r, self.protocol)

    def is_root(self) -> bool:
        return self.s == '/'

    def is_absolute(self) -> bool:
        return fp.isabs(self.s)

    def is_relative(self) -> bool:
        return not self.is_absolute()

    @property
    def n(self) -> str:
        return fp.basename(self.s)

    def name(self) -> 'Path':
        return Path(self.n, self.protocol)

    @property
    def extension_name(self) -> str:
        return fp.splitext(self.s)[1]

    @property
    def e(self) -> str:
        return self.extension_name

    @property
    def f(self) -> str:
        return fp.dirname(self.s)

    def father(self) -> 'Path':
        return Path(self.f, self.protocol)

    def parts(self) -> Tuple[str]:
        result = list(fp.iteratepath(self.s))
        if self.is_absolute():
            result = ['/'] + result
        return tuple(result)

    def join(self, name):
        return Path(fp.combine(self.s, name), self.protocol)

    def __truediv__(self, name):
        return self.join(name)

    def __add__(self, suffix):
        return Path(self.s + suffix, self.protocol)

    def __str__(self):
        return self._p

    def __hash__(self):
        return hash(self._p)

    def __eq__(self, path):
        return self._p == Path(path)._p

    def regex_match(self, pattern: str, is_ignore_extension=False) -> bool:
        raise NotImplementedError

    def unix_match(self, pattern: str, is_ignore_extension=False) -> bool:
        raise NotImplementedError

    def url_safe_path(self, with_protocol=False) -> str:
        from urllib.parse import quote_plus
        result = quote_plus(quote_plus(self.s))
        if with_protocol:
            return self.protocol + result
        return result

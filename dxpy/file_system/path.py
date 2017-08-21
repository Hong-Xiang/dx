import pathlib
import urllib
from functools import wraps


class PathError(Exception):
    pass


class NonePathError(PathError, TypeError):
    pass


class NotUrlPathError(PathError, ValueError):
    pass


class NotPurePathError(PathError, ValueError):
    pass


class NotValidPathError(PathError, ValueError):
    pass


def _is_url_path(path, is_strict=False):
    if not isinstance(path, str):
        raise TypeError
    if '/' in path and not "%252F" in path:
        return False
    if not '/' in path and "%252F" in path:
        return True
    if not '/' in path and not "%252F" in path:
        return not is_strict
    raise NotValidPathError(path)


def _url_quote(path):
    if _is_url_path(path, is_strict=True):
        raise NotPurePathError(path)
    qpath = urllib.parse.quote_plus(str(pathlib.Path(path).absolute()))
    qqpath = urllib.parse.quote_plus(qpath)
    return qqpath


def _url_unquote(path_url):
    if not _is_url_path(path_url):
        raise NotUrlPathError
    qpath = urllib.parse.unquote_plus(path_url)
    path = urllib.parse.unquote_plus(qpath)
    return path

# TODO: Add str path warper
# def path_str_support(func):
#     @warps(func)
#     def warper(path, )


class Path:
    """ Path warper for posix/windows/url paths.
    This class is an 'abstract' path object, which means it only normalize its representation for different platform,
    but there is not any relation to the true file system. Thus this class does **NOT** provide methods like `exists()` or
    `is_dir()`, please refer `dxpy.file_syste.file.File` for these functions.
    """

    def __init__(self, path, is_url_path=None, ):
        """
        -`is_url_path`: a bool to specify if given path is a url path. Default is `None` which requires automatic determination.
        """
        if isinstance(path, Path):
            self.path = path.path
            return
        if path is None:
            raise NotValidPathError
        if is_url_path is None:
            is_url_path = _is_url_path(path)
        if is_url_path:
            self.path = pathlib.Path(_url_unquote(path)).absolute()
        else:
            self.path = pathlib.Path(path).absolute()

    def __str__(self):
        return '<dxpy.file_system.path.Path object with path: {abs}>'.format(abs=self.abs)

    def parts(self):
        return self.path.parts

    @property
    def parent(self):
        return Path(self.path.parent, is_url_path=False).abs

    @property
    def name(self):
        return self.path.name

    @property
    def url(self):
        return _url_quote(self.abs)

    @property
    def abs(self):
        return str(self.path.absolute())

    @property
    def suffix(self):
        return self.path.suffix

    def check_exists(self, file_system):
        return file_system.exists(self.path)

    @property
    def brief(self):
        return {
            'name': self.name,
            'path': self.abs
        }

    @property
    def detail(self):
        result = self.brief
        result.update({
            'parent': self.parent,
            'url': self.url,
            'suffix': self.suffix,
            'parts': self.parts()
        })
        return result

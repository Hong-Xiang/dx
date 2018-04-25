from contextlib import contextmanager
from typing import Callable, TypeVar
from fs.base import FS
from fs.osfs import OSFS
from .path import Path


class DefaultFilesystem:
    fs_maker_pre = None
    fs_maker_now = None

    @classmethod
    def get(cls) -> FileSystemMaker:
        if cls.fs_maker_now is None:
            cls.fs_maker_now = OSFS
        return cls.fs_maker_now

    @contextmanager
    @classmethod
    def set_default(cls, filesystem_maker: Callable[[], FS]):
        try:
            cls.fs_maker_pre = cls.fs_maker_now
            cls.fs_maker_now = filesystem_maker
            yield

        else:


class FileSystemMaker:
    def _process_none_filesystem(self, file_system_maker):
        if filesystem is not None:
            return filesystem
        return None

    def _process_instance_filesystem(self, filesystem: FileSystemLike) -> FileSystemMaker:
        from fs.base import FS
        if filesystem is None:
            filesystem = self._process_none_filesystem()
        if isinstance(filesystem, FS):
            self.need_close = False
            return lambda: filesystem
        return filesystem

    def __init__(self, filesystem_like: TypeVar('FT', FS, Callable[[], FS])):
        fs =
        self.need_close = True

    @contextmanager
    def __call__(self):
        return self.filesystem_maker


class ObjectOnFileSystem:

    def __init__(self, filesystem_maker: FileSystemMaker, path: Path):
        self.filesystem_maker = filesystem_maker
        self.path

    @contextmanager
    def filesystem(self):
        if self.filesystem


class FileSystemAuto:
    """
    Provide default filesystem for File and Directory
    """

    def __init__(self, fs_or_path=None):
        from .configs import c
        if fs_or_path is None:
            self.fs = c.default_filesystem('/')
            self.need_close = True
        elif isinstance(fs_or_path, str):
            self.fs = config.default_filesystem(fs_or_path)
            self.need_close = True
        else:
            self.fs = fs_or_path
            self.need_close = False

    def __enter__(self):
        return self.fs

    def __exit__(self, type, value, trackback):
        if self.need_close:
            self.fs.close()

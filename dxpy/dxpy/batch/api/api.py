class FilesAPI:
    from . import service

    def __init__(self, fs, filters):
        self.fs = fs
        self.filters = filters

    @classmethod
    def ls(fs, filters, show_size=False):
        """
        List all files matches filters, show their properties.
        """
        pass

    @classmethod
    def merge(fs, filters, target=None, method=None):
        """
        Merge all files matches filters into one.
        """
        pass

    @classmethod
    def map(fs, filters, callback, args, kwargs):
        """
        Map callback to files like:
            for f in valid_files:
                callback(*args, filename=f, **kwargs)
        """
        pass

    @classmethod
    def clear(fs, filters):
        pass


class DirsAPI:
    @classmethod
    def ls(fs, filters, show_size=False):
        """
        List all files matches filters, show their properties.
        """
        pass

    @classmethod
    def merge(cls, fs, filters, target=None, is_check=True, is_auto_rename=True, rename_pattern=r'{name}.{id}.{suffix}'):
        """
        Merge directories, provide check, auto rename options.
        """
        pass

    @classmethod
    def clear(fs, filters):
        pass

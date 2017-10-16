import rx


def map_file(fs, filter, callback, dryrun):
    pass


def map_directory(fs, filter, callback, dryrun):
    pass


class Mapper:
    def __init__(self, fs, filter):
        self.fs = fs
        self.filter = filter

    def ls(self, infos=None):
        # TODO convert to true observalbes
        infos = infos or []
        paths = self.filter.get_list(self.fs)
        result_dct = {'path': paths}
        for k in infos:
            if 'size' == k:
                sizes = [self.fs.getdetails(p).size for p in paths]
                result_dct.update({'size': sizes})
        results = zip(*(result_dct[k] for k in result_dct))
        return rx.Observable.from_(results)


class Reducer:
    @classmethod
    def cat(cls, files):
        """
        Inputs:
            files: a list/observable of File.
        """
        pass

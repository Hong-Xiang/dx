import rx


class Mapper:
    def __init__(self, fs, filters, silent):
        self.fs = fs
        self.filter = filters

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
        # return rx.Observable.from_(results)
        return results

    def call(self, fs, callback):
        paths = self.filter.get_list(fs)
        for p in paths:
            callback(p)

    def broadcast(self, fs, dirs):
        # TODO: Implementation
        for d in dirs:
            if not fs.exists(d):
                fs.makedirs(d)
            elif not fs.isdir(d):
                pass


class Reducer:
    @classmethod
    def cat(cls, files):
        """
        Inputs:
            files: a list/observable of File.
        """
        pass

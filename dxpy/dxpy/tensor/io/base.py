from dxpy.core.path import Path


class TensorSpec:
    def __init__(self, path='data', shape=None, dtype=None, chunks=None):
        self._path = Path(path)
        self.shape = shape
        self.dtype = dtype
        self.chunks = chunks

    @property
    def dataset(self):
        return self._path.basename

    @property
    def groups(self):
        return self._path.parts()[:-1]

    def get_group(self, h5py_file, *, restrict=False):
        ds = h5py_file
        for g in self.groups:
            if restrict:
                ds = ds[g]
            else:
                ds = ds.require_group(g)
        return ds

    def create_dateset(self, h5py_file, data=None):
        gp = self.get_group(h5py_file)
        if data is None:
            return gp.create_dateset(self.dataset, shape=self.shape, dtype=self.dtype, chunks=chunks)
        else:
            return gp.create_dataset(self.dataset, data=data)

    def get_dataset(self, h5py_file):
        gp = self.get_group(h5py_file)
        return gp[self.basename]

class Tensor:
    def __init__(self, ):
        pass

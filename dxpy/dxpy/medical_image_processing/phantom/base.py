class PhantomSpec:
    def __init__(self, shape):
        self._shape = shape

    @property
    def shape(self):
        return self._shape


class Phantom2DSpec(PhantomSpec):
    ndim = 2

    def __init__(self, shape):
        super().__init__(shape)


class Phantom3DSpec(PhantomSpec):
    ndim = 3

    def __init__(self, shape):
        super().__init__(shape)

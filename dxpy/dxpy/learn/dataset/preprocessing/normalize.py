from ...graph import Graph


class Normalizer(Graph):
    def __init__(self, name):
        super(__class__, name)
        self.register_main_task(self._normalization)

    def _normalization_kernel(self, feeds):
        raise NotImplementedError

    def _normalization(self, feeds):
        if isinstance(feeds, dict):
            result = {}
            for k in feeds:
                result[k] = self._normalization_kernel(feeds[k])
            return result
        return self._normalization_kernel(feeds)


class FixWhite(Normalizer):
    def __init__(self, name):
        super(__class__, name)

    def _normalization_kernel(self, feeds):
        return (data - self.c['mean']) / self.c['std']

    def normalization(self, feeds):
            return result
        if isinstance(feeds, (np.ndarray, tf.Tensor)):
            return self._white_kernel(feeds, self.c['mean'], self.c['std'])

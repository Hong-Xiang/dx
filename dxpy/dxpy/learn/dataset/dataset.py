from ..model.base import Net


class Dataset(Net):
    """
    Subnet for loading datasets.
    """

    def __init__(self, name, config):
        super(__class__, name).__init__(self, config)

    def run(self, session, task, feeds):
        pass

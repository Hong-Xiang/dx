"""
Metrics of many samples
"""


def mean_square_error(labels, targets):
    from .transform import unbatch
    from .metrics import mean_square_error as msem
    labels = unbatch(labels)
    targets = unbatch(targets)
    results = [msem(msem) for l, t in zip(labels, targets)]
    return results


def analysis(labels, targets=None, *, stats=('mean_square_error',)):
    pass


def get_stats(name):
    if name.lower() in ['mean_square_error', 'mse']:
        return mean_square_error

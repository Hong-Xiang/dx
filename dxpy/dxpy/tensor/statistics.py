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

def stat(tensor):
    import numpy as np
    return {'min': np.min(tensor), 'max': np.max(tensor), 'mean': np.mean(tensor), 'std': np.std(tensor), 'shape': list(tensor.shape)}

def compare(label, target):
    from .metrics import rmse, psnr, ssim
    return rmse(label, target), psnr(label, target), ssim(label, target)
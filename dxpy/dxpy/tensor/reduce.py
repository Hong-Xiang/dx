def profile(tensor, sample_points, **kwargs):
    import numpy as np
    from scipy.interpolate import griddata
    from .mesh import linspace
    xis = [linspace(0, s, s, method='mid') for s in tensor.shape]
    grids = np.meshgrid(*xis)
    grids = np.array([g.flatten() for g in grids]).T
    values = griddata(grids, tensor.flatten(), sample_points, **kwargs)
    return values


def profile_h(tensor, y, num=None, **kwargs):
    import numpy as np
    from .mesh import linspace
    if num is None:
        num = tensor.shape[0]
    x = linspace(0, tensor.shape[0], num, method='mid')
    y = np.ones(x.shape) * y
    return profile(tensor, (x, y)), (x, y)

def profile_v(tensor, x, num=None, **kwargs):
    import numpy as np
    from .mesh import linspace
    if num is None:
        num = tensor.shape[0]
    y = linspace(0, tensor.shape[0], num, method='mid')
    x = np.ones(y.shape) * x
    return profile(tensor, (x, y)), (x, y)

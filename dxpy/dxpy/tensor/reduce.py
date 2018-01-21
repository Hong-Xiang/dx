def profile(tensor, sample_points, **kwargs):
    import numpy as np
    from scipy.interpolate import griddata
    from .mesh import linspace
    xis = [linspace(0, s, s, method='mid') for s in tensor.shape]
    grids = np.meshgrid(*xis)
    grids = np.array([g.flatten() for g in grids]).T
    values = griddata(grids, tensor.flatten(), sample_points, **kwargs)
    return values 

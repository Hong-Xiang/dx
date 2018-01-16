import numpy as np
from typing import TypeVar


def _create_2d_ndarray(images, shape=None):
    if shape is None:
        shape = images.shape[:2]
    result = np.empty(shape[:2], np.ndarray)
    if isinstance(images, np.ndarray):
        images = images.tolist()
    for i in range(shape[0]):
        for j in range(shape[1]):
            if images[i] is None or images[i][j] is None:
                result[i, j] = None
            else:
                result[i, j] = np.array(images[i][j])
    return result


def _handle_list_inputs(images, error):
    if isinstance(images, (list, tuple)):
        types = {type(im) for im in images}
        types.discard(None)
        if len(types) > 1:
            raise TypeError('images have different types: {}.'.format(types))
        types = list(types)
        if types[0] == np.ndarray:
            nc = min([im.shape[0] for im in images if im is not None])
        elif types[0] in (list, tuple):
            nc = min([len(im) for im in images if im is not None])
        else:
            raise TypeError("Type {} not supported.".format(types[0]))
        nr = len(images)
        return _create_2d_ndarray(images, [nr, nc])
    else:
        raise error


def _unified_images(images, invert_row_column):
    try:
        images = np.array(images)
    except ValueError as e:
        images = _handle_list_inputs(images, e)
    if images.ndim == 1:
        images = _handle_list_inputs(images.tolist(), ValueError(
            "Failed to analysis, hint: images.dim==1."))
    if images.ndim > 2:
        images = _create_2d_ndarray(images)
    if invert_row_column:
        images = np.moveaxis(images, 1, 0)
    # Unified array to 2 dimension
    for ir in range(images.shape[0]):
        for ic in range(images.shape[1]):
            t = images[ir, ic]
            if t is None:
                continue
            if t.ndim == 2:
                continue
            if t.ndim == 3 and t.shape[-1] == 3:
                continue
            if t.ndim == 4:
                # Case [1, M, N, 1]
                if t.shape[0] == 1 and t.shape[3] == 1:
                    images[ir, ic] = t[0, :, :, 0]
                    continue
                # Case [1, M, N, 3]
                if t.shape[0] == 1 and t.shape[3] == 3:
                    images[ir, ic] = t[0, :, :, :]
                    continue
            elif t.ndim == 3:
                # Case [M, N, 1]
                if t.shape[-1] == 1:
                    images[ir, ic] = t[:, :, 0]
                    continue
                # Case [1, M, N]
                if t.shape[0] == 1:
                    images[ir, ic] = t[0, :, :]
                    continue
            raise ValueError(
                'Invalid images[{}, {}] with shape {}.'.format(ir, ic, t.shape))
    return images


def _auto_windows(images, windows):
    windows = np.zeros(list(images.shape) + [2])
    for i in range(images.shape[0]):
        for j in range(images.shape[1]):
            if images[i, j] is None:
                windows[i, j] = np.nan
            windows[i, j, 0] = np.min(images[i, j])
            windows[i, j, 1] = np.max(images[i, j])
    return windows


def _unified_windows(images, windows):
    if windows is None:
        return _auto_windows(images, windows)
    windows = np.array(windows)
    if windows.ndim < 3:
        windows = np.reshape(
            windows, [1] * (3 - windows.ndim) + list(windows.shape))
    # Force broadcast windows shape to [R,C,2]
    dummy_zero = np.zeros(list(images.shape[:2]) + [2])
    windows = windows + dummy_zero
    return windows


def _adjust_images_to_fit_nb_columns(images, windows, max_columns=None, max_rows=None):
    """
    images: np.array of shape [R, C]
    windows: np.array of shape [R, C, 2]
    """
    if not images.shape == windows.shape[:2]:
        raise ValueError("Images shape {} and windows shape {} not consist.".format(
            images.shape, windows.shape))
    nb_row_pre, nb_column_pre = images.shape
    if max_columns is not None and nb_column_pre > max_columns:
        nb_ratio = np.ceil(double(nb_column_pre) / max_columns)
        nb_row = nb_row_pre * nb_ratio
        new_images = np.empty([nb_row, max_columns], np.ndarray)
        new_windows = np.empty([nb_row, max_columns, 2], np.ndarray)
        for i in range(nb_ratio):
            r_s, r_e = (i * nb_row_pre, (i + 1) * nb_row_pre)
            c_s, c_e = (i * max_columns,
                        min((i + 1) * max_columns, nb_column_pre))
            new_images[r_s: r_e, :] = images[:, c_s: c_e]
            new_windows[r_s: r_e, :, :] = windows[:, c_s: c_e, :]
        images = new_images
        windows = new_windows
    if max_rows is not None and images.shape[0] > max_rows:
        images = images[:max_rows, :]
        windows = windows[:max_rows, :]
    return images, windows


def _adjust_figure_size(images, scale, scale_factor):
    # Default scale: 10: 100
    width = 0.0
    height = 0.0
    nb_images = 0
    for ir in range(images.shape[0]):
        for ic in range(images.shape[1]):
            if images[ir, ic] is None:
                continue
            width += images[ir, ic].shape[1]
            height += images[ir, ic].shape[0]
            nb_images += 1
    width = width / nb_images * images.shape[1]
    height = height / nb_images * images.shape[0]
    DEFAULT_WIDTH = scale_factor * scale
    ratio = DEFAULT_WIDTH / width
    height = height * ratio
    return (DEFAULT_WIDTH, height), 100.0 
    # return (images.shape[1] + 1, images.shape[0] + 1), 640.0 / (images.shape[1] + 1)


def grid_view(images, windows=None, scale=1.0, cmap=None,
              *,
              max_columns=None, max_rows=None,
              hide_axis=True,
              hspace=0.1, wspace=0.1, return_figure=False, dpi=None, adjust_figure_size=True, save_filename=None,
              invert_row_column=False,
              scale_factor=2.0,
              _top=None,
              _right=None):
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    from matplotlib.figure import SubplotParams
    """ subplot list of images of multiple categories into grid subplots

    Args:
        image_lists: list of [list of images or 4D tensor]
        windows: list of windows
        nb_column: columns of images
    Returns:
        Return figure if return_figure is true, else None.
    """
    images = _unified_images(images, invert_row_column)
    windows = _unified_windows(images, windows)
    images, windows = _adjust_images_to_fit_nb_columns(images, windows,
                                                       max_columns, max_rows)
    figsize, default_dpi = _adjust_figure_size(images, scale, scale_factor)
    from dxpy.debug.utils import dbgmsg
    dbgmsg(figsize, default_dpi)
    dbgmsg(images.shape)
    if dpi is None:
        dpi = default_dpi
    dpi = dpi * scale
    fig = plt.figure(figsize=figsize, dpi=dpi,
                     subplotpars=SubplotParams(left=0.0, right=1.0, bottom=0.0, top=1.0, wspace=0.0, hspace=0.0))
    # fig.subplots_adjust(hspace=hspace, wspace=wspace)
    nr, nc = images.shape
    if _top is None:
        # _top = figsize[1] / nr * nc
        _top = scale
    if _right is None:
        _right = figsize[0] / nc * nr
        _right = scale
    gs = gridspec.GridSpec(nr, nc,
                           wspace=wspace, hspace=hspace,
                           top=_top, bottom=0.0,
                           left=0.0, right=_right)
    for ir in range(nr):
        for ic in range(nc):
            if images[ir, ic] is None:
                continue
            # ax = plt.subplot(nr, nc, ir * nc + ic + 1)
            ax = plt.subplot(gs[ir, ic])
            ax.imshow(images[ir, ic], cmap=cmap,
                      vmin=windows[ir, ic, 0], vmax=windows[ir, ic, 1])
            if hide_axis:
                plt.axis('off')
            else:
                ax.set_xticklabels([])
                ax.set_yticklabels([])
    if save_filename is not None:
        fig.savefig(save_filename)
    if return_figure:
        return fig

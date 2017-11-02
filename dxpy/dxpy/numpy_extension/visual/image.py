import matplotlib.pyplot as plt
import numpy as np
from .. import image as nei


def grid_view(image_lists, windows=None, nb_column=8, scale=2.0, cmap=None, *, hide_axis=False, tight_c=0.3):
    """ subplot list of images of multiple categories into grid subplots
    Args:
        images: tuple of list of images
    """
    nb_cata = len(image_lists)    
    image_lists = map(nei.try_unbatch, image_lists)
    image_lists = [list(map(nei.fix_dim, imgs)) for imgs in image_lists]
    nb_images = max([len(imgs) for imgs in image_lists])
    nb_row = np.ceil(nb_images / nb_column) * nb_cata
    fig = plt.figure(figsize=(nb_column * scale, nb_row * scale))
    if windows is None:
        windows = [(None, None)] * nb_cata
    for k in range(nb_cata):
        for i in range(nb_images):
            if i > len(image_lists[k]):
                continue
            r = i // nb_column * nb_cata + k
            c = i % nb_column
            ax = plt.subplot(nb_row, nb_column, r * nb_column + c + 1)            
            plt.imshow(image_lists[k][i], cmap=cmap,
                       vmin=windows[k][0], vmax=windows[k][1])
            if hide_axis:
                ax.get_xaxis().set_visible(False)
                ax.get_yaxis().set_visible(False)
    plt.tight_layout(tight_c)
    return fig

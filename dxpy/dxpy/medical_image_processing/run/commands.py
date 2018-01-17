import click


@click.command()
@click.option('--input', '-i', type=str)
@click.option('--output', '-o', type=str)
@click.option('--keys', '-k', type=(str, str), multiple=True)
@click.option('--phantom_shape', '-s', type=int, nargs=2)
@click.option('--sen_width', '-w', type=float)
@click.option('--method', '-m', type=str, default='FBP')
@click.option('--nb_iter', '-n', type=int, default=1)
def reconnpz(input, output, keys, phantom_shape, sen_width, method, nb_iter):
    import numpy as np
    from dxpy.tensor.io import load_npz
    from tqdm import tqdm
    from dxpy.tensor.collections import dict_element_to_tensor
    from dxpy.medical_image_processing.phantom import Phantom2DSpec
    from dxpy.medical_image_processing.projection.parallel import projection2d
    from dxpy.medical_image_processing.reconstruction.parallel import reconstruction2d
    from dxpy.medical_image_processing.detector.parallel import Detector2DParallelRing
    sinos = load_npz(input)
    result = dict()
    nb_imgs = None
    nb_sen = 0
    if len(keys) == 0:
        keys_input = list()
        keys_output = list()
        for k in sinos:
            if k.startswith('sino_'):
                keys_input.append(k)
                keys_output.append(k.replace('sino_', 'recon_'))
    else:
        keys_input, keys_output = tuple(zip(*keys))
    keys_mapped = dict()
    for ki, ko in zip(keys_input, keys_output):
        keys_mapped[ki] = ko
    for k in sinos:
        if k not in keys_input:
            continue
        if sinos[k].shape[2] > nb_sen:
            nb_sen = sinos[k].shape[2]
    for k in sinos:
        if k not in keys_input:
            result[k] = sinos[k]
            continue
        if nb_imgs is None:
            nb_imgs = sinos[k].shape[0]
        else:
            if not nb_imgs == sinos[k].shape[0]:
                raise ValueError("Invalid sinos shape.")
        phan_spec = Phantom2DSpec(shape=phantom_shape)
        sen_width_c = sen_width * nb_sen / sinos[k].shape[2]
        views = np.linspace(0, np.pi, sinos[k].shape[1], endpoint=False)
        detector = Detector2DParallelRing(nb_sensors=sinos[k].shape[2],
                                          sensor_width=sen_width_c,
                                          views=views)
        print('I: Reconstructing: {}.'.format(k))
        ko = keys_mapped[k]
        result[ko] = []
        for i in tqdm(range(nb_imgs)):
            recon = reconstruction2d(sinos[k][i, ...], detector, phan_spec,
                                     method=method,
                                     iterations=nb_iter)
            result[ko].append(recon)
    dict_element_to_tensor(result)
    np.savez(output, **result)

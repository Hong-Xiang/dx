import click


@click.command()
@click.option('--input', '-i', type=str)
@click.option('--output', '-o', type=str)
@click.option('--skip_keys', '-s', type=str)
@click.option('--phantom_x', '-x', type=int)
@click.option('--phantom_y', '-y', type=int)
@click.option('--sen_width', '-w', type=float)
@click.option('--method', '-m', type=str, default='FBP')
@click.option('--nb_iter', '-n', type=int, default=1)
def reconnpz(input, output, skip_keys, phantom_x, phantom_y, sen_width, method, nb_iter):
    import numpy as np
    from dxpy.tensor.io import load_npz
    from tqdm import tqdm
    from dxpy.medical_image_processing.phantom import Phantom2DSpec
    from dxpy.medical_image_processing.projection.parallel import projection2d
    from dxpy.medical_image_processing.reconstruction.parallel import reconstruction2d
    from dxpy.medical_image_processing.detector.parallel import Detector2DParallelRing
    sinos = load_npz(input)
    result = {k: [] for k in sinos}
    nb_imgs = None
    nb_sen = 0
    for k in sinos:
        if k == skip_keys:
            continue
        if sinos[k].shape[2] > nb_sen:
            nb_sen = sinos[k].shape[2]
    for k in sinos:
        if k == skip_keys:
            result[k] = sinos[k]
            continue
        if nb_imgs is None:
            nb_imgs = sinos[k].shape[0]
        else:
            if not nb_imgs == sinos[k].shape[0]:
                raise ValueError("Invalid sinos shape.")
        phan_spec = Phantom2DSpec(shape=[phantom_x, phantom_y])
        sen_width_c = sen_width * nb_sen / sinos[k].shape[2]
        views = np.linspace(0, np.pi, sinos[k].shape[1], endpoint=False)
        detector = Detector2DParallelRing(nb_sensors=sinos[k].shape[2],
                                          sensor_width=sen_width_c,
                                          views=views)
        print('I: Reconstructing: {}.'.format(k))
        for i in tqdm(range(nb_imgs)):
            recon = reconstruction2d(sinos[k][i, ...], detector, phan_spec,
                                     method=method,
                                     iterations=nb_iter)
            result[k].append(recon)
    for k in result:
        result[k] = np.array(result[k])
    np.savez(output, **result)

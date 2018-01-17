def npz2mat(input_filename, output_filename):
    from scipy.io import savemat
    from .io import load_npz
    savemat(output, load_npz(input_filename))


def list_npz(input_filename):
    import numpy as np
    data = np.load(input_filename)
    for k in data:
        print(k, data[k].shape)


def concatenate(filenames, output_filename):
    from .io import load_npz
    result = None
    for f in filenames:
        data = load_npz(f)
        if result is None:
            result = data
        else:
            for k in result:
                result[k] = np.concatenate([result[k], data[k]], axis=0)
    np.savez(output_filename, **result)

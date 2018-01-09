import click
from tqdm import tqdm


def infer_sino_sr(dataset, nb_samples, output):
    """
    Use network in current directory as input for inference
    """
    import tensorflow as tf
    from dxpy.learn.dataset.api import get_dataset
    from dxpy.learn.net.api import get_network
    from dxpy.configs import ConfigsView
    from dxpy.learn.config import config
    import numpy as np
    import yaml
    from dxpy.debug.utils import dbgmsg
    dbgmsg(dataset)
    data_raw = np.load(dataset)
    data_raw = {k: np.array(data_raw[k]) for k in data_raw.keys()}
    config_view = ConfigsView(config)

    def tensor_shape(key):
        shape_origin = data_raw[key].shape
        return [1] + list(shape_origin[1:3]) + [1]
    with tf.name_scope('inputs'):
        keys = ['input/image{}x'.format(2**i) for i in range(4)]
        keys += ['label/image{}x'.format(2**i) for i in range(4)]
        dataset = {k: tf.placeholder(
            tf.float32, tensor_shape(k)) for k in keys}

    network = get_network('network/srms', dataset=dataset)
    nb_down_sample = network.param('nb_down_sample')
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.train.MonitoredTrainingSession(
        checkpoint_dir='./save', config=config, save_checkpoint_secs=None)

    STAT_STD = 9.27
    STAT_MEAN = 9.76
    BASE_SHAPE = (640, 320)

    dataset_configs = config_view['dataset']['srms']
    with_noise = dataset_configs['with_poission_noise']
    if with_noise:
        PREFIX = 'input'
    else:
        PREFIX = 'label'

    def crop_sinogram(tensor, target_shape=None):
        if target_shape is None:
            target_shape = BASE_SHAPE
        if len(tensor.shape) == 4:
            tensor = tensor[0, :, :, 0]
        o1 = (tensor.shape[0] - target_shape[0]) // 2
        o2 = (tensor.shape[1] - target_shape[1]) // 2
        return tensor[o1:-o1, o2:-o2]

    def run_infer(idx):
        input_key = '{}/image{}x'.format(PREFIX, 2**nb_down_sample)
        low_sino = np.reshape(
            data_raw[input_key][idx, :, :], tensor_shape(input_key))
        low_sino = (low_sino - STAT_MEAN) / STAT_STD
        feeds = {dataset['input/image{}x'.format(2**nb_down_sample)]: low_sino}
        inf, itp = sess.run([network['outputs/inference'],
                             network['outputs/interp']], feed_dict=feeds)
        infc = crop_sinogram(inf)
        itpc = crop_sinogram(itp)
        infc = infc * STAT_STD + STAT_MEAN
        itpc = itpc * STAT_STD + STAT_MEAN
        return infc, itpc

    phans = []
    sino_highs = []
    sino_lows = []
    sino_itps = []
    sino_infs = []
    NB_MAX = data_raw['phantom'].shape[0]
    for idx in tqdm(range(nb_samples), ascii=True):
        if idx > NB_MAX:
            import sys
            print('Index {} out of range {}, stop running and store current result...'.format(
                idx, NB_MAX), file=sys.stderr)
            break

        phans.append(data_raw['phantom'][idx, ...])
        sino_highs.append(crop_sinogram(
            data_raw['{}/image1x'.format(PREFIX)][idx, :, :]))
        sino_lows.append(crop_sinogram(data_raw['{}/image{}x'.format(
            PREFIX, 2**nb_down_sample)][idx, ...], [s // (2**nb_down_sample) for s in BASE_SHAPE]))
        sino_inf, sino_itp = run_infer(idx)
        sino_infs.append(sino_inf)
        sino_itps.append(sino_itp)

    results = {'phantom': phans, 'sino_itps': sino_itps,
               'sino_infs': sino_infs, 'sino_highs': sino_highs, 'sino_lows': sino_lows}
    np.savez(output, **results)


def infer_phan_sr(dataset, nb_samples, output):
    """
    Use network in current directory as input for inference
    """
    import tensorflow as tf
    from dxpy.learn.dataset.api import get_dataset
    from dxpy.learn.net.api import get_network
    from dxpy.configs import ConfigsView
    from dxpy.learn.config import config
    import numpy as np
    import yaml
    from dxpy.debug.utils import dbgmsg
    print('Using dataset file:', dataset)
    data_raw = np.load(dataset)
    data_raw = {k: np.array(data_raw[k]) for k in data_raw.keys()}
    config_view = ConfigsView(config)

    dataset_configs = config_view['dataset']['srms']
    with_noise = dataset_configs['with_poission_noise']
    dbgmsg(with_noise)
    if with_noise:
        PREFIX = 'noise'
    else:
        PREFIX = 'clean'

    def data_key(nd):
        return '{}{}x'.format(PREFIX, 2**nd)

    def tensor_shape(key):
        shape_origin = data_raw[key].shape
        return [1] + list(shape_origin[1:3]) + [1]
    with tf.name_scope('inputs'):
        keys = ['input/image{}x'.format(2**i) for i in range(4)]
        keys += ['label/image{}x'.format(2**i) for i in range(4)]
        dataset = {k: tf.placeholder(tf.float32, tensor_shape(data_key(i % 4)))
                   for i, k in enumerate(keys)}

    network = get_network('network/srms', dataset=dataset)
    nb_down_sample = network.param('nb_down_sample')
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.train.MonitoredTrainingSession(
        checkpoint_dir='./save', config=config, save_checkpoint_secs=None)

    STAT_MEAN = 15.26 
    STAT_STD = 22.0 
    STAT_MEAN_LOW = 15.26 * (4.0**nb_down_sample)
    STAT_STD_LOW = 22.0 * (4.0**nb_down_sample)
    BASE_SHAPE = (256, 256)

    def crop_image(tensor, target_shape=None):
        if target_shape is None:
            target_shape = BASE_SHAPE
        if len(tensor.shape) == 4:
            tensor = tensor[0, :, :, 0]
        o1 = (tensor.shape[0] - target_shape[0]) // 2
        o2 = (tensor.shape[1] - target_shape[1]) // 2
        return tensor[o1:-o1, o2:-o2]

    input_key = data_key(nb_down_sample)
    dbgmsg('input_key:', input_key)

    def run_infer(idx):
        low_phan = np.reshape(
            data_raw[input_key][idx, :, :], tensor_shape(input_key))
        # low_phan = (low_phan - STAT_MEAN) / STAT_STD
        feeds = {dataset['input/image{}x'.format(2**nb_down_sample)]: low_phan}
        inf, itp = sess.run([network['outputs/inference'],
                             network['outputs/interp']], feed_dict=feeds)
        infc = crop_image(inf)
        itpc = crop_image(itp)
        infc = infc * STAT_STD_LOW + STAT_MEAN_LOW
        itpc = itpc * STAT_STD_LOW + STAT_MEAN_LOW
        return infc, itpc

    phans = []
    img_highs = []
    img_lows = []
    img_itps = []
    img_infs = []
    NB_MAX = data_raw['phantom'].shape[0]
    for idx in tqdm(range(nb_samples), ascii=True):
        if idx > NB_MAX:
            import sys
            print('Index {} out of range {}, stop running and store current result...'.format(
                idx, NB_MAX), file=sys.stderr)
            break

        phans.append(data_raw['phantom'][idx, ...])
        img_high = crop_image(data_raw[data_key(0)][idx, :, :])
        img_high = img_high * STAT_STD + STAT_MEAN
        # img_high = img_high * STAT_STD / \
        # (4.0**nb_down_sample) + STAT_MEAN / (4.0**nb_down_sample)
        img_highs.append(img_high)
        img_low = crop_image(data_raw[data_key(nb_down_sample)][idx, ...],
                             [s // (2**nb_down_sample) for s in BASE_SHAPE])
        img_low = img_low * STAT_STD_LOW + STAT_MEAN_LOW
        img_lows.append(img_low)
        img_inf, img_itp = run_infer(idx)
        img_infs.append(img_inf)
        img_itps.append(img_itp)
    
    img_highs = np.array(img_highs)
    img_infs = np.array(img_infs) / (4.0**nb_down_sample)
    img_itps = np.array(img_itps) / (4.0**nb_down_sample)
    img_lows = np.array(img_lows) / (4.0**nb_down_sample)

    results = {'phantom': phans, 'img_itps': img_itps,
               'img_infs': img_infs, 'img_highs': img_highs, 'img_lows': img_lows}
    np.savez(output, **results)


def infer_mct(dataset, nb_samples, output):
    """
    Use network in current directory as input for inference
    """
    import tensorflow as tf
    from dxpy.learn.dataset.api import get_dataset
    from dxpy.learn.net.api import get_network
    from dxpy.configs import ConfigsView
    from dxpy.learn.config import config
    import numpy as np
    import yaml
    from dxpy.debug.utils import dbgmsg
    print('Using dataset file:', dataset)
    data_raw = np.load(dataset)
    data_raw = {k: np.array(data_raw[k]) for k in data_raw.keys()}
    config_view = ConfigsView(config)

    def data_key(nd):
        return 'image{}x'.format(2**nd)

    def tensor_shape(key):
        shape_origin = data_raw[key].shape
        return [1] + list(shape_origin[1:3]) + [1]

    with tf.name_scope('inputs'):
        keys = ['input/image{}x'.format(2**i) for i in range(4)]
        keys += ['label/image{}x'.format(2**i) for i in range(4)]
        dataset = {k: tf.placeholder(tf.float32, tensor_shape(data_key(i % 4)))
                   for i, k in enumerate(keys)}

    network = get_network('network/srms', dataset=dataset)
    nb_down_sample = network.param('nb_down_sample')
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.train.MonitoredTrainingSession(
        checkpoint_dir='./save', config=config, save_checkpoint_secs=None)

    STAT_MEAN = 9.93 
    STAT_STD = 7.95
    STAT_MEAN_LOW = 9.93 * (4.0**nb_down_sample)
    STAT_STD_LOW = 7.95 * (4.0**nb_down_sample)
    BASE_SHAPE = (384, 384)

    def crop_image(tensor, target_shape=None):
        if target_shape is None:
            target_shape = BASE_SHAPE
        if len(tensor.shape) == 4:
            tensor = tensor[0, :, :, 0]
        # o1 = (tensor.shape[0] - target_shape[0]) // 2
        o1 = tensor.shape[0] // 2
        o2 = (tensor.shape[1] - target_shape[1]) // 2
        return tensor[o1:o1+target_shape[0], o2:-o2]

    input_key = data_key(nb_down_sample)
    dbgmsg('input_key:', input_key)

    def run_infer(idx):
        low_phan = np.reshape(
            data_raw[input_key][idx, :, :], tensor_shape(input_key))
        # low_phan = (low_phan - STAT_MEAN) / STAT_STD
        feeds = {dataset['input/image{}x'.format(2**nb_down_sample)]: low_phan}
        inf, itp = sess.run([network['outputs/inference'],
                             network['outputs/interp']], feed_dict=feeds)
        infc = crop_image(inf)
        itpc = crop_image(itp)
        infc = infc * STAT_STD_LOW + STAT_MEAN_LOW
        itpc = itpc * STAT_STD_LOW + STAT_MEAN_LOW
        return infc, itpc

    phans = []
    img_highs = []
    img_lows = []
    img_itps = []
    img_infs = []
    NB_MAX = data_raw['phantom'].shape[0]
    for idx in tqdm(range(nb_samples), ascii=True):
        if idx > NB_MAX:
            import sys
            print('Index {} out of range {}, stop running and store current result...'.format(
                idx, NB_MAX), file=sys.stderr)
            break

        phans.append(data_raw['phantom'][idx, ...])
        img_high = crop_image(data_raw[data_key(0)][idx, :, :])
        img_high = img_high * STAT_STD + STAT_MEAN
        # img_high = img_high * STAT_STD / \
        # (4.0**nb_down_sample) + STAT_MEAN / (4.0**nb_down_sample)
        img_highs.append(img_high)
        img_low = crop_image(data_raw[data_key(nb_down_sample)][idx, ...],
                             [s // (2**nb_down_sample) for s in BASE_SHAPE])
        img_low = img_low * STAT_STD_LOW + STAT_MEAN_LOW
        img_lows.append(img_low)
        img_inf, img_itp = run_infer(idx)
        img_infs.append(img_inf)
        img_itps.append(img_itp)
    
    img_highs = np.array(img_highs)
    img_infs = np.array(img_infs) / (4.0**nb_down_sample)
    img_itps = np.array(img_itps) / (4.0**nb_down_sample)
    img_lows = np.array(img_lows) / (4.0**nb_down_sample)

    results = {'phantom': phans, 'sino_itps': img_itps,
               'sino_infs': img_infs, 'sino_highs': img_highs, 'sino_lows': img_lows}
    np.savez(output, **results)

def recon_sino(sinograms_filename, nb_samples, output, recon_method):
    import numpy as np
    from dxpy.medical_image_processing.phantom import Phantom2DSpec
    from dxpy.medical_image_processing.reconstruction.parallel import reconstruction2d
    from dxpy.medical_image_processing.detector import Detector2DParallelRing
    sinograms = np.load(sinograms_filename)
    sino_highs = np.array(sinograms['sino_highs'])
    sino_lows = np.array(sinograms['sino_lows'])
    sino_infs = np.array(sinograms['sino_infs'])
    sino_itps = np.array(sinograms['sino_itps'])
    phans = np.array(sinograms['phantom'])
    nb_views_high = sino_highs.shape[1]
    nb_views_low = sino_lows.shape[1]
    nb_views_high //= 2
    nb_views_low //= 2
    sino_highs = sino_highs[:, :nb_views_high, :]
    sino_lows = sino_lows[:, :nb_views_low, :]
    sino_infs = sino_infs[:, :nb_views_high, :]
    sino_itps = sino_itps[:, :nb_views_high, :]
    sino_lows = sino_lows * nb_views_high**2 / (nb_views_low**2)
    phan_spec = Phantom2DSpec(shape=[256] * 2)
    detec_high = Detector2DParallelRing(views=np.linspace(
        0, np.pi, nb_views_high, endpoint=False), nb_sensors=nb_views_high, sensor_width=1.0)
    detec_low = Detector2DParallelRing(views=np.linspace(
        0, np.pi, nb_views_low, endpoint=False), nb_sensors=nb_views_low, sensor_width=1.0 * nb_views_high / nb_views_low)
    recon_highs = []
    recon_lows = []
    recon_infs = []
    recon_itps = []

    def recon_kernel(sinogram, detec):
        sinogram = np.maximum(sinogram, 0.0)
        if recon_method == 'fbp':
            recon = reconstruction2d(sinogram, detec, phan_spec)
        elif recon_method == 'sart':
            recon = reconstruction2d(
                sinogram, detec, phan_spec, method='SART_CUDA', iterations=100)
        recon = np.maximum(recon, 0.0)
        recon = recon / np.sum(recon) * 1e6
        return recon

    for i in tqdm(range(nb_samples), ascii=True):
        recon_highs.append(recon_kernel(sino_highs[i, ...], detec_high))
        recon_lows.append(recon_kernel(sino_lows[i, ...], detec_low))
        recon_infs.append(recon_kernel(sino_infs[i, ...], detec_high))
        recon_itps.append(recon_kernel(sino_itps[i, ...], detec_high))
    results = {'phantom': phans, 'recon_highs': recon_highs,
               'recon_lows': recon_lows, 'recon_infs': recon_infs, 'recon_itps': recon_itps}
    np.savez(output, **results)

def infer_mice(dataset, nb_samples, output):
    import numpy as np
    import tensorflow as tf
    from dxpy.learn.dataset.api import get_dataset
    from dxpy.learn.net.api import get_network
    from dxpy.learn.utils.general import load_yaml_config, pre_work
    from dxpy.learn.session import Session
    from dxpy.numpy_extension.visual import grid_view
    from tqdm import tqdm
    pre_work()
    input_data = np.load('/home/hongxwing/Workspace/NetInference/Mice/mice_test_data.npz')
    input_data = {k: np.array(input_data[k]) for k in input_data}
    dataset_origin = get_dataset('dataset/srms')
    is_low_dose = dataset_origin.param('low_dose')
    for k in input_data:
        print(k, input_data[k].shape)
    input_keys = ['input/image{}x'.format(2**i) for i in range(4)]
    label_keys = ['label/image{}x'.format(2**i) for i in range(4)]
    shapes = [[1]+list(input_data['clean/image{}x'.format(2**i)].shape)[1:]+[1] for i in range(4)]
    inputs = {input_keys[i]: tf.placeholder(tf.float32, shapes[i], name='input{}x'.format(2**i)) for i in range(4)}
    labels = {label_keys[i]: tf.placeholder(tf.float32, shapes[i], name='label{}x'.format(2**i)) for i in range(4)}
    dataset = dict(inputs)
    dataset.update(labels)
    network = get_network('network/srms', dataset=dataset)
    nb_down_sample = network.param('nb_down_sample')
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.train.MonitoredTrainingSession(
            checkpoint_dir='./save', config=config, save_checkpoint_secs=None)


    def get_feed(idx):
#     return dict()
        data_raw = input_data['clean/image{}x'.format(2**nb_down_sample)][idx, ...]
        data_raw = np.reshape(data_raw, [1]+list(data_raw.shape)+[1])
        data_label = input_data['clean/image1x'.format(2**nb_down_sample)][idx, ...]
        data_label = np.reshape(data_label, [1]+list(data_label.shape)+[1])
        return {dataset['input/image{}x'.format(2**nb_down_sample)]: data_raw,
                dataset['input/image1x'.format(2**nb_down_sample)]: data_label,
                dataset['label/image1x'.format(2**nb_down_sample)]: data_label,}
            
    to_run = {
        'inf': network['outputs/inference'], 
        'itp': network['outputs/interp'], 
        'high': network['input/image1x'],
    #     'li': network['outputs/loss_itp'],
    #     'ls': network['outputs/loss'],
    #     'la': network['outputs/aligned_label']
    }

    def crop(data, target):
        if len(data.shape) == 4:
            data = data[0, :, :, 0]
        o1 = data.shape[0]//2
        o2 = (data.shape[1] - target[1])//2
        return data[o1:o1+target[0], o2:-o2]

    
    MEAN = 100.0
    STD = 150.0
    if is_low_dose:
        MEAN /= dataset_origin.param('low_dose_ratio')
        STD /= dataset_origin.param('low_dose_ratio')
    NB_IMAGES = nb_samples

    def get_infer(idx):
        result = sess.run(to_run, feed_dict=get_feed(idx))
        inf = crop(result['inf'], [320, 64])
        itp = crop(result['itp'], [320, 64])
        high = crop(input_data['clean/image1x'][idx, ...], [320, 64])
        low = crop(input_data['clean/image{}x'.format(2**nb_down_sample)][idx, ...], [320//(2**nb_down_sample), 64//(2**nb_down_sample)])

        high = high * STD + MEAN
        low = low * STD + MEAN
        inf = inf * STD + MEAN
        itp = itp * STD + MEAN
        high = np.pad(high, [[0, 0], [32, 32]], mode='constant')
        low = np.pad(low, [[0, 0], [32//(2**nb_down_sample)]*2], mode='constant')
        inf = np.pad(inf, [[0, 0], [32, 32]], mode='constant')
        # inf = np.maximum(inf, 0.0)
        itp = np.pad(itp, [[0, 0], [32, 32]], mode='constant')
        return high, low, inf, itp

    results = {'high': [], 'low': [], 'inf': [], 'itp': []}
    for i in tqdm(range(NB_IMAGES)):
        high, low, inf, itp = get_infer(1)
        results['high'].append(high)
        results['low'].append(low)
        results['inf'].append(inf)
        results['itp'].append(itp)

    np.savez(output, **results)
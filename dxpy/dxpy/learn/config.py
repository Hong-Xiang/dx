from dxpy.filesystem import Path
import os
datasets_configs = {
    
    'dataset_root_path': os.environ.get('PATHS_DATASET', str(Path(os.environ.get('HOME')) / 'Datas')),
    'analytical_phantom_sinogram': {
        'path': '/home/hongxwing/Datas/Phantom',
    },
    'apssr': {
        'image_type': 'sinogram',
        'target_shape': [320, 320],
        'super_resolution': {
            'nb_down_sample': 3
        },
        'with_poission_noise': False
    }
}
config = {
    'train': {
        'save': {
            'frequency': 100,
            'method': 'step'
        },
        'load': {
            'is_load': True,
            'step': -1
        },
        'model_filesystem': {
            'path_model': './model',
            'ckpt_name': 'save'
        },
    },
    'datasets': datasets_configs
}


def get_config():
    from dxpy.configs import ConfigsView
    return ConfigsView(config)


def clear_config():
    global config
    for k in config:
        config.pop(k)

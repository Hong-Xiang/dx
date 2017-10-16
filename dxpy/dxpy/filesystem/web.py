from .path.web import add_api as add_path_api
from .file.web import add_api as add_file_api
from .directory.web import add_api as add_dir_api


def add_apis(api, root, name='fs'):
    root_fs = root + '/{0}'.format(name)
    add_path_api(api, root_fs)
    add_file_api(api, root_fs)
    add_dir_api(api, root_fs)

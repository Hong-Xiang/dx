"""
Decorate functions foo(*args, **kw) to provide `kw` from config objects.
Useage:
Case 1:
@configurable(c)
def foo(xx=None, yy=None, zz=None, name='default_name'):
    pass
Will try to load config by c
Case 2:
@configurable(c)
def foo(xx=None, yy=None, zz=None, name='default_name'):
    pass
Will try to load config by c['defautl_name']

Case 3:
@configurable(c['conf_name'])
def foo(**kw):
    pass
Will try to load config by c['conf_name']
"""
import inspect
from functools import wraps

KEY_NAME = 'name'


def parse_configs(func, *args, _config_object, **kw):
    sig = inspect.signature(func)
    parameter_keys_not_in_args = list(sig.parameters.keys())[len(args):]
    kw_refined = dict()
    for k in parameter_keys_not_in_args:
        if k in kw and kw[k] is not None:
            kw_refined[k] = kw[k]
            continue
        if _config_object.get(k) is not None:
            kw_refined[k] = _config_object.get(k)
            continue
    ba = sig.bind(*args, **kw_refined)
    ba.apply_defaults()
    return ba.arguments


def get_name(func, *args, **kw):
    sig = inspect.signature(func)
    ba = sig.bind_partial(*args, **kw)
    ba.apply_defaults()
    return ba.arguments[KEY_NAME]


class configurable:
    def __init__(self, configs_object=None, with_name=False):
        if configs_object is None:
            configs_object = dict()
        self._c = configs_object
        self._with_name = with_name

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kw):
            config = self._c
            if self._with_name:
                config = config[get_name(func, *args, **kw)]
            return func(**parse_configs(func, *args, **kw, _config_object=config))
        return wrapper

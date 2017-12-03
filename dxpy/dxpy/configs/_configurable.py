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
@configurable(c.get('conf_name'))
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
        if _config_object[k] is not None:
            kw_refined[k] = _config_object[k]
            continue
    from dxpy.debug.utils import dbgmsg
    dbgmsg(kw)
    left_kw = dict()
    for k in kw:
        if kw[k] is not None and not k in kw_refined:
            left_kw[k] = kw[k]
    # for v in sig.parameters.values():
        # if v.kind == inspect.Parameter.VAR_KEYWORD:
            # kw_refined[v.name] = left_kw
    dbgmsg(left_kw)
    ba = sig.bind(*args, **kw_refined, **left_kw)
    ba.apply_defaults()
    dbgmsg(ba.arguments)
    args = dict(ba.arguments)
    args.update(left_kw)
    return ba


def get_name(func, *args, **kw):
    sig = inspect.signature(func)
    ba = sig.bind_partial(*args, **kw)
    ba.apply_defaults()
    return ba.arguments[KEY_NAME]

class configurable:
    def __init__(self, configs_object=None, with_name=False):
        from ._viewer import ConfigsView
        if configs_object is None:
            configs_object = dict()
        if isinstance(configs_object, dict):
            configs_object = ConfigsView(configs_object)
        self._c = configs_object
        self._with_name = with_name

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kw):
            config = self._c
            if self._with_name:
                config = config.get(get_name(func, *args, **kw))
            ba = parse_configs(func, *args, **kw, _config_object=config)
            return func(*ba.args, **ba.kwargs)
        return wrapper

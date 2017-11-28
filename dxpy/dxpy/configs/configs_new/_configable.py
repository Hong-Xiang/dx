"""
Use case:
a function with parameters foo(**kw, name),

if is defined like:
@configurable()
def foo(xx=None, yy=None, zz=None, name='default_name'):
    pass
Will try to load config by c['defautl_name']

if is defined like:
@configurable('conf_name')
def foo(**kw):
    pass
Will try to load config by c['conf_name']
"""
def configurable(name=None):
    pass

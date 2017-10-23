def root(version):
    return "/api/v{version}".format(version=version)


def full(name, suffix=None, version=None, base=None):
    if base is None:
        base = root(version)
    if suffix is None:
        return "{base}/{name}".format(base=base, name=name)
    else:
        return "{base}/{name}/{suffix}".format(base=base, name=name, suffix=suffix)

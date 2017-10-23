def api_format(root, base, version):
    return "{root}/api/v{version}/{base}".format(root=root, version=version, base=base)

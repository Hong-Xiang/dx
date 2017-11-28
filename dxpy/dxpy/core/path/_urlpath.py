class UrlSpec:
    def __init__(self, protocol=None, username=None, password=None, resource=None, params=None):
        self.protocol = protocol
        self.username = username
        self.password = password
        self.resource = resource
        self.params = params

    def __eq__(self, url_spec):
        compares = [self.protocol == url_spec.protocol,
                    self.username == url_spec.username,
                    self.password == url_spec.password,
                    self.resource == url_spec.resource]
        return all(compares)

    @classmethod
    def parse(cls, s):
        p = opener.parse.parse_fs_url(s)
        return cls(p.protocol, p.username, p.password, p.resource, p.params)

    def serilization(self, format='JSON'):
        def to_json_dct():
            return {'protocol': self.protocol,
                    'username': self.username,
                    'password': self.password,
                    'resource': self.resource,
                    'params': self.params}
        if format.upper() == 'JSON':
            pass
        return None


QUOTED_SLASH = qut('/')
DOUBLE_QUOTED_SLASH = qut(qut('/'))


def is_quoted_url(s):
    return QUOTED_SLASH in s


def is_double_quoted_url(s):
    return DOUBLE_QUOTED_SLASH in s


def url_quote_path(path):
    return qut(path)


def url_unquote_path(url):
    return uqut(url)


def url_double_quoted_path(path):
    return qut(qut(path))


def url_double_unquoted_path(path):
    return uqut(uqut(path))


def unified_path_to_str(path):
    if path is None:
        raise NotValidPathError
    if isinstance(path, str):
        if is_quoted_url(path):
            path = url_unquote_path(path)
        return normpath(path)
    if isinstance(path, Path):
        return unified_path_to_str(str(path.path))
    if isinstance(path, pathlib.Path):
        return unified_path_to_str(str(path))
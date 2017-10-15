import json
from .exceptions import InvalidJSONForTask

def check_json(s, is_with_id=False):
    dct = json.loads(s)
    if not dct.get('__task__'):
        raise InvalidJSONForTask(
            "'__task__' not found or is False for JSON: {}".format(s))

    def check_key(dct, key, value_type=None):
        if not key in dct:
            raise InvalidJSONForTask(
                "Required key: {key} is not found in JSON string: {s}".format(key=key, s=s))
        if value_type is not None:
            if not isinstance(dct[key], value_type):
                raise InvalidJSONForTask(
                    "Wrong type for key: {k} with value: {v}".format(k=key, v=dct[k]))

    if is_with_id:
        check_key(dct, 'id', int)
    check_key(dct, 'desc', str)
    check_key(dct, 'data', dict)
    check_key(dct, 'time_stamp', dict)
    check_key(dct['time_stamp'], 'create', (str, type(None)))
    check_key(dct['time_stamp'], 'start', (str, type(None)))
    check_key(dct['time_stamp'], 'end', (str, type(None)))
    check_key(dct, 'state', str)
    check_key(dct, 'is_root', bool)
    check_key(dct, 'worker', str)
    check_key(dct, 'type', str)
    check_key(dct, 'workdir', str)
    check_key(dct, 'dependency', list)

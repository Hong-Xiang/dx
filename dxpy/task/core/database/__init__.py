"""
Task database support module.

JSON Format:
{
    'id': <int>
    'desc': <str>
    'body': <str>
    'dependency': <str> ' '(space) seperated dependency ids.
    'time_create': <str> string of time stamp
    'state': <str> task state
    'is_root': <bool> if task is root
}
"""
# from .api import create, read, read_all, update, delete
# from .model import create_datebase, drop_database

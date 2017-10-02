"""
Task database support module.

JSON Format:
{
    'id': <int>
    'desc': <str>
    'data': <str>    
    'time_create': <str> string of time stamp
    'time_start': <str> string of time stamp
    'time_end': <str> string of time stamp
    'state': <str> task state
    'is_root': <bool> if task is root
}
"""
from .api import create, read, read_all, update, delete
from .model import Database

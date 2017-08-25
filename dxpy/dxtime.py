# Author: Hong Xiang <hx.hongxiang@gmail.com>

"""
A time utility module, used for measure, record and analysis of time related tasks, all time in float are defined in
millisecond, this module defines the following classes:

- `TimeStamp`, a time stamp

Exception classes:

Functions:


"""

import json
import yaml
import time
from flask_restful import Resource
from dxpy.utils import Tags


class TimeDuration:
    sec = 1000.0
    min = 60.0 * sec
    hur = 60.0 * min
    day = 24.0 * hur


def time_now():
    return time.time() * TimeDuration.sec


class TimeReadable:
    from time import strftime, localtime, gmtime
    FULLFORMAT = "%a, %d %b %Y %H:%M:%S"
    MINFORMAT = "{:.3f} secs"
    HURFORMAT = "%M mins, %S secs"
    DAYFORMAT = "%H hurs, %M mins, %S secs"
    MONTHFORMAT = "%d d, %H h, %M m, %S s"

    def __init__(self, time_in_ms=None):
        self.t = time_in_ms

    @property
    def in_second(self):
        return self.t / 1000.0

    @staticmethod
    def _parse_full(data_str):
        pt = re.compile(r'(.*), (\d+) (\w+) (\d+) (\d+):(\d+):(\d+)')
        if pt.match(data_str):
            return TimeReadable(time.mktime(time.strptime(data_str, TimeReadable.FULLFORMAT)) * TimeDuration.sec)
        return None

    @staticmethod
    def _parse_min(data_str):
        pt = re.compile(r'(\d+\.?\d*) secs')
        if pt.match(data_str):
            return float(pt.match(data_str)[1]) * TimeDuration.sec

    @staticmethod
    def _parse_hur(data_str):
        try:
            return TimeReadable(time.mktime(time.strptime(data_str, TimeReadable.FULLFORMAT)) * TimeDuration.sec)

    @staticmethod
    def _parse(data_str, format):
        return TimeReadable(time.mktime(time.strptime(data_str, format)) * TimeDuration.sec)

    @staticmethod
    def load(data_str):
        import re
        if

        pt_less
        if pt_less_hur.

    def to_format(self, format, time_system=None):
        if time_system is None:
            time_system = time.gmtime
        return time.strftime(format, time_system(self.in_second))

    @property
    def full(self):
        if self.t is None:
            return Tags.undifined
        return self.to_format(TimeReadable.FULLFORMAT, time.localtime)

    @property
    def duration(self):
        if self.t is None:
            return Tags.undifined
        elif self.t < TimeDuration.min:
            return TimeReadable.MINFORMAT.format(self.in_second)
        elif self.t < TimeDuration.hur:
            return self.to_format(TimeReadable.HURFORMAT)
        elif self.t < TimeDuration.day:
            return self.to_format(TimeReadable.DAYFORMAT)
        else:
            return self.to_format(TimeReadable.MONTHFORMAT)


class TimeStamp(yaml.YAMLObject):
    """ A time stamp object.


    Members:

    - start: float, start time in secs,
    - run: float, run time in secs,
    - end: float, [Optional, Default=0.0], end time in secs

    Methods:


    """

    yaml_tag = '!time_stamp'

    def __init__(self, start=None, run=None, end=None):
        self.start = start or time_now()
        self.run = run or time_now() - self.start
        self.end = end

    def now(self):
        return TimeStamp(self.start, end=self.end)

    @property
    def eta(self):
        if self.end > self.start:
            return self.end - self.start - self.run
        else:
            return None

    @classmethod
    def to_yaml(cls, dumper, data):
        return yaml.MappingNode(cls.yaml_tag, value=[
            (yaml.ScalarNode(tag='tag:yaml.org,2002:str', value='start'),
             yaml.ScalarNode(tag='tag:yaml.org,2002:str', value=TimeReadable(data.start).full)),
            (yaml.ScalarNode(tag='tag:yaml.org,2002:str', value='run'),
             yaml.ScalarNode(tag='tag:yaml.org,2002:str', value=TimeReadable(data.run).duration)),
            (yaml.ScalarNode(tag='tag:yaml.org,2002:str', value='end'),
             yaml.ScalarNode(tag='tag:yaml.org,2002:str', value=TimeReadable(data.end).full))
        ])

    @classmethod
    def from_yaml(cls, loader, node):
        import calendar
        data = loader.construct_mapping(node)
        start = calendar.timegm()
        return

    def _to_readable(self):
        from dxpy.utils import Tags
        msg_start = strftime("%a, %d %b %Y %H:%M:%S", localtime(self.start))
        msg_run = readable_duration(self.run)
        if self.end:
            msg_end = strftime("%a, %d %b %Y %H:%M:%S", localtime(self.end))
        else:
            msg_end = Tags.undifined
        msg_times = {
            'start': msg_start,
            'end': msg_end,
            'run': msg_run
        }
        out = {k: msg_times[k] for k in msg_times}

    @property
    def __repr__(self):
        from dxpy.utils import Tags
        if fields is None:
            fields = ('start', 'end', 'run')
        msg_start = strftime("%a, %d %b %Y %H:%M:%S", localtime(self.start))
        msg_run = readable_duration(self.run)
        if self.end:
            msg_end = strftime("%a, %d %b %Y %H:%M:%S", localtime(self.end))
        else:
            msg_end = Tags.undifined
        msg_times = {
            'start': msg_start,
            'end': msg_end,
            'run': msg_run
        }
        out = {k: msg_times[k] for k in msg_times}
        return out

    def __str__(self):
        return yaml.dump(self.info(), default_flow_style=False, Dumper=yaml)

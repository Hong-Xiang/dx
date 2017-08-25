"""
A 
"""
import json
import yaml
from time import strftime, localtime, time, gmtime
from flask_restful import Resource
from dxpy.time.io import readable_duration

class TimeStamp(yaml.YAMLObject):
    """ Time stamp of a object.

    Members:
        * start: float, start time in secs,
        * run: float, run time in secs,
        * end: float, [Optional, Default=0.0], end time in secs
    
    Methods:
    """
    
    def __init__(self, start=None, run=None, end=None):
        self.start = start or time()
        self.run = run or time()-self.start
        self.end = end or 0.0

    def update_run(self):
        self.run = time() - self.start

    def info(self, fields=None):
        if fields is None:
            fields = ('start', 'end', 'run')
        msg_start = strftime("%a, %d %b %Y %H:%M:%S", localtime(self.start))
        msg_run = readable_duration(self.run)
        if self.end:
            msg_end = strftime("%a, %d %b %Y %H:%M:%S", localtime(self.end))
        else:
            msg_end = 'UNKONWN'
        msg_times = {
            'start': msg_start,
            'end': msg_end,
            'run': msg_run
        }
        out = {k: msg_times[k] for k in msg_times}
        return out

    @property
    def eta(self):
        if self.end > self.start:
            return self.end - self.start - self.run
        else:
            return None

    def __str__(self):        
        return yaml.dump(self.info(), default_flow_style=False, Dumper=yaml)
    
    # class _JSONEncoder(json.JSONEncoder):
    #     """ JSON encoder of TimeStamp cls """
    #     def default(self, obj):
    #         if isinstance(obj, TimeStamp):
    #             dct = {
    #                 '__TimeStamp__': True,
    #                 'start': obj.start,
    #                 'run': obj.run,
    #                 'end': obj.end
    #             }
    #             return dct
    #         return json.JSONEncoder.default(self, obj)

    # @staticmethod
    # def json_decoder(dct):
    #     """ JSON decoder of TimeStamp cls """
    #     if '__TimeStamp__' in dct:
    #         start = dct.get('start')
    #         run = dct.get('run')
    #         end = dct.get('end', 0.0)
    #         return TimeStamp(start=start, run=run, end=end)
    #     else:
    #         return dct
    
    # def to_json(self):
    #     return json.dumps(self, cls=TimeStamp._JSONEncoder)

    # @staticmethod
    # def from_json(s):
    #     return json.loads(s, object_hook=TimeStamp.json_decoder)


    # For test only, time stamp is not intend to save to database
    # db_model = None
    # @staticmethod
    # def get_db_model(db):
    #     if TimeStamp.db_model is None:
    #         class TimeStampDatabaseModel(db.Model):
    #             id = db.Column(db.Integer, primary_key=True)
    #             start = db.Column(db.Float)
    #             end = db.Column(db.Float)
    #             run = db.Column(db.Float)

    #             def __init__(self, start, run, end):
    #                 self.start = start
    #                 self.run = run
    #                 self.end = end
    #         TimeStamp.db_model = TimeStampDatabaseModel
    #         return TimeStampDatabaseModel
    #     else:
    #         return TimeStamp.db_model

    # @staticmethod
    # def from_dbobj(obj):
    #     return TimeStamp(obj.start, obj.run, obj.end)

    # def to_dbobj(self, db):
    #     return self.get_db_model(db)(self.start, self.run, self.end)


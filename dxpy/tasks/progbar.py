""" ProgBar 
Report services:
    print to sys.stdout
    print to file
    report to http server
"""
# TODO: Implement HTTP Report
# TODO: Implement nested ProgBar
# TODO: Test print to file

import time
import requests
import sys
import json
from dxpy.time.stamp import TimeStamp
from dxpy.time.io import readable_duration


class ProgBarReporter:
    def __init__(self, min_report_intervel=None, verbose=None):
        if min_report_intervel is None:
            min_report_intervel = 1.0
        if verbose is None:
            verbose = 1
        self._min_report_interval = min_report_intervel
        self._last_report = -self._min_report_interval
        self._verbose = verbose

    def dump(self, bar):
        if (time.time() - self._last_report) < self._min_report_interval:
            return None
        else:
            self._dump_core(bar.state_msg(self._verbose))
            self._last_report = time.time()

    def _dump_core(self, msg):
        raise NotImplementedError


class ReporterPrint(ProgBarReporter):
    def __init__(self, file=None, min_report_interval=None, verbose=None):
        super(self.__class__, self).__init__(min_report_interval, verbose)
        if file is None:
            self._file = sys.stdout
        else:
            self._file = file

    def _dump_core(self, msg):
        if isinstance(self._file, str):
            with open(self._file, 'a') as fout:
                print(msg, file=fout)
        else:
            print(msg, file=self._file)


class ReporterHttp(ProgBarReporter):
    def __init__(self,
                 task_id,
                 report_url=None,
                 server_port=None,
                 min_report_interval=None,
                 verbose=None):
        super(self.__class__, self).__init__(min_report_interval, verbose)
        self._task_id = task_id
        self._port = server_port or 5000
        self._url = r"http://localhost:{port}/task/{task_id}/progbar"

    def _dump_core(self, msg):
        url_server = self._url.format(port=self._port, task_id=self._task_id)
        r = requests.get(url_server)
        if r.status_code != 200:
            raise ValueError(
                "Wrong http status code {code}.".format(code=r.status_code))
        r = requests.put(self._url, {'msg': msg})

# MAIN_BAR = None

class ProgBar:
    def __init__(self,
                 step_total=1,
                 step_now=0,
                 time_stamp=None,
                 message=None,
                 out_bar=None):
        """ ProgBar

        Inputs:
            * task_id: <int>, [Optional], if not provided, http report service would
                not be avaliable,
        """
        # Times
        self._step_total = step_total
        self._step_now = step_now

        if time_stamp is None:
            if out_bar is not None:
                self._time_stamp = out_bar._time_stamp
            else:
                self._time_stamp = TimeStamp()
        else:
            self._time_stamp = time_stamp

        self._message = message or ""

        self.out_bar = out_bar

        self._reports = None

        self._progress = None
        self._eta = None
        step_progress_base = self.out_bar._step_progress if self.out_bar else 1.0
        self._step_progress = step_progress_base / self._step_total
        self.step(self._step_now)

    def set_reports(self, reports):
        self._reports = reports

    @property
    def start(self):
        return self._time_stamp.start

    @property
    def end(self):
        return self._time_stamp.end

    @property
    def run(self):
        return self._time_stamp.run

    @property
    def progress(self):
        return self._progress

    @property
    def step_now(self):
        return self._step_now

    @property
    def step_total(self):
        return self.step_total

    @property
    def eta(self):
        time_eta = self._time_stamp.eta
        if time_eta is None:
            time_eta = -1.0
        return time_eta

    def step(self, step_now):
        # update step_now and time_stamp
        self._step_now = step_now
        self._time_stamp.update_run()

        # update progress
        if self.out_bar is None:
            self._progress = self._step_now / self._step_total
        else:
            self._progress = self.out_bar.progress + self._step_progress * self._step_now

        # update eta
        time_ela = self.run
        pgs = self._progress

        
        if pgs > 0.0:
            time_eta = time_ela / pgs * (1 - pgs)
        else:
            time_eta = -1.0
        # update time_stamp
        self._time_stamp.end = self.start + self.run + time_eta

    def state_msg(self, verbose=1):
        pgs = self.progress
        time_ela = self.run
        msg_ela = readable_duration(time_ela)
        time_eta = self.eta
        
        if time_eta >= 0.0:
            msg_eta = readable_duration(time_eta)
        else:
            msg_eta = 'UKNOWN'
        time_msg = "[PB: {0: 3.3f}% | {1} << {2} ]".format(
            pgs * 100, msg_ela, msg_eta)
        msg_now = self._message.format(step_now=self._step_now)
        if verbose == 0:
            return msg_now
        elif verbose == 1:
            return time_msg + msg_now
        elif verbose == 2:
            return time_msg + self.out_bar.state_msg(0) + msg_now
        elif verbose == 3:
            return time_msg + self.out_bar.state_msg(0) + msg_now + " Start: {start}. ".format(start=self._time_stamp.info()['start'])
        elif verbose == 4:
            return time_msg + self.out_bar.state_msg(0) + msg_now + str(self._time_stamp)

    def report(self):
        for srv in self._reports:
            srv.dump(self)

    class _JSONEncoder(json.JSONEncoder):
        """ JSON encoder of ProgBar cls """

        def default(self, obj):
            if isinstance(obj, ProgBar):
                dct = {
                    '__ProgBar__': True,
                    'step_total': obj._step_total,
                    'step_now': obj._step_now,
                    'message': obj._message
                }
                if obj.out_bar is None:
                    dct['time_stamp'] = obj._time_stamp.to_json()
                    dct['out_bar'] = None
                else:
                    dct['out_bar'] = obj.out_bar.to_json()
                return dct
            return json.JSONEncoder.default(self, obj)

    @staticmethod
    def json_decoder(dct):
        """ JSON decoder of ProgBar cls """
        if '__ProgBar__' in dct:
            step_total = dct['step_total']
            step_now = dct['step_now']
            message = dct['message']
            out_bar = dct['out_bar']
            if out_bar:
                out_bar = ProgBar.from_json(out_bar)
                time_stamp = out_bar._time_stamp
            else:
                time_stamp = TimeStamp.from_json(dct['time_stamp'])

            return ProgBar(step_total=step_total,
                           step_now=step_now,
                           time_stamp=time_stamp,
                           message=message,
                           out_bar=out_bar)
        else:
            return dct

    def to_json(self):
        return json.dumps(self, cls=ProgBar._JSONEncoder)

    @staticmethod
    def from_json(s):
        return json.loads(s, object_hook=ProgBar.json_decoder)

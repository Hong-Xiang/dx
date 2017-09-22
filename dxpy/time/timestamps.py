from dxpy.time.utils import now, delta


class TimeStamps:
    """ A dict of time stamps
    """

    def __init__(self, time_stamps=None):
        if isinstance(time_stamps, TimeStamps):
            time_stamps = time_stamps.time_stamps
        if not isinstance(time_stamps, dict):
            raise TypeError(
                "time_stamps must be a dict, not {}.".format(type(time_stamps)))
        self.time_stamps = time_stamps


class Start(TimeStamps):
    def __init__(self, start=None):
        if start is None:
            start = now()
        super(Start, self).__init__({'start': start})

    @property
    def start(self):
        return self.time_stamps['start']


class Duration(Start):
    def __init__(self, start, end):
        super(__class__, self).__init__(start=start)
        self.time_stamps['end'] = end

    @property
    def end(self):
        return self.time_stamps['end']

    @property
    def length(self):
        return self.end - self.start

    def update_end(self, end):
        self.time_stamps['end'] = end


class Run(Start):
    def __init__(self, start, run=None):
        super(__class__, self).__init__(start=start)
        if run is None:
            run = delta()
        self.run = run

    def update_run(self):
        self.run = now() - self.start


class Progress(Duration, Run):
    def __init__(self, start, end, run=None):
        Duration.__init__(self, start=start, end=end)
        if run is None:
            run = delta()
        self.run = run

    @property
    def progress(self):
        return self.run / self.length

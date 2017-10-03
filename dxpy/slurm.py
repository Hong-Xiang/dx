import rx
from rx import Observable
from collections import namedtuple
import re
import os

SINFO = namedtuple('SINFO', ('id', 'part', 'cmd', 'usr',
                             'stat', 'time', 'nodes', 'node_name'))


class TaskInfo:
    def __init__(self, tid, part, cmd, usr, stat, time, nodes, node_name, *args):
        self.id = int(tid)
        self.part = part
        self.cmd = cmd
        self.usr = usr
        self.stat = stat
        self.time = time
        self.nodes = nodes
        self.node_name = node_name

    @classmethod
    def from_squeue(cls, l):
        s = re.sub('\s+', ' ', l).strip()
        items = s.split()
        if not items[0].isdigit():
            return None
        else:
            return cls(*items)

# class Slurm:
#     def __init__(self):
#         self._sinfo_buffer = None

#     def _assign_sinfo(self, value):
#         self._sinfo_buffer = value

#     def _sinfo_kernel(self):
#         (Observable.from_(os.popen('squeue').readlines())
#          .map(lambda l: re.sub('\s+', ' ', l).strip())
#          .map(lambda l: l.split(' '))
#          .filter(lambda l: l[0].isdigit())
#          .map(lambda s: [int(s[0])] + s[1:])
#          .map(lambda s: SINFO(*s))
#          .to_list()
#          .subscribe(lambda s: self._assign_sinfo(s)))

#     def sinfo(self):
#         self._sinfo_kernel()
#         if self._sinfo_buffer is None:
#             self._sinfo_buffer = []
#         return self._sinfo_buffer

#     def srun(command):
#         with os.popen(command) as fin:
#             return fin.readlines()

def sbatch(workdir, script_file):
    with os.popen('cd {dir} && sbatch {file}'.format(dir=workdir, file=script_file)) as fin:
        return sid_from_submit(fin.readlines()[0])

def sid_from_submit(s):
    return int(re.sub('\s+', ' ', s).strip().split(' ')[3])

def squeue():
    return (Observable.from_(os.popen('squeue').readlines())
            .map(lambda l: TaskInfo.from_squeue(l))
            .filter(lambda l: l is not None))

def is_complete(sid):
    return (squeue()
            .subscribe_on(rx.concurrency.ThreadPoolScheduler())
            .filter(lambda tinfo: tinfo.id == sid)
            .count()
            .to_blocking().first()) == 0

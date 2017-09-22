"""
    
"""
import rx
from dxpy.file_system.path import Path
from dxpy.time.timestamps import Start
import dxpy.task.misc as misc
from .templates import create
import yaml


def sleep(workdir, duration, workers=None, desc='sleep task', depens=None):
    if workers is None:
        workers = misc.Workers(misc.WorkerType.MultiThreading)
    if depens is None:
        depens = []
    task = create('COMMAND', tid=None,
                  command='sleep {:d}'.format(duration),
                  desc=desc,
                  workdir=workdir,
                  workers=workers,
                  activity=True,
                  state=misc.TaskState.BeforeSubmit,
                  time_stamps=Start(),
                  dependency=depens,
                  is_root=True)
    return rx.Observable.just(task)


def sleep_chain(workdir, duration, creator, nb_chain=3, workers=None, desc='sleep chain'):
    def descn(x): return desc + ' #{:d}'.format(x)

    def slp(desc, depens=None):
        return TaskCommand(tid=None,
                           desc=desc,
                           workdir=workdir,
                           workers=workers,
                           activity=True,
                           state=misc.TaskState.BeforeSubmit,
                           time_stamps=Start(),
                           dependency=depens,
                           is_root=True,
                           command='sleep {:d}'.format(duration))

    result = rx.Observable.just((0, []))
    for i in range(nb_chain):
        result = (result
                  .map(lambda x: (x[0], slp(descn(x[0]), x[1])))
                  .map(lambda x: (x[0], creator(x[1])))
                  .map(lambda x: (x[0] + 1, [x[1]])))
    return result

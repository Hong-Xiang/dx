import tensorflow as tf
from dxpy.filesystem.path import Path
from dxpy.filesystem.directory import Directory
from .base import Net


class Saver(Net):
    def __init__(self, config, global_step):
        super(__class__, self).__init__(config)
        self.saver = tf.train.Saver()
        self.add_node('global_step', global_step)
        self.model_dir = Directory(Path(self.config['model_dir']))
        self.model_dir.ensure()
        self.model_path = self.model_dir.path / self.config['ckpt_name']

    def run(self, session):
        self.save(session)

    def echo(self, task, step):
        if task.upper() == 'SAVE':
            msg = "[SAVE] model with step: {} to path: {}."
            print(msg.format(step, self.model_path))
        else:
            path_load = self.resolve_path_load(step)
            print("[LOAD] model from: {}.".format(path_load))

    def save(self, session):
        step = session.run(self.gs)
        self.echo('SAVE', step)
        self.saver.save(session, self.model_path, global_step=step)

    def resolve_path_load(self, step):
        path_load = pathlib.Path(self.params['model_dir'])
        step = self.params['load_step']
        if step == -1:
            if not path_load.is_dir():
                return
            pattern = self.params['ckpt_name'] + '-' + '([0-9]+)' + '-*'
            p = re.compile(pattern)
            for f in path_load.iterdir():
                mat = p.match(f.name)
                if mat and step < int(mat[1]):
                    step = int(mat[1])
        path_load = str(path_load / self.params['ckpt_name'])
        path_load += '-%d' % (step)
        return path_load

    def load(self, session, step):
        self.echo('SAVE', step)
        self.saver.restore(sess, path_load)
        self.nodes['global_step'].run(session, "SET", {'global_step': step})

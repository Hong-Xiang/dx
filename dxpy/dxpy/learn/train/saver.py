import tensorflow as tf
from dxpy.filesystem import Path
from ..graph import Graph

_instance = None


def get_saver():
    global _instance
    if _instance is None:
        _instance = Saver()
    return _instance


class Saver(Graph):
    def __init__(self, name='/saver', **config):
        super(__class__, self).__init__(name, **config)
        self._saver = None
        self.register_task('save', self.__save)
        self.register_task('load', self.__load)

    @classmethod
    def _default_config(cls):
        return {'model_dir': './save',
                'ckpt_name': 'save'}

    def _model_path(self):
        return str(Path(self.c['model_dir']) / self.config['ckpt_name'])

    def __save(self, feeds):
        from ..scalar import global_step
        if self._saver is None:
            self._saver = tf.train.Saver()
        sess = tf.get_default_session()
        step = sess.run(global_step())
        self.echo('SAVE', step)
        self.saver.save(sess, self.c['model_dir'], global_step=step)

    def resolve_path_load(self, feeds):
        from fs.osfs import OSFS
        path_load = Path(self.c['model_dir'])
        if path_load.isrel:
            root = '.'
        else:
            root = '/'
        with OSFS(root) as fs:
            step = self.param('step', feeds)
            if step == -1:
                if not fs.isdir(str(path_load)):
                    raise ValueError(
                        "Invalid load path {}.".format(str(path_load)))
                p = re.compile(self.param('ckpt_name', feeds) + '-([0-9]+)-*')
                # TODO: Start here:
                for f in fs.listdir(path_load)
                    mat = p.match(f)
                    if mat and step < int(mat[1]):
                        step = int(mat[1])
            path_load = str(path_load / self.params['ckpt_name'])
            path_load += '-%d' % (step)
        return path_load

    def __load(self, feeds):
        from ..scalar import global_global_step
        if self._saver is None:
            self._saver = tf.train.Saver()
        sess = tf.get_default_session()
        path_load = self.resolve_path_load(feeds['step'])
        print("[LOAD] model from: {}.".format(path_load))
        self._saver.restore(sess, path_load)

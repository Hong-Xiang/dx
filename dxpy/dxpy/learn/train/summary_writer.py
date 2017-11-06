import tensorflow as tf

from ..graph import Graph


class SummaryWriter(Graph):
    @classmethod
    def _default_config(cls):
        result = dict()
        result.update(super()._default_config())
        result.update({'path': './summary',
                       'add_prefix': False})
        return result

    def __init__(self, name, tensors=None, inputs=None, **config):
        super().__init__(name, **config)
        if tensors is None:
            tensors = dict()
        if inputs is None:
            inputs = dict()

        self._tensors = self._default_summaries()
        self._tensors.update(tensors)
        self._inputs = inputs
        for k in self._inputs:
            self.register_node(k, self._inputs[k])
        self._summary_ops = list()
        self.register_task('create_writer', self._create_writer)
        self.register_main_task(self.summary)
        self.register_task('flush', self.flush)

        if self.param('add_prefix'):
            with tf.name_scope('summary'):
                self._add_all_ops()
        else:
            self._add_all_ops()

    def _add_all_ops(self):
        self._add_tensors_to_summary()
        self._add_main_op()

    def _add_main_op(self):
        if len(self._summary_ops) > 0:
            self.register_main_node(tf.summary.merge(self._summary_ops))

    @classmethod
    def _default_summaries(cls):
        from ..scalar import global_step
        return {
            'global_step': {
                'tensor': global_step(),
                'type': 'scalar'
            }
        }

    def post_session_created(self):
        self.run('create_writer')

    def _create_writer(self, feeds):
        self.register_node('summary_writer', tf.summary.FileWriter(self.param('path', feeds),
                                                                   tf.get_default_session().graph))

    def _get_summary_name(self, name):
        if self.param('add_prefix'):
            return self.basename + '/' + name
        else:
            return name

    def _add_tensors_to_summary(self):
        for n, v in self._tensors.items():
            if v is None:
                continue
            op = None
            if v['type'] == 'scalar':
                op = tf.summary.scalar(self._get_summary_name(n),
                                       v['tensor'])
            elif v['type'] == 'image':
                op = tf.summary.image(self._get_summary_name(n),
                                      v['tensor'])
            if op is not None:
                self._summary_ops.append(op)

    def summary(self, feeds=None):
        from ..scalar import global_global_step
        if self.as_tensor() is None:
            return
        value = tf.get_default_session().run(self.as_tensor(), feeds)
        self.nodes['summary_writer'].add_summary(value,
                                                 global_global_step.get_value())

    def flush(self):
        self.nodes['summary_writer'].flush()

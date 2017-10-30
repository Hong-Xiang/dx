import tensorflow as tf
from ..graph import Graph


class GlobalStep(Graph):
    def __init__(self, name='global_step'):
        super(__class__, self).__init__(name)
        gs = tf.Variable(0, dtype=tf.int32, trainable=False,
                         name='global_step')
        with tf.name_scope('global_step_setter'):
            new_value = tf.placeholder(dtype=tf.int32, name='new_value')
            setter = gs.assign(new_value)
        self.register_node('main', gs)
        self.register_node('new_value', new_value)
        self.register_node('setter', setter)
        self.register_task('main')

    def old(self):
        self.gs = tf.Variable(
            0, dtype=tf.int32, trainable=False, name='global_step')

        self.add_node('global_step', tensor=self.gs, shape=[])

    def run(self, session, task=None, feeds=None):
        if task is None or task.upper() == "GET":
            return session.run(self.main)
        elif task.upper() == "SET":
            return session.run(self.__gs_setter, feed_dict={self.__gs_setter: feeds['global_step']})
        self.run_unknwn_task(session, task)
